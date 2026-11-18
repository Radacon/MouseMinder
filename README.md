# MouseMinder

MouseMinder is a coin-cell-powered alarm for reusable mouse traps. The current hardware is built around a **Padauk PMS150C-U06**, not an ATtiny10. A piezo element serves as both the trap-event sensor and the audible sounder; the board also has a status LED and a pushbutton.

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

## Repository Layout

- `codebase/VSCODE_FreePDK/` — current PMS150C production firmware
- `codebase/MouseMinderProgrammer/` — current local production programmer UI
- `codebase/MouseMinderProgrammerWeb/` — Web Serial production station
- `pcb_design/` — KiCad source, fabrication history, and test hardware
- `mechanical_design/` — enclosure and accessory CAD exports
- `tools/` — release and engineering utilities
- `codebase/AtmelStudio/`, `codebase/ardu_tiny_toaster.ino`, `codebase/tiny10_base_code.ino`, and `codebase/gui.py` — archived ATtiny10-era prototype work; **not the current product architecture**

## Firmware Releases

Production firmware releases use tags named `firmware-vMAJOR.MINOR.PATCH` that point to commits already on `main`. The GitHub Actions workflow builds the PMS150C firmware and publishes:

- `slowclocksleep_PMS150C.bin`
- `slowclocksleep_PMS150C.bin.sha256`
- `mouseminder-firmware.json`

The manifest records the source commit, toolchain, PMS150C memory contract, calibration target, asset size, and SHA-256. Production programming still requires explicit operator approval and checksum verification.

## Legacy ATtiny10 Work

Early prototypes used an ATtiny10 and an Arduino Uno TPI fixture. Those files remain for design history and reference only. They must not be used to describe, build, or program current MouseMinder hardware.
