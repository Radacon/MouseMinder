# MouseMinder

MouseMinder is a small ATtiny10-based hardware project with a matching programming and test fixture. This repository combines the PCB design, fixture firmware, operator GUI, mechanical CAD exports, and simulation or validation data used to build and test the device.

## Repository Layout

- `codebase/`
  - Arduino Uno fixture firmware in `ardu_tiny_toaster.ino`
  - Base TPI programmer implementation in `tiny10_base_code.ino`
  - Operator desktop GUI in `gui.py`
  - Early or alternate device firmware work under `AtmelStudio/`
- `pcb_design/`
  - Main MouseMinder KiCad project files:
    - `MouseMinder.kicad_sch`
    - `MouseMinder.kicad_pcb`
    - `MouseMinder.kicad_pro`
  - Fixture or shield PCB design under `MouseMinder_Programmer_Shield/`
  - Archived KiCad backups under `MouseMinder-backups/`
  - Older release archives under `mouseminder_prev_versions/`
- `mechanical_design/`
  - Enclosure and trap body STEP exports under `trap_body/`
  - Accessory parts such as the battery isolator under `accessories/`
- `sim_and_test/`
  - Power profiling captures under `PowerProfilerData/`
  - Simulation exports under `Simulation/`

## Hardware Overview

The main board centers on an `ATtiny10-TS` and includes:

- A coin-cell battery holder
- A buzzer
- An LED indicator
- Two pushbuttons
- A discrete power or latching section around `Q1`

The repository also includes a separate programmer shield design and a fixture workflow for flashing and validating boards during bring-up or production.

## PCB Design Files

Primary electrical design assets live in `pcb_design/`:

- `MouseMinder.kicad_sch`
- `MouseMinder.kicad_pcb`
- `MouseMinder.kicad_pro`

Related hardware history is split out into:

- `pcb_design/MouseMinder_Programmer_Shield/` for the programming fixture PCB
- `pcb_design/MouseMinder-backups/` for KiCad backup archives
- `pcb_design/mouseminder_prev_versions/` for older packaged revisions

## Firmware And GUI

The programming and test fixture is built around an Arduino Uno and a Python desktop GUI.

Arduino-side files in `codebase/`:

- `ardu_tiny_toaster.ino`: fixture control firmware
- `tiny10_base_code.ino`: base TPI programming support for ATtiny4/5/9/10/20/40 devices

Desktop-side files in `codebase/`:

- `gui.py`: operator GUI for selecting firmware, discovering the fixture over serial, and running the programming loop
- `requirements.txt`: original behavior notes for the GUI and fixture

There is also an Atmel Studio project under `codebase/AtmelStudio/MouseMinder/` with a `main.c` firmware entry point and generated debug outputs.

## Fixture I/O Mapping

The current fixture firmware uses:

- `D10` -> `!RST`
- `D11/D12` -> `TPIDATA`
- `D13` -> `TPICLK`
- `A0` -> `BATT`
- `A1` -> `LATCHED`

The operator GUI is intended to:

- Auto-discover the Arduino fixture over available COM ports
- Show connection and pin-state information
- Let the operator select a `.hex` file
- Run the detect, program, verify, and test loop

## Mechanical Assets

Mechanical CAD exports are grouped under `mechanical_design/`:

- `trap_body/` contains enclosure and body STEP files, including lid and clip geometry
- `accessories/` contains supporting parts such as `Battery_Isolator_debossed.STEP`

## Simulation And Validation Data

Supporting measurement and simulation files live in `sim_and_test/`:

- `PowerProfilerData/` contains sleep-current or power measurement CSV files
- `Simulation/` contains scope and waveform export data from circuit simulation work

## Typical Workflow

1. Open the main hardware in `pcb_design/MouseMinder.kicad_sch` and `pcb_design/MouseMinder.kicad_pcb`.
2. Load the Arduino fixture firmware from `codebase/ardu_tiny_toaster.ino`.
3. Launch the operator GUI from `codebase/gui.py`.
4. Connect the programming fixture and target board.
5. Select a target `.hex` file and run the programming and test cycle.

## Running The GUI

Install the required Python package, then launch the GUI:

```powershell
pip install pyserial
python codebase\gui.py
```

The GUI depends on:

- `pyserial`
- Python standard library `tkinter`

## Fastest Entry Points

If you are picking up the project fresh, start with:

- `pcb_design/MouseMinder.kicad_sch`
- `pcb_design/MouseMinder.kicad_pcb`
- `codebase/ardu_tiny_toaster.ino`
- `codebase/gui.py`
