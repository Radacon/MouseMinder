# MouseMinder Programmer

Double-click `Launch MouseMinder Programmer.cmd`.

The app uses the existing production settings and standard firmware:

- IC: PMS150C
- programming frequency: 10 kHz
- phase: 20 us
- firmware: `..\VSCODE_FreePDK\.output\slowclocksleep_PMS150C.ihx`

`Check Programmer / PCB` runs a non-writing probe. `PROGRAM FIRMWARE` asks for confirmation, then writes, calibrates, and verifies through `easypdkprog.exe`.

PMS150C is OTP: a programmed chip cannot be erased and reused.
