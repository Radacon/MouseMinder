# Codebase Guide

## Current production code

- `VSCODE_FreePDK/` — PMS150C firmware built with SDCC and the Free PDK headers
- `MouseMinderProgrammer/` — local Easy PDK production programmer
- `MouseMinderProgrammerWeb/` — browser-based Easy PDK production station

Start with `VSCODE_FreePDK/main.c` and `VSCODE_FreePDK/Makefile`. The [project README](../README.md#revision-history) summarizes hardware and software revisions.

See the [Free PDK project](https://free-pdk.github.io/), [Easy PDK programmer hardware](https://github.com/free-pdk/easy-pdk-programmer-hardware), and [Easy PDK programmer software](https://github.com/free-pdk/easy-pdk-programmer-software) for the upstream open-source toolchain.

## Prototype tools

`AtmelStudio/` contains the early AVR firmware. `ardu_tiny_toaster.ino`, `tiny10_base_code.ino`, `gui.py`, and `requirements.txt` cover the Arduino TPI programming fixture and its operator interface.
