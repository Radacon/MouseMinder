from __future__ import annotations

import json
import queue
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import serial
from serial.tools import list_ports

DEFAULT_HEX_PATH = Path(r"C:\Users\robot\Documents\Atmel Studio\7.0\MouseMinder\MouseMinder\Debug\MouseMinder.hex")
DEFAULT_GITHUB_HEX_URL = "https://github.com/Radacon/MouseMinder/blob/main/codebase/AtmelStudio/MouseMinder/MouseMinder/Debug/MouseMinder.hex"
HTTP_USER_AGENT = "MouseMinderGui/1.0"


class ToasterGui:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Arduino Toaster")
        self.root.geometry("760x860")

        self.event_queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.serial_lock = threading.RLock()
        self.serial_conn: serial.Serial | None = None
        self.reader_thread: threading.Thread | None = None
        self.discovery_thread = threading.Thread(target=self._discovery_loop, daemon=True)
        self.running = True
        self.connected_port = ""
        self.handshake_complete = False
        self.hex_path = Path()
        self.hex_send_in_progress = False
        self.github_refresh_in_progress = False
        self.cached_github_hex_lines: list[str] = []
        self.cached_github_hex_hash = ""
        self.cached_github_hex_url = ""

        self.connection_var = tk.StringVar(value="Disconnected")
        self.state_var = tk.StringVar(value="WAIT_GUI")
        self.device_var = tk.StringVar(value="")
        self.chip_id_var = tk.StringVar(value="")
        self.prompt_var = tk.StringVar(value="Waiting for operator input.")
        self.hex_var = tk.StringVar(value="No file selected")
        self.firmware_source_var = tk.StringVar(value="github")
        self.github_url_var = tk.StringVar(value=DEFAULT_GITHUB_HEX_URL)
        self.github_hash_var = tk.StringVar(value="Git hash: loading...")
        self.clear_memory_var = tk.BooleanVar(value=False)
        self.pin_value_labels: dict[str, tk.Label] = {}
        self.pin_adc_labels: dict[str, tk.Label] = {}
        self.connection_label: tk.Label | None = None
        self.operator_prompt_label: tk.Label | None = None

        self.pin_vars = {
            "BATT": {"mode": tk.StringVar(value="-"), "value": tk.StringVar(value="-"), "adc": tk.StringVar(value="")},
            "LATCHED": {"mode": tk.StringVar(value="-"), "value": tk.StringVar(value="-"), "adc": tk.StringVar(value="")},
        }

        self._build_ui()
        self._load_default_hex()
        self._refresh_github_hash()
        self.discovery_thread.start()
        self.root.after(100, self._pump_events)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)

        chip_id = ttk.LabelFrame(main, text="Read Chip ID", padding=12)
        chip_id.pack(fill="x", pady=(12, 0))
        ttk.Label(chip_id, textvariable=self.chip_id_var).pack(anchor="w")

        operator = ttk.LabelFrame(main, text="OPERATOR ACTIONS", padding=12)
        operator.pack(fill="x", pady=(12, 0))
        self.operator_prompt_label = tk.Label(
            operator,
            textvariable=self.prompt_var,
            wraplength=700,
            bg="#ffffff",
            fg="#b42318",
            justify="center",
            anchor="center",
            padx=12,
            pady=16,
        )
        self.operator_prompt_label.pack(fill="x")

        file_frame = ttk.LabelFrame(main, text="Firmware", padding=12)
        file_frame.pack(fill="x", pady=(12, 0))
        github_row = ttk.Frame(file_frame)
        github_row.pack(fill="x", anchor="w")
        ttk.Radiobutton(
            github_row,
            text="GitHub",
            variable=self.firmware_source_var,
            value="github",
        ).pack(side="left")
        ttk.Label(github_row, textvariable=self.github_hash_var).pack(side="left", padx=(12, 0))
        ttk.Button(github_row, text="Refresh Hash", command=self._refresh_github_hash).pack(side="right")

        ttk.Entry(file_frame, textvariable=self.github_url_var).pack(fill="x", pady=(6, 8))

        local_row = ttk.Frame(file_frame)
        local_row.pack(fill="x", anchor="w")
        ttk.Radiobutton(
            local_row,
            text="Local .hex",
            variable=self.firmware_source_var,
            value="local",
        ).pack(side="left")
        ttk.Label(local_row, textvariable=self.hex_var).pack(side="left", padx=(12, 0))

        ttk.Checkbutton(
            file_frame,
            text="Clear memory only",
            variable=self.clear_memory_var,
        ).pack(anchor="w", pady=(8, 0))

        buttons = ttk.Frame(file_frame)
        buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(buttons, text="Select .hex", command=self._select_hex).pack(side="left")
        ttk.Button(buttons, text="Restart Loop", command=self._restart_loop).pack(side="left", padx=(8, 0))
        ttk.Button(buttons, text="Rescan Ports", command=self._force_disconnect).pack(side="left", padx=(8, 0))

        pins = ttk.LabelFrame(main, text="Pin States", padding=12)
        pins.pack(fill="x", pady=(12, 0))
        grid = ttk.Frame(pins)
        grid.pack(fill="x")
        ttk.Label(grid, text="Pin", width=12).grid(row=0, column=0, sticky="w")
        ttk.Label(grid, text="Mode", width=12).grid(row=0, column=1, sticky="w")
        ttk.Label(grid, text="Value", width=16).grid(row=0, column=2, sticky="w")
        ttk.Label(grid, text="ADC", width=16).grid(row=0, column=3, sticky="w")
        for row, pin_name in enumerate(("BATT", "LATCHED"), start=1):
            ttk.Label(grid, text=pin_name, width=12).grid(row=row, column=0, sticky="w", pady=(4, 0))
            ttk.Label(grid, textvariable=self.pin_vars[pin_name]["mode"], width=12).grid(row=row, column=1, sticky="w", pady=(4, 0))
            value_label = tk.Label(grid, textvariable=self.pin_vars[pin_name]["value"], width=16, anchor="w", fg="#666666")
            value_label.grid(row=row, column=2, sticky="w", pady=(4, 0))
            adc_label = tk.Label(grid, textvariable=self.pin_vars[pin_name]["adc"], width=16, anchor="w", fg="#666666")
            adc_label.grid(row=row, column=3, sticky="w", pady=(4, 0))
            self.pin_value_labels[pin_name] = value_label
            self.pin_adc_labels[pin_name] = adc_label

        log_frame = ttk.LabelFrame(main, text="Log", padding=12)
        log_frame.pack(fill="both", expand=True, pady=(12, 0))
        self.log_text = tk.Text(log_frame, height=14, wrap="word", state="disabled")
        self.log_text.pack(fill="both", expand=True)

        connection = ttk.LabelFrame(main, text="Connection", padding=12)
        connection.pack(fill="x", pady=(12, 0))
        self.connection_label = tk.Label(
            connection,
            textvariable=self.connection_var,
            font=("Segoe UI", 11, "bold"),
            fg="#b42318",
            anchor="w",
        )
        self.connection_label.pack(anchor="w")

    def _select_hex(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Select firmware",
            filetypes=[("Hex files", "*.hex"), ("All files", "*.*")],
        )
        if not file_path:
            return
        self.hex_path = Path(file_path)
        self.hex_var.set(str(self.hex_path))
        self._log(f"Selected firmware: {self.hex_path}")

    def _load_default_hex(self) -> None:
        if DEFAULT_HEX_PATH.exists():
            self.hex_path = DEFAULT_HEX_PATH
            self.hex_var.set(str(self.hex_path))
            self._log(f"Default firmware loaded: {self.hex_path}")

    def _restart_loop(self) -> None:
        self._send_line("RESET_LOOP")
        self._log("Requested loop restart")

    def _pump_events(self) -> None:
        while True:
            try:
                event, payload = self.event_queue.get_nowait()
            except queue.Empty:
                break

            if event == "connected":
                self.connected_port = str(payload)
                self.handshake_complete = False
                self.connection_var.set(f"Connected on {self.connected_port}")
                if self.connection_label:
                    self.connection_label.configure(fg="#1a7f37")
                self._log(f"Connected to toaster on {self.connected_port}")
                self._send_line("GUI_HELLO")
            elif event == "disconnected":
                self.connection_var.set("Disconnected")
                self.state_var.set("WAIT_GUI")
                self.device_var.set("")
                self.chip_id_var.set("")
                self.prompt_var.set("Waiting for Arduino toaster.")
                if self.connection_label:
                    self.connection_label.configure(fg="#b42318")
                self.handshake_complete = False
                self.connected_port = ""
                self._reset_pins()
                self._log("Disconnected from toaster")
            elif event == "line":
                self._handle_line(str(payload))

        if self.running:
            self.root.after(100, self._pump_events)

    def _handle_line(self, line: str) -> None:
        if not line:
            return

        if line.startswith("HELLO "):
            if not self.handshake_complete:
                self._send_line("GUI_HELLO")
            return

        if line.startswith("ACK GUI"):
            self.handshake_complete = True
            self._log("GUI handshake complete")
            return

        if line.startswith("STATUS "):
            _, state, *rest = line.split(" ")
            message = " ".join(rest).replace("_", " ")
            self.state_var.set(state)
            self.prompt_var.set(message)
            return

        if line.startswith("DEVICE "):
            parts = line.split(" ")
            if len(parts) >= 4 and parts[1] == "VALID":
                self.device_var.set(parts[2])
                self.chip_id_var.set(parts[3])
            else:
                self.device_var.set("")
                self.chip_id_var.set("")
            return

        if line.startswith("PIN "):
            parts = line.split(" ", 3)
            if len(parts) == 4 and parts[1] in self.pin_vars:
                self._update_pin_display(parts[1], parts[2], parts[3])
            return

        if line.startswith("REQUEST HEX"):
            self._handle_hex_request()
            return

        if line.startswith("RESULT "):
            self._log(line.replace("_", " "))
            return

        if line.startswith("LOG "):
            self._log(line[4:].replace("_", " "))
            return

        self._log(line)

    def _handle_hex_request(self) -> None:
        if self.hex_send_in_progress:
            return
        if self.clear_memory_var.get():
            self.hex_send_in_progress = True
            threading.Thread(target=self._send_clear_hex, daemon=True).start()
            return
        if self.firmware_source_var.get() == "local" and (not self.hex_path or not self.hex_path.exists()):
            self._log("Hex requested but no firmware file is selected")
            self._send_line("ABORT")
            return
        if self.firmware_source_var.get() == "github" and not self.github_url_var.get().strip():
            self._log("Hex requested but no GitHub HEX URL is configured")
            self._send_line("ABORT")
            return

        self.hex_send_in_progress = True
        threading.Thread(target=self._send_hex_file, daemon=True).start()

    def _send_hex_file(self) -> None:
        try:
            source_name, lines = self._load_selected_hex_lines()
            self._log(f"Sending firmware: {source_name}")
            for line in lines:
                self._send_raw(line + "\n")
                time.sleep(0.01)
            self._log("Firmware transfer complete")
        except Exception as exc:
            self._log(f"Firmware transfer failed: {exc}")
            self._send_line("ABORT")
        finally:
            self.hex_send_in_progress = False

    def _send_clear_hex(self) -> None:
        try:
            self._log("Sending blank HEX for clear-memory mode")
            self._send_raw(":00000001FF\n")
            time.sleep(0.01)
            self._log("Blank HEX transfer complete")
        except Exception as exc:
            self._log(f"Clear-memory transfer failed: {exc}")
            self._send_line("ABORT")
        finally:
            self.hex_send_in_progress = False

    def _send_line(self, line: str) -> None:
        self._send_raw(line + "\n")

    def _load_selected_hex_lines(self) -> tuple[str, list[str]]:
        if self.firmware_source_var.get() == "github":
            blob_url = self.github_url_var.get().strip()
            if not blob_url:
                raise RuntimeError("GitHub HEX URL is empty")
            if not self.cached_github_hex_lines or self.cached_github_hex_url != blob_url:
                self._refresh_github_cache(force_download=True)
            if not self.cached_github_hex_lines:
                raise RuntimeError("GitHub HEX is not cached yet")
            source_name = f"{blob_url} @ {self.cached_github_hex_hash or 'unknown'}"
            return (source_name, list(self.cached_github_hex_lines))

        if not self.hex_path or not self.hex_path.exists():
            raise FileNotFoundError("No local firmware file is selected")

        with self.hex_path.open("r", encoding="utf-8") as handle:
            lines = [raw_line.strip() for raw_line in handle if raw_line.strip()]
        return (self.hex_path.name, lines)

    def _send_raw(self, payload: str) -> None:
        with self.serial_lock:
            if not self.serial_conn or not self.serial_conn.is_open:
                return
            try:
                self.serial_conn.write(payload.encode("ascii", errors="ignore"))
                self.serial_conn.flush()
            except Exception:
                self._drop_connection()

    def _discovery_loop(self) -> None:
        while self.running:
            if self.serial_conn and self.serial_conn.is_open:
                time.sleep(1.0)
                continue

            found = False
            for port in list_ports.comports():
                if not self.running:
                    return
                try:
                    ser = serial.Serial(port.device, 9600, timeout=0.25, write_timeout=1)
                    time.sleep(1.8)
                    hello_seen = False
                    deadline = time.time() + 2.0
                    while time.time() < deadline:
                        raw = ser.readline()
                        if not raw:
                            continue
                        line = raw.decode("utf-8", errors="ignore").strip()
                        if line.startswith("HELLO ARDUINO_TOASTER"):
                            hello_seen = True
                            break
                    if not hello_seen:
                        ser.close()
                        continue

                    self.serial_conn = ser
                    self.reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
                    self.reader_thread.start()
                    self.event_queue.put(("connected", port.device))
                    found = True
                    break
                except Exception:
                    continue

            if not found:
                time.sleep(2.0)

    def _reader_loop(self) -> None:
        while self.running:
            with self.serial_lock:
                ser = self.serial_conn
            if not ser or not ser.is_open:
                return
            try:
                raw = ser.readline()
                if not raw:
                    continue
                line = raw.decode("utf-8", errors="ignore").strip()
                self.event_queue.put(("line", line))
            except Exception:
                self._drop_connection()
                return

    def _drop_connection(self) -> None:
        with self.serial_lock:
            if self.serial_conn:
                try:
                    self.serial_conn.close()
                except Exception:
                    pass
            self.serial_conn = None
        self.event_queue.put(("disconnected", None))

    def _force_disconnect(self) -> None:
        self._drop_connection()

    def _update_pin_display(self, pin_name: str, mode: str, raw_value: str) -> None:
        pin = self.pin_vars[pin_name]
        pin["mode"].set(mode)
        if mode == "ADC":
            pin["value"].set("")
            pin["adc"].set(raw_value)
            self.pin_value_labels[pin_name].configure(fg="#666666")
            self.pin_adc_labels[pin_name].configure(fg="#1f1f1f")
            return

        pin["adc"].set("")
        pin["value"].set(raw_value)
        is_true = raw_value == "HIGH"
        self.pin_value_labels[pin_name].configure(fg="#1a7f37" if is_true else "#b42318")
        self.pin_adc_labels[pin_name].configure(fg="#666666")

    def _reset_pins(self) -> None:
        for pin_name in self.pin_vars:
            self.pin_vars[pin_name]["mode"].set("-")
            self.pin_vars[pin_name]["value"].set("-")
            self.pin_vars[pin_name]["adc"].set("")
            self.pin_value_labels[pin_name].configure(fg="#666666")
            self.pin_adc_labels[pin_name].configure(fg="#666666")

    def _log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _refresh_github_hash(self) -> None:
        if self.github_refresh_in_progress:
            return
        self.github_refresh_in_progress = True
        self.github_hash_var.set("Git hash: loading...")
        threading.Thread(target=self._refresh_github_hash_worker, daemon=True).start()

    def _refresh_github_hash_worker(self) -> None:
        try:
            self._refresh_github_cache(force_download=False)
        except Exception as exc:
            self.root.after(0, lambda: self.github_hash_var.set(f"Git hash: error ({exc})"))
        finally:
            self.root.after(0, self._finish_github_hash_refresh)

    def _finish_github_hash_refresh(self) -> None:
        self.github_refresh_in_progress = False

    def _close(self) -> None:
        self.running = False
        self._drop_connection()
        self.root.destroy()

    def _download_github_hex_lines(self, blob_url: str) -> list[str]:
        raw_url = self._github_blob_to_raw_url(blob_url)
        request = Request(raw_url, headers={"User-Agent": HTTP_USER_AGENT})
        try:
            with urlopen(request, timeout=15) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            raise RuntimeError(f"GitHub HEX download failed: HTTP {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError(f"GitHub HEX download failed: {exc.reason}") from exc

        lines = [line.strip() for line in body.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError("GitHub HEX file was empty")
        return lines

    def _refresh_github_cache(self, force_download: bool) -> None:
        blob_url = self.github_url_var.get().strip()
        if not blob_url:
            raise RuntimeError("GitHub HEX URL is empty")

        commit_hash = self._fetch_github_commit_hash(blob_url)
        needs_download = (
            force_download
            or not self.cached_github_hex_lines
            or self.cached_github_hex_hash != commit_hash
            or self.cached_github_hex_url != blob_url
        )

        if needs_download:
            lines = self._download_github_hex_lines(blob_url)
            self.cached_github_hex_lines = lines
            self.cached_github_hex_hash = commit_hash
            self.cached_github_hex_url = blob_url
            self.root.after(0, lambda: self._log(f"Cached GitHub firmware: {commit_hash}"))
        else:
            self.root.after(0, lambda: self._log(f"GitHub firmware unchanged: {commit_hash}"))

        self.root.after(0, lambda: self.github_hash_var.set(f"Git hash: {commit_hash}"))

    def _fetch_github_commit_hash(self, blob_url: str) -> str:
        owner, repo, ref, _ = self._parse_github_blob_url(blob_url)
        api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{ref}"
        request = Request(api_url, headers={"User-Agent": HTTP_USER_AGENT, "Accept": "application/vnd.github+json"})
        try:
            with urlopen(request, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise RuntimeError(f"HTTP {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError(str(exc.reason)) from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError("invalid JSON") from exc

        sha = payload.get("sha")
        if not isinstance(sha, str) or not sha:
            raise RuntimeError("missing sha")
        return sha[:12]

    def _github_blob_to_raw_url(self, blob_url: str) -> str:
        owner, repo, ref, repo_path = self._parse_github_blob_url(blob_url)
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{repo_path}"

    def _parse_github_blob_url(self, blob_url: str) -> tuple[str, str, str, str]:
        parsed = urlparse(blob_url)
        if parsed.netloc not in {"github.com", "www.github.com"}:
            raise RuntimeError("URL must point to github.com")

        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 5 or parts[2] != "blob":
            raise RuntimeError("URL must look like github.com/<owner>/<repo>/blob/<ref>/<path>")

        owner = parts[0]
        repo = parts[1]
        ref = parts[3]
        repo_path = "/".join(parts[4:])
        if not repo_path.lower().endswith(".hex"):
            raise RuntimeError("GitHub URL must point to a .hex file")
        return (owner, repo, ref, repo_path)


def main() -> None:
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    ToasterGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
