# Codebase Guide

## Current production code

- `VSCODE_FreePDK/` — PMS150C firmware built with SDCC and the Free PDK headers
- `MouseMinderProgrammer/` — local Easy PDK production programmer
- `MouseMinderProgrammerWeb/` — browser-based Easy PDK production station

The sellable Rev 6.1 hardware uses a Padauk PMS150C-U06. Start with `VSCODE_FreePDK/main.c` and `VSCODE_FreePDK/Makefile`.

See the [Free PDK project](https://free-pdk.github.io/), [Easy PDK programmer hardware](https://github.com/free-pdk/easy-pdk-programmer-hardware), and [Easy PDK programmer software](https://github.com/free-pdk/easy-pdk-programmer-software) for the upstream open-source toolchain.

## Archived prototype code

`AtmelStudio/`, `ardu_tiny_toaster.ino`, `tiny10_base_code.ino`, `gui.py`, and `requirements.txt` belong to the earlier ATtiny10/Arduino TPI prototype. They are retained for history only and are not compatible with the current PMS150C production hardware.
