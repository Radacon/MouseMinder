# MouseMinder

MouseMinder is a coin-cell-powered alarm for reusable mouse traps, built around a **Padauk PMS150C-U06**. A piezo element serves as both the trap-event sensor and the audible sounder; the board also has a status LED and a pushbutton.

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

- **Early prototypes:** ATtiny10 with an Arduino Uno TPI programming fixture.
- **Rev 6 (August 2026):** PMS150C hardware with Free PDK/SDCC firmware and Easy PDK programming.
- **Rev 6.1 (October 2026):** rotated R1 for easier rework and updated the silkscreen.

### Software

- **Firmware v1.0.0 (October 2026):** introduced tagged releases with a binary, checksum, and build manifest.
- **Firmware v1.1.0 (October 2026):** reserved program memory for per-unit production metadata.
- **Subsequent development (October–November 2026):** added local and Web Serial programmer tools, presence/button/chirp QC, and updated ILRC startup to keep IHRC disabled.

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
