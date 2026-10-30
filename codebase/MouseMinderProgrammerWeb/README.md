# MouseMinder Programmer Web

A self-hosted production station for the Easy PDK Programmer and PMS150C. Chrome talks directly to the programmer over Web Serial; the Node server only serves the app, standard firmware, and JSON programming history.

## Run on this PC

Requires Node.js 20+ and desktop Google Chrome.

```powershell
cd project-source\codebase\MouseMinderProgrammerWeb
npm start
```

Open <http://localhost:8787>, connect the Easy PDK Programmer, and select its COM port when Chrome asks.

## What it does

- loads the bundled standard `slowclocksleep_PMS150C.ihx`
- uses the existing 10 kHz / 20 us programming timing
- probes and confirms a PMS150C target
- blank-checks before the irreversible OTP write
- programs, verifies, performs the 52 kHz ILRC calibration at 2.8 V, and writes the calibration result
- reads a target back to a downloadable Intel HEX file
- displays the complete 2,048-byte readback as an addressed hex dump
- embeds and decodes unit number, programming time, firmware Git hash, and notes with CRC-16 protection
- records successes and failures in `data/programming-log.json`

The serial implementation follows Easy PDK protocol 1.4 at 115200 baud. The browser performs all hardware I/O; the server never needs the USB programmer passed into its container.

## PMS150C metadata layout

During programming, the station adds a self-loop immediately after the compiled application, then stores metadata in the following words. A second self-loop remains fixed at word `0x3F5`; words `0x3F6` through `0x3FF` stay excluded by the PMS150C definition. The available note capacity is recalculated from the loaded firmware size, so a larger application automatically gets a smaller limit.

Metadata uses one byte per 13-bit program word and contains an `MMP2` marker, format version, length, flags, CRC-16, 9-digit unit number, UTC programming timestamp, 16-hex-digit Git identifier, and UTF-8 notes. The current standard firmware leaves 538 note bytes. The input enforces the calculated byte limit while typing, including multi-byte characters. Readback also supports the earlier `MMP1` layout.

The guards prevent normal sequential execution from entering metadata; they are not protection against corrupted or deliberately redirected control flow.

## TrueNAS / Docker

```powershell
docker compose up -d --build
```

Persist `./data` as a writable dataset. The container runs as UID/GID 1000 and listens on port 8787.

Web Serial requires a secure browser context. `http://localhost:8787` works locally, but a page opened from a TrueNAS hostname or LAN IP must be served through **HTTPS with a certificate Chrome trusts**. Put this container behind the TrueNAS HTTPS reverse proxy, then use Chrome on the workstation physically connected to the programmer.

Keep the station on a trusted LAN: this first version has no login or API authentication.

## Validation

```powershell
npm test
```

The protocol and firmware transformation are unit tested. A real programming cycle still requires a connected Easy PDK Programmer and a sacrificial blank PMS150C because the chip is OTP.
