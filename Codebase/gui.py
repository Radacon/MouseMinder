from __future__ import annotations

import queue
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

import serial
from serial.tools import list_ports

DEFAULT_HEX_PATH = Path(r"C:\Users\robot\Documents\Atmel Studio\7.0\MouseMinder\MouseMinder\Debug\MouseMinder.hex")


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

        self.connection_var = tk.StringVar(value="Disconnected")
        self.state_var = tk.StringVar(value="WAIT_GUI")
        self.device_var = tk.StringVar(value="")
        self.chip_id_var = tk.StringVar(value="")
        self.prompt_var = tk.StringVar(value="Waiting for operator input.")
        self.hex_var = tk.StringVar(value="No file selected")
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
        ttk.Label(file_frame, textvariable=self.hex_var).pack(anchor="w")
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
        if not self.hex_path or not self.hex_path.exists():
            self._log("Hex requested but no firmware file is selected")
            self._send_line("ABORT")
            return

        self.hex_send_in_progress = True
        threading.Thread(target=self._send_hex_file, daemon=True).start()

    def _send_hex_file(self) -> None:
        try:
            self._log(f"Sending firmware: {self.hex_path.name}")
            with self.hex_path.open("r", encoding="utf-8") as handle:
                for raw_line in handle:
                    line = raw_line.strip()
                    if not line:
                        continue
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

    def _close(self) -> None:
        self.running = False
        self._drop_connection()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    ToasterGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
