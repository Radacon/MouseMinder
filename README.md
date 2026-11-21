# MouseMinder

MouseMinder is a coin-cell-powered alarm to extend the lifespan of mouse traps, built around a **Padauk PMS150C-U06**. A piezo element serves as both the trap-event sensor and the audible sounder; the board also has a status LED and a pushbutton.

It clips onto a trap and chirps and flashes after detecting the sharp vibration of the trap firing. The goal is to make a sprung trap easier to find and check, using a replaceable CR2032 and a small, reusable sensor. Operation is entirely local, with no app, radio, hub, or subscription.

## How It Works

While waiting for a trigger, the microcontroller sleeps and the piezo acts as a vibration sensor. A trap firing produces a voltage pulse that wakes the controller. The firmware then uses that same piezo to play the alert, switching its pin between sensing and sound output.

The alert repeats until the button is pressed: a brief LED flash roughly once a second, with a two-tone chirp after every fifth flash. Pressing the button silences the alert and returns the sensor to its quiet, armed state. Pressing it while armed starts the alert for testing.

Mounting matters: the sensor needs to move with the trap, and unrelated impacts or vibration can trigger it. Inspect the trap to confirm a catch. Choose a position where the chirp can be heard or the LED seen.

## Using MouseMinder

1. **Mount it:** attach the snap-trap clip to a compatible wooden spring trap, or use the zip-tie mount for another suitable setup. Keep the sensor and mount clear of the trigger and moving bar.
2. **Power it:** remove the battery-isolator tab completely. The sensor starts its chirp-and-flash alert.
3. **Set and arm:** set the trap following its manufacturer's instructions, then press the MouseMinder button to silence it. The quiet sensor is waiting for a trigger.
4. **Check an alert:** inspect the trap and press the button to silence the sensor. Setting or moving the trap may trigger it again; finish by returning it to the quiet waiting state.
5. **Test it:** press the button while the sensor is quiet to test the alert, then press again to silence it. To check the complete setup, safely fire an empty trap with a suitable tool while keeping hands clear, confirm the alert, and reset it.
6. **Replace the battery:** use a CR2032 with the polarity shown in the holder and securely close the battery compartment. Keep sensors and coin batteries away from children.

The snap-trap clip is intended for common wooden spring traps. Other traps need a suitable mounting arrangement that securely couples the sensor to the trap. See the [illustrated setup guide](https://www.mouseminder.com/index.php/setup/) for mounting examples and troubleshooting.

## Current Hardware

| Item | Current implementation |
|---|---|
| PCB revision | Rev 6.1 (October 2026) |
| Microcontroller | Padauk PMS150C-U06, one-time programmable (OTP) |
| Power | CR2032 coin cell |
| Event sensing / sound | Piezo element on PA3 |
| Status LED | PA4, active high |
| Pushbutton | PA6, externally pulled low; switch connects to VDD |
| Production clock | Calibrated 52 kHz ILRC; IHRC remains disabled |

The authoritative electrical design is:

- `pcb_design/MouseMinder.kicad_sch`
- `pcb_design/MouseMinder.kicad_pcb`
- `pcb_design/MouseMinder.kicad_pro`

## Firmware and Free PDK

Production firmware lives in [`codebase/VSCODE_FreePDK`](codebase/VSCODE_FreePDK). It targets the PMS150C `pdk13` architecture and is compiled with SDCC.

This work depends on the open-source [Free PDK project](https://free-pdk.github.io/), including its [PDK device headers](https://github.com/free-pdk/pdk-includes), [Easy PDK headers](https://github.com/free-pdk/easy-pdk-includes), and Easy PDK programming ecosystem. Free PDK makes it practical to build and program Padauk devices with an open toolchain.

Build the current firmware from a shell with SDCC, `make`, `makebin`, and `gawk` installed:

```sh
make -C codebase/VSCODE_FreePDK clean build
```

The build produces `slowclocksleep_PMS150C.ihx` and `slowclocksleep_PMS150C.bin` under `codebase/VSCODE_FreePDK/.output/`.

> **OTP warning:** the PMS150C cannot be erased. Programming a device is irreversible.

## Programming

The current production path uses the open-source Easy PDK programmer:

- [Easy PDK programmer hardware](https://github.com/free-pdk/easy-pdk-programmer-hardware)
- [Easy PDK programmer software](https://github.com/free-pdk/easy-pdk-programmer-software)
- Local production utility: [`codebase/MouseMinderProgrammer`](codebase/MouseMinderProgrammer)
- Browser-based production station: [`codebase/MouseMinderProgrammerWeb`](codebase/MouseMinderProgrammerWeb)

The local programmer uses the PMS150C target, the current `.ihx` firmware, and an explicit confirmation before writing, calibration, and verification.

## Revision History

### Hardware

- **First prototypes:** explored a piezo-triggered, coin-cell alarm with discrete MOSFET sensing and power-latching circuitry around an ATtiny10. The original goals were a replaceable battery, repeatable test/reset controls, and an alert that could run for at least a week.
- **Revisions 2-3:** developed the shared piezo sensor/sounder. Tap tests, trap tests, and oscilloscope measurements showed how the sensing network loaded the piezo; resistor and capacitor changes improved sensitivity while retaining useful sound output.
- **Spring 2026 beta run:** ordered a first batch of 50 units. Power profiling led to resistor changes and deeper firmware sleep. Further experiments connected the piezo to the microcontroller's wake input, simplifying the discrete sensing/latching circuit. An Arduino Uno TPI fixture supported programming and test work.
- **July 2026 redesign:** feedback from the beta run focused the next version on lower cost, a smaller enclosure, and one button. Bench prototypes moved to the PMS150C with Free PDK/SDCC and Easy PDK programming, using the controller's low-power sleep modes for the armed state.
- **August-September 2026 / Rev 6:** refined decoupling, the battery holder, and in-circuit programming. The piezo and LED share programming pins; measurements exposed short clock pulses and signal loading. Easy PDK timing changes added settling time and maintained a 50% clock duty cycle. Revised sample boards ordered in August programmed successfully in September.
- **October 2026 / Rev 6.1:** rotated R1 for easier rework and updated the silkscreen and component sourcing. Panelization reduced assembly overhead for a 200-board order. Enclosure work refined the clip fit and reinforced printed lettering after experiments with recessed text and solid color layers.

### Software

- **Early AVR firmware:** implemented the chirp/flash pattern on the ATtiny10, then replaced busy waits with sleep between events. The Arduino fixture and Python GUI provided a serial programming and test workflow.
- **July-August 2026 PMS150C port:** carried the alert behavior into the Free PDK/SDCC toolchain, with GPIO wake, Timer16 sleep intervals, and Timer2 piezo tones. Programming work also addressed piezo capacitance, clock pulse width, and data/clock settling time in Easy PDK.
- **Firmware v1.0.0 (October 2026):** introduced tagged releases with a binary, checksum, and build manifest.
- **Firmware v1.1.0 (October 2026):** reserved program memory for per-unit production metadata.
- **October-November 2026 tooling:** added local and Web Serial programmer interfaces, unit history, stable board-presence detection, and button/LED/chirp quality checks. The latest firmware source also keeps the high-speed oscillator disabled during startup.

## Repository Layout

- `codebase/VSCODE_FreePDK/` — current PMS150C production firmware
- `codebase/MouseMinderProgrammer/` — current local production programmer UI
- `codebase/MouseMinderProgrammerWeb/` — Web Serial production station
- `pcb_design/` — KiCad source, fabrication history, and test hardware
- `mechanical_design/` — enclosure and accessory CAD exports
- `tools/` — release and engineering utilities
- `codebase/AtmelStudio/`, `codebase/ardu_tiny_toaster.ino`, `codebase/tiny10_base_code.ino`, and `codebase/gui.py` — prototype AVR firmware and Arduino TPI fixture tools

## Firmware Releases

Production firmware releases use tags named `firmware-vMAJOR.MINOR.PATCH` that point to commits already on `main`. The GitHub Actions workflow builds the PMS150C firmware and publishes:

- `slowclocksleep_PMS150C.bin`
- `slowclocksleep_PMS150C.bin.sha256`
- `mouseminder-firmware.json`

The manifest records the source commit, toolchain, PMS150C memory contract, calibration target, asset size, and SHA-256. Production programming still requires explicit operator approval and checksum verification.
