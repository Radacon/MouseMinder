# Building and flashing Easy PDK Programmer

The host program and programmer firmware must be updated together because the
timing-control command uses protocol 1.4.

## Required tools

- GNU Make and a C compiler (`gcc`) for the host application
- MinGW-w64 GCC when producing `easypdkprog.exe` on Windows
- GNU Arm Embedded GCC (`arm-none-eabi-gcc`, `objcopy`, and `size`) for firmware
- `dfu-suffix` to package the DFU image
- `dfu-util` to upload it

Use an MSYS2/MinGW shell for a native Windows `.exe`, or build the host in WSL
for a Linux executable. The ARM firmware can be built in either environment as
long as the ARM tools are on `PATH`.

## Build

From the repository root:

```sh
make clean
make
make firmware
```

Or build both artifacts with:

```sh
make release
```

Artifacts:

- `easypdkprog.exe` (MinGW) or `easypdkprog` (Linux)
- `Firmware/source/build/EASYPDKPROG.bin`
- `Firmware/source/build/EASYPDKPROG.dfu`

If the ARM compiler is installed outside `PATH`, pass its `bin` directory:

```sh
make -C Firmware/source GCC_PATH=/path/to/arm-gnu-toolchain/bin
```

## Flash firmware over USB DFU

1. Unplug the programmer.
2. Hold its button while reconnecting USB.
3. Release the button after USB is connected.
4. From the repository root, run:

```sh
make flash-firmware
```

The equivalent direct command is:

```sh
dfu-util -d 0483:df11 -a "@Internal Flash  /0x08000000/064*0002Kg" --dfuse-address 0x08000000 -D Firmware/source/build/EASYPDKPROG.dfu
```

Unplug and reconnect normally after the upload.

## Timing controls

The defaults are a 25 kHz programming clock and a +10 us phase:

```sh
easypdkprog.exe --frequency 25000 --phase 10 -n PMS150C write program.ihx
```

`--phase N` has these meanings:

- Transmit, positive: change DATA, wait `N` us, then raise CLOCK.
- Receive, positive: raise CLOCK, wait `N` us, then sample DATA.
- Transmit, negative: raise CLOCK, wait `abs(N)` us, then change DATA.
- Receive, negative: sample DATA, wait `abs(N)` us, then raise CLOCK.

The serial clock uses a frequency-scaled 50% duty cycle. The absolute phase
must fit inside each half-cycle. Firmware accepts 1 through 500000 Hz. Periods
are quantized to whole microseconds; GPIO and loop overhead add a small
hardware-dependent error, so confirm the final waveform with an oscilloscope
when precise timing matters.

Use `-v` to confirm the values sent to the programmer. Example:

```sh
easypdkprog.exe -v --frequency 10000 --phase 30 -n PMS150C read dump.ihx
```
