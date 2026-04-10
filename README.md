# MouseMinder

MouseMinder is a small ATtiny10-based hardware project with a matching programming and test fixture. This repository contains the KiCad source for the board itself, manufacturing outputs, Arduino-based fixture firmware, a Python operator GUI, and supporting test data.

## What Is In This Repo

- `MouseMinder/`
  - Main KiCad project for the MouseMinder PCB
  - 3D models, schematics, PCB layout, fabrication outputs, and production BOM/position files
  - `MouseMinder_Programmer/` contains the companion KiCad project for the programming fixture
- `Codebase/`
  - `ardu_tiny_toaster.ino`: Arduino Uno firmware for the programming and test fixture
  - `tiny10_base_code.ino`: base TPI programmer implementation for ATtiny4/5/9/10/20/40 devices
  - `gui.py`: desktop GUI for operators to select firmware, auto-discover the fixture over serial, and run the programming loop
  - `requirements.txt`: project notes describing the original GUI/fixture behavior
- `PowerProfilerData/`
  - Power measurements for ATtiny10 sleep behavior
- `Simulation/`
  - CSV exports from circuit/scope simulation work

## Hardware Overview

The main board centers on an `ATtiny10-TS` and includes:

- A coin-cell battery holder
- A buzzer
- An LED indicator
- Two pushbuttons
- A discrete power/latching section around `Q1`

Repository BOM files indicate this design is intended for assembled prototype or low-volume production runs, with both sourcing-oriented BOM exports and placement data included.

## Design Files

Primary design assets live under `MouseMinder/`:

- `MouseMinder.kicad_sch`
- `MouseMinder.kicad_pcb`
- `MouseMinder.step`
- `production/bom.csv`
- `production/*-pos.csv`
- `Fabs/` and `Fabs/R2JLC/` Gerber and drill outputs

There are also schematic PDFs for archived revisions, including `V3_JLC_SCH.pdf` and `V4_SCH.pdf`.

## Programming And Test Fixture

The fixture is built around an Arduino Uno and a desktop GUI.

The Arduino side:

- Speaks to the GUI over serial at `9600` baud
- Detects supported ATtiny devices over TPI
- Requests an Intel HEX image from the GUI
- Programs and verifies flash
- Performs a post-program battery/isolation check using analog measurements

The current fixture firmware maps:

- `D10` -> `!RST`
- `D11/D12` -> `TPIDATA`
- `D13` -> `TPICLK`
- `A0` -> `BATT`
- `A1` -> `LATCHED`

The operator GUI:

- Auto-discovers the Arduino fixture over available COM ports
- Displays connection state, detected chip ID, operator prompts, and `BATT` / `LATCHED` pin states
- Lets the operator select a `.hex` file
- Supports a clear-memory mode for erase/blank-check workflows

## Typical Workflow

1. Build or load the fixture firmware onto an Arduino Uno.
2. Launch the Python GUI from `Codebase/gui.py`.
3. Connect the programming fixture and target board.
4. Select the target `.hex` file, or use clear-memory mode.
5. Follow the GUI prompts while the fixture detects the device, programs it, verifies it, and checks battery isolation behavior.

## Running The GUI

Install the Python dependency manually, then run:

```powershell
pip install pyserial
python Codebase\gui.py
```

The GUI depends on:

- `pyserial`
- Python standard library `tkinter`

## Manufacturing Notes

For board fabrication or assembly handoff, start with:

- `MouseMinder/production/bom.csv`
- `MouseMinder/production/MouseMinder-top-pos.csv`
- `MouseMinder/production/MouseMinder-bottom-pos.csv`
- `MouseMinder/Fabs/` or `MouseMinder/Fabs/R2JLC/`

The repository also includes alternate BOM exports such as `qty50_MouseMinder_boM.csv` for sourcing and cost planning.

## Status

This repository appears to combine active hardware design work, production outputs, fixture firmware, and validation data in one place. If you are picking it up fresh, the fastest entry points are:

- `MouseMinder/MouseMinder.kicad_sch`
- `MouseMinder/MouseMinder.kicad_pcb`
- `Codebase/ardu_tiny_toaster.ino`
- `Codebase/gui.py`
