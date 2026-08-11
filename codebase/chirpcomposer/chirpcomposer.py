"""MouseMinder chirp composer and Arduino playback controller."""

from __future__ import annotations

import json
import queue
import threading
import tkinter as tk
from dataclasses import asdict, dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    import serial
    from serial.tools import list_ports
except ImportError as exc:  # Give a useful error instead of failing mysteriously.
    raise SystemExit("pyserial is required: python -m pip install pyserial") from exc


BAUDRATE = 115200
MAX_STEPS = 128
DEFAULT_MASTER_CLOCK_HZ = 52_000
DEFAULT_CLOCK_DIVIDER = 1
ARDUINO_MAX_FREQUENCY_HZ = 65_535
MAX_TIMER_DIVISOR = 255
MAX_EXPORT_DURATION_MS = 65_535


@dataclass
class Step:
    frequency_hz: int
    duration_ms: int

    @property
    def description(self) -> str:
        sound = "Rest" if self.frequency_hz == 0 else f"{self.frequency_hz} Hz"
        return f"{sound} for {self.duration_ms} ms"


class ChirpComposer:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MouseMinder Chirp Composer")
        self.root.geometry("860x680")

        self.steps: list[Step] = []
        self.connection: serial.Serial | None = None
        self.reader: threading.Thread | None = None
        self.events: queue.Queue[tuple[str, str]] = queue.Queue()
        self.closing = False

        self.port_var = tk.StringVar()
        self.connection_var = tk.StringVar(value="Disconnected")
        self.frequency_var = tk.StringVar(value="2000")
        self.duration_var = tk.StringVar(value="250")
        self.master_clock_var = tk.StringVar(value=str(DEFAULT_MASTER_CLOCK_HZ))
        self.divider_var = tk.StringVar(value=str(DEFAULT_CLOCK_DIVIDER))
        self.limit_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()
        self._refresh_ports()
        self._update_limit()
        self.root.after(50, self._pump_events)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=12)
        outer.pack(fill="both", expand=True)

        connection = ttk.LabelFrame(outer, text="Arduino Uno", padding=10)
        connection.pack(fill="x")
        self.port_box = ttk.Combobox(connection, textvariable=self.port_var, state="readonly", width=35)
        self.port_box.pack(side="left")
        ttk.Button(connection, text="Refresh", command=self._refresh_ports).pack(side="left", padx=6)
        self.connect_button = ttk.Button(connection, text="Connect", command=self._toggle_connection)
        self.connect_button.pack(side="left")
        ttk.Label(connection, textvariable=self.connection_var).pack(side="left", padx=12)

        clock = ttk.LabelFrame(outer, text="PMS150 clock limit", padding=10)
        clock.pack(fill="x", pady=(10, 0))
        ttk.Label(clock, text="Master clock (Hz)").grid(row=0, column=0, sticky="w")
        ttk.Entry(clock, textvariable=self.master_clock_var, width=14).grid(row=0, column=1, padx=(6, 16))
        ttk.Label(clock, text="Timer divider").grid(row=0, column=2, sticky="w")
        ttk.Entry(clock, textvariable=self.divider_var, width=8).grid(row=0, column=3, padx=(6, 16))
        ttk.Button(clock, text="Apply", command=self._update_limit).grid(row=0, column=4)
        ttk.Label(clock, textvariable=self.limit_var).grid(row=1, column=0, columnspan=5, sticky="w", pady=(6, 0))

        editor = ttk.LabelFrame(outer, text="Add step", padding=10)
        editor.pack(fill="x", pady=(10, 0))
        ttk.Label(editor, text="Frequency (Hz, 0 = rest)").grid(row=0, column=0, sticky="w")
        ttk.Entry(editor, textvariable=self.frequency_var, width=14).grid(row=1, column=0, sticky="w")
        ttk.Label(editor, text="Duration (ms)").grid(row=0, column=1, sticky="w", padx=(16, 0))
        ttk.Entry(editor, textvariable=self.duration_var, width=14).grid(row=1, column=1, sticky="w", padx=(16, 0))
        ttk.Button(editor, text="Add tone", command=self._add_step).grid(row=1, column=2, padx=(16, 4))
        ttk.Button(editor, text="Add rest", command=lambda: self._add_step(rest=True)).grid(row=1, column=3, padx=4)
        ttk.Button(editor, text="Update selected", command=self._update_selected).grid(row=1, column=4, padx=(4, 0))

        sequence = ttk.LabelFrame(outer, text="Sequence", padding=10)
        sequence.pack(fill="both", expand=True, pady=(10, 0))
        self.sequence_table = ttk.Treeview(
            sequence,
            columns=("requested", "snapped", "duration"),
            show="tree headings",
            selectmode="extended",
            height=14,
        )
        self.sequence_table.heading("#0", text="Step")
        self.sequence_table.heading("requested", text="Requested frequency (Hz)")
        self.sequence_table.heading("snapped", text="Snapped frequency (Hz)")
        self.sequence_table.heading("duration", text="Duration (ms)")
        self.sequence_table.column("#0", width=55, stretch=False, anchor="center")
        self.sequence_table.column("requested", width=175, anchor="center")
        self.sequence_table.column("snapped", width=175, anchor="center")
        self.sequence_table.column("duration", width=120, anchor="center")
        self.sequence_table.pack(side="left", fill="both", expand=True)
        self.sequence_table.bind("<<TreeviewSelect>>", self._load_selected_step)
        self.sequence_table.bind("<Double-Button-1>", self._begin_cell_edit)
        scrollbar = ttk.Scrollbar(sequence, command=self.sequence_table.yview)
        scrollbar.pack(side="left", fill="y")
        self.sequence_table.configure(yscrollcommand=scrollbar.set)
        tools = ttk.Frame(sequence)
        tools.pack(side="left", fill="y", padx=(10, 0))
        ttk.Button(tools, text="Move up", command=lambda: self._move(-1)).pack(fill="x")
        ttk.Button(tools, text="Move down", command=lambda: self._move(1)).pack(fill="x", pady=4)
        ttk.Button(tools, text="Remove", command=self._remove).pack(fill="x")
        ttk.Button(tools, text="Clear", command=self._clear).pack(fill="x", pady=4)
        ttk.Separator(tools).pack(fill="x", pady=8)
        ttk.Button(tools, text="Save…", command=self._save).pack(fill="x")
        ttk.Button(tools, text="Load…", command=self._load).pack(fill="x", pady=4)
        ttk.Button(tools, text="Export C header…", command=self._export_c_header).pack(fill="x")

        playback = ttk.LabelFrame(outer, text="Playback", padding=10)
        playback.pack(fill="x", pady=(10, 0))
        ttk.Button(playback, text="Play / Resume", command=self._play).pack(side="left")
        ttk.Button(
            playback,
            text="Play frequency-snapped",
            command=lambda: self._play(snapped=True),
        ).pack(side="left", padx=(6, 0))
        ttk.Button(playback, text="Pause", command=lambda: self._send("PAUSE")).pack(side="left", padx=6)
        ttk.Button(playback, text="Restart", command=lambda: self._send("RESTART")).pack(side="left")
        ttk.Button(playback, text="Stop", command=lambda: self._send("STOP")).pack(side="left", padx=6)
        ttk.Label(playback, textvariable=self.status_var).pack(side="right")

    def _maximum_frequency(self) -> int:
        clock = int(self.master_clock_var.get())
        divider = int(self.divider_var.get())
        if clock <= 0 or divider <= 0:
            raise ValueError
        # A square wave requires two timer ticks per complete cycle.
        return min(clock // (2 * divider), ARDUINO_MAX_FREQUENCY_HZ)

    def _update_limit(self) -> None:
        try:
            maximum = self._maximum_frequency()
        except ValueError:
            messagebox.showerror("Clock settings", "Clock and divider must be positive whole numbers.")
            return
        pms_limit = int(self.master_clock_var.get()) // (2 * int(self.divider_var.get()))
        reason = "PMS150 clock / 2 / divider" if pms_limit <= ARDUINO_MAX_FREQUENCY_HZ else "Arduino command limit"
        self.limit_var.set(f"Maximum buzzer frequency: {maximum:,} Hz ({reason})")
        if hasattr(self, "sequence_table"):
            self._redraw()

    def _snap_frequency(self, requested_hz: int) -> tuple[int, int | None]:
        """Return the nearest timer-derived frequency and its integer divisor."""
        if requested_hz == 0:
            return requested_hz, None
        clock = int(self.master_clock_var.get())
        timer_divider = int(self.divider_var.get())
        timer_base_hz = clock / (2 * timer_divider)
        ideal_divisor = timer_base_hz / requested_hz
        lower_divisor = min(MAX_TIMER_DIVISOR, max(1, int(ideal_divisor)))
        candidates = tuple(
            divisor
            for divisor in (lower_divisor, lower_divisor + 1)
            if divisor <= MAX_TIMER_DIVISOR
        )
        integer_divisor = min(
            candidates,
            key=lambda divisor: abs((timer_base_hz / divisor) - requested_hz),
        )
        snapped_hz = max(1, round(timer_base_hz / integer_divisor))
        return snapped_hz, integer_divisor

    def _add_step(self, rest: bool = False) -> None:
        if len(self.steps) >= MAX_STEPS:
            messagebox.showerror("Sequence full", f"The Arduino supports at most {MAX_STEPS} steps.")
            return
        try:
            frequency = 0 if rest else int(self.frequency_var.get())
            duration = int(self.duration_var.get())
            maximum = self._maximum_frequency()
        except ValueError:
            messagebox.showerror("Invalid step", "Frequency, duration, clock, and divider must be whole numbers.")
            return
        if frequency < 0 or frequency > maximum:
            messagebox.showerror("Invalid frequency", f"Frequency must be from 0 to {maximum:,} Hz.")
            return
        if not 1 <= duration <= 4_294_967_295:
            messagebox.showerror("Invalid duration", "Duration must be at least 1 ms.")
            return
        self.steps.append(Step(frequency, duration))
        self._redraw()

    def _redraw(self) -> None:
        selected = set(self.sequence_table.selection())
        self.sequence_table.delete(*self.sequence_table.get_children())
        for index, step in enumerate(self.steps):
            snapped, _integer_divisor = self._snap_frequency(step.frequency_hz)
            requested_text = "Rest" if step.frequency_hz == 0 else str(step.frequency_hz)
            snapped_text = "Rest" if snapped == 0 else str(snapped)
            iid = str(index)
            self.sequence_table.insert(
                "",
                tk.END,
                iid=iid,
                text=str(index + 1),
                values=(requested_text, snapped_text, step.duration_ms),
            )
            if iid in selected:
                self.sequence_table.selection_add(iid)

    def _selected_indices(self) -> list[int]:
        return sorted(int(iid) for iid in self.sequence_table.selection())

    def _load_selected_step(self, _event: tk.Event | None = None) -> None:
        selected = self._selected_indices()
        if len(selected) != 1:
            return
        step = self.steps[selected[0]]
        self.frequency_var.set(str(step.frequency_hz))
        self.duration_var.set(str(step.duration_ms))

    def _begin_cell_edit(self, event: tk.Event) -> None:
        row = self.sequence_table.identify_row(event.y)
        column = self.sequence_table.identify_column(event.x)
        if not row or column not in {"#1", "#3"}:
            if column == "#2":
                self.status_var.set("Snapped frequency is calculated and cannot be edited")
            return
        bounds = self.sequence_table.bbox(row, column)
        if not bounds:
            return
        x, y, width, height = bounds
        index = int(row)
        initial = str(self.steps[index].frequency_hz if column == "#1" else self.steps[index].duration_ms)
        editor = ttk.Entry(self.sequence_table)
        editor.insert(0, initial)
        editor.select_range(0, tk.END)
        editor.place(x=x, y=y, width=width, height=height)
        editor.focus_set()

        def commit(_event: tk.Event | None = None) -> None:
            if not editor.winfo_exists():
                return
            value = editor.get()
            editor.destroy()
            self._commit_cell_edit(index, column, value)

        editor.bind("<Return>", commit)
        editor.bind("<FocusOut>", commit)
        editor.bind("<Escape>", lambda _event: editor.destroy())

    def _commit_cell_edit(self, index: int, column: str, value: str) -> None:
        try:
            number = int(value)
            maximum = self._maximum_frequency()
        except ValueError:
            messagebox.showerror("Invalid value", "Table values must be whole numbers.")
            return
        step = self.steps[index]
        if column == "#1":
            if not 0 <= number <= maximum:
                messagebox.showerror("Invalid frequency", f"Frequency must be from 0 to {maximum:,} Hz.")
                return
            self.steps[index] = Step(number, step.duration_ms)
        else:
            if not 1 <= number <= 4_294_967_295:
                messagebox.showerror("Invalid duration", "Duration must be at least 1 ms.")
                return
            self.steps[index] = Step(step.frequency_hz, number)
        self._redraw()
        self.sequence_table.selection_set(str(index))
        self._load_selected_step()

    def _update_selected(self) -> None:
        selected = self._selected_indices()
        if len(selected) != 1:
            messagebox.showerror("Select a step", "Select exactly one tone or rest to update.")
            return
        try:
            frequency = int(self.frequency_var.get())
            duration = int(self.duration_var.get())
            maximum = self._maximum_frequency()
        except ValueError:
            messagebox.showerror("Invalid step", "Frequency and duration must be whole numbers.")
            return
        if not 0 <= frequency <= maximum:
            messagebox.showerror("Invalid frequency", f"Frequency must be from 0 to {maximum:,} Hz.")
            return
        if not 1 <= duration <= 4_294_967_295:
            messagebox.showerror("Invalid duration", "Duration must be at least 1 ms.")
            return
        index = selected[0]
        self.steps[index] = Step(frequency, duration)
        self._redraw()
        self.sequence_table.selection_set(str(index))
        self.sequence_table.focus(str(index))
        self.frequency_var.set(str(frequency))

    def _remove(self) -> None:
        for index in reversed(self._selected_indices()):
            del self.steps[index]
        self._redraw()

    def _clear(self) -> None:
        self.steps.clear()
        self._redraw()

    def _move(self, direction: int) -> None:
        selected = self._selected_indices()
        if len(selected) != 1:
            return
        old = selected[0]
        new = old + direction
        if not 0 <= new < len(self.steps):
            return
        self.steps[old], self.steps[new] = self.steps[new], self.steps[old]
        self._redraw()
        self.sequence_table.selection_set(str(new))
        self.sequence_table.focus(str(new))

    def _save(self) -> None:
        filename = filedialog.asksaveasfilename(defaultextension=".chirp.json", filetypes=[("Chirp sequence", "*.json")])
        if not filename:
            return
        data = {
            "format": "mouseminder-chirp-v1",
            "master_clock_hz": int(self.master_clock_var.get()),
            "clock_divider": int(self.divider_var.get()),
            "steps": [asdict(step) for step in self.steps],
        }
        Path(filename).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def _load(self) -> None:
        filename = filedialog.askopenfilename(filetypes=[("Chirp sequence", "*.json"), ("All files", "*.*")])
        if not filename:
            return
        try:
            data = json.loads(Path(filename).read_text(encoding="utf-8"))
            if data.get("format") != "mouseminder-chirp-v1":
                raise ValueError("unsupported file format")
            loaded = [Step(int(item["frequency_hz"]), int(item["duration_ms"])) for item in data["steps"]]
            if len(loaded) > MAX_STEPS:
                raise ValueError(f"more than {MAX_STEPS} steps")
            self.master_clock_var.set(str(int(data["master_clock_hz"])))
            self.divider_var.set(str(int(data["clock_divider"])))
            maximum = self._maximum_frequency()
            if any(s.frequency_hz < 0 or s.frequency_hz > maximum or s.duration_ms < 1 for s in loaded):
                raise ValueError("a step is outside the saved clock or duration limits")
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            messagebox.showerror("Could not load", str(exc))
            return
        self.steps = loaded
        self._update_limit()
        self._redraw()

    def _export_c_header(self) -> None:
        if not self.steps:
            messagebox.showerror("Empty sequence", "Add or load at least one step before exporting.")
            return
        if any(step.duration_ms > MAX_EXPORT_DURATION_MS for step in self.steps):
            messagebox.showerror(
                "Duration too long",
                f"Firmware export supports durations up to {MAX_EXPORT_DURATION_MS:,} ms per step.",
            )
            return

        default_dir = Path(__file__).resolve().parent.parent / "VSCODE_FreePDK"
        filename = filedialog.asksaveasfilename(
            title="Export firmware chirp header",
            initialdir=str(default_dir),
            initialfile="chirp_pattern.h",
            defaultextension=".h",
            filetypes=[("C header", "*.h"), ("All files", "*.*")],
        )
        if not filename:
            return

        data: list[int] = []
        comments: list[str] = []
        for index, step in enumerate(self.steps, 1):
            snapped_hz, divisor = self._snap_frequency(step.frequency_hz)
            encoded_divisor = divisor or 0
            data.extend((encoded_divisor, step.duration_ms & 0xFF, step.duration_ms >> 8))
            tone = "rest" if divisor is None else f"{snapped_hz} Hz (divisor {divisor})"
            comments.append(f"    {index:3}: {tone}, {step.duration_ms} ms")

        byte_rows = [
            "    " + ", ".join(f"0x{value:02X}" for value in data[offset : offset + 12]) + ","
            for offset in range(0, len(data), 12)
        ]
        header = "\n".join(
            [
                "/* Generated by MouseMinder Chirp Composer. Do not edit by hand. */",
                "#ifndef MOUSEMINDER_CHIRP_PATTERN_H",
                "#define MOUSEMINDER_CHIRP_PATTERN_H",
                "",
                "#include <stdint.h>",
                "",
                f"#define CHIRP_MASTER_CLOCK_HZ {int(self.master_clock_var.get())}UL",
                f"#define CHIRP_TIMER_DIVIDER {int(self.divider_var.get())}u",
                "#define CHIRP_STEP_BYTES 3u",
                f"#define CHIRP_STEP_COUNT {len(self.steps)}u",
                "",
                "/* Each step: timer divisor, duration LSB, duration MSB. Divisor 0 is rest. */",
                "static const uint8_t chirpPattern[CHIRP_STEP_COUNT * CHIRP_STEP_BYTES] =",
                "{",
                *byte_rows,
                "};",
                "",
                "/* Decoded steps:",
                *comments,
                " */",
                "",
                "#endif",
                "",
            ]
        )
        try:
            Path(filename).write_text(header, encoding="ascii")
        except OSError as exc:
            messagebox.showerror("Export failed", str(exc))
            return
        self.status_var.set(f"Exported {len(self.steps)} firmware steps to {Path(filename).name}")

    def _refresh_ports(self) -> None:
        port_info = list(list_ports.comports())
        ports = [port.device for port in port_info]
        self.port_box["values"] = ports
        if ports and self.port_var.get() not in ports:
            arduino = next(
                (
                    port.device
                    for port in port_info
                    if "arduino" in (port.description or "").lower()
                    or (port.vid, port.pid) == (0x2341, 0x0043)
                ),
                ports[0],
            )
            self.port_var.set(arduino)

    def _toggle_connection(self) -> None:
        if self.connection and self.connection.is_open:
            self._disconnect()
            return
        port = self.port_var.get()
        if not port:
            messagebox.showerror("No port", "Select an Arduino serial port first.")
            return
        try:
            self.connection = serial.Serial(port, BAUDRATE, timeout=0.2, write_timeout=1)
        except serial.SerialException as exc:
            details = str(exc)
            if "access is denied" in details.lower() or "permissionerror" in details.lower():
                details = (
                    f"Windows would not release {port}. Close Arduino Serial Monitor/Plotter, "
                    "PuTTY, PlatformIO monitors, and any other MouseMinder GUI, then try again.\n\n"
                    f"Technical details: {exc}"
                )
            messagebox.showerror("Connection failed", details)
            return
        self.connection_var.set(f"Connected to {port}")
        self.connect_button.configure(text="Disconnect")
        self.reader = threading.Thread(target=self._read_loop, daemon=True)
        self.reader.start()

    def _disconnect(self) -> None:
        connection, self.connection = self.connection, None
        if connection:
            try:
                connection.close()
            except serial.SerialException:
                pass
        self.connection_var.set("Disconnected")
        self.connect_button.configure(text="Connect")

    def _read_loop(self) -> None:
        connection = self.connection
        while not self.closing and connection is self.connection and connection and connection.is_open:
            try:
                line = connection.readline().decode("ascii", errors="replace").strip()
                if line:
                    self.events.put(("line", line))
            except (serial.SerialException, OSError) as exc:
                self.events.put(("error", str(exc)))
                return

    def _pump_events(self) -> None:
        try:
            while True:
                event, value = self.events.get_nowait()
                if event == "error":
                    self._disconnect()
                    self.status_var.set(f"Serial error: {value}")
                elif value.startswith("STATUS "):
                    self.status_var.set(value[7:].replace("_", " ").title())
                elif value.startswith("ERR "):
                    self.status_var.set(value)
                else:
                    self.status_var.set(value)
        except queue.Empty:
            pass
        if not self.closing:
            self.root.after(50, self._pump_events)

    def _send(self, command: str) -> bool:
        if not self.connection or not self.connection.is_open:
            messagebox.showerror("Not connected", "Connect to the Arduino first.")
            return False
        try:
            self.connection.write((command + "\n").encode("ascii"))
            self.connection.flush()
            return True
        except (serial.SerialException, OSError) as exc:
            self._disconnect()
            messagebox.showerror("Serial error", str(exc))
            return False

    def _play(self, snapped: bool = False) -> None:
        if not self.steps:
            messagebox.showerror("Empty sequence", "Add at least one tone or rest.")
            return
        if not self._send("CLEAR"):
            return
        changed = 0
        for step in self.steps:
            frequency = step.frequency_hz
            if snapped:
                frequency, _integer_divisor = self._snap_frequency(frequency)
                changed += frequency != step.frequency_hz
            if not self._send(f"ADD {frequency} {step.duration_ms}"):
                return
        self._send("PLAY")
        if snapped:
            self.status_var.set(f"Playing snapped sequence ({changed} tones adjusted)")

    def _close(self) -> None:
        self.closing = True
        self._disconnect()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    ChirpComposer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
