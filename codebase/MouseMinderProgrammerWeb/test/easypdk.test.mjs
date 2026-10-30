import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";
import {
  decodePms150cMetadata,
  formatRawHex,
  getPms150cMetadataCapacity,
  parseIntelHex,
  PMS150C_METADATA,
  preparePms150cFirmware,
  toIntelHex
} from "../public/easypdk.js";

const firmwareUrl = new URL("../firmware/slowclocksleep_PMS150C.ihx", import.meta.url);

test("standard MouseMinder firmware parses with the expected calibration", async () => {
  const firmware = await readFile(firmwareUrl, "utf8");
  const prepared = preparePms150cFirmware(firmware);

  assert.equal(prepared.length, 892);
  assert.equal(prepared.codeWords, 446);
  assert.equal(prepared.fuse, null);
  assert.equal(prepared.calibrations.length, 1);
  assert.deepEqual(
    {
      type: prepared.calibrations[0].type,
      frequency: prepared.calibrations[0].frequency,
      millivolt: prepared.calibrations[0].millivolt,
      position: prepared.calibrations[0].position
    },
    { type: 2, frequency: 52000, millivolt: 2800, position: 393 }
  );
});

test("Intel HEX export round-trips binary bytes", () => {
  const input = Uint8Array.from({ length: 95 }, (_, index) => (index * 37) & 0xff);
  const output = toIntelHex(input);
  const parsed = parseIntelHex(output, 256);
  assert.equal(parsed.length, input.length);
  assert.deepEqual(parsed.data.slice(0, parsed.length), input);
});

test("Intel HEX checksum errors are rejected", () => {
  assert.throws(() => parseIntelHex(":020000000102FA\n:00000001FF\n"), /checksum/i);
});

test("production metadata round-trips through reserved program words", async () => {
  const firmware = await readFile(firmwareUrl, "utf8");
  const capacity = getPms150cMetadataCapacity(firmware);
  assert.deepEqual(capacity, { applicationWords: 446, dataWord: 447, notesBytes: 538 });
  const prepared = preparePms150cFirmware(firmware, {
    unitNumber: "000000003",
    programmedAt: "2026-10-27T23:15:00.000Z",
    gitHash: "0123456789abcdef0123456789abcdef01234567",
    gitDirty: true,
    notes: "Luke 19:40 - the stones will cry out."
  });
  const readback = new Uint8Array(2048);
  readback.fill(0xff);
  readback.set(prepared.data);
  const metadata = decodePms150cMetadata(readback);

  assert.equal(metadata.unitNumber, "000000003");
  assert.equal(metadata.programmedAt, "2026-10-27T23:15:00.000Z");
  assert.equal(metadata.gitHash, "0123456789abcdef");
  assert.equal(metadata.gitDirty, true);
  assert.equal(metadata.notes, "Luke 19:40 - the stones will cry out.");
  assert.equal(readback[446 * 2] | (readback[446 * 2 + 1] << 8), 0x1800 | 446);
  assert.equal(readback[PMS150C_METADATA.endGuardWord * 2] | (readback[PMS150C_METADATA.endGuardWord * 2 + 1] << 8), 0x1800 | PMS150C_METADATA.endGuardWord);
});

test("metadata corruption is detected by CRC", async () => {
  const firmware = await readFile(firmwareUrl, "utf8");
  const prepared = preparePms150cFirmware(firmware, {
    unitNumber: "000000004",
    programmedAt: "2026-10-27T23:15:00.000Z",
    gitHash: "0123456789abcdef",
    notes: "test"
  });
  const readback = new Uint8Array(2048);
  readback.fill(0xff);
  readback.set(prepared.data);
  readback[(447 + PMS150C_METADATA.headerBytes) * 2] ^= 1;
  assert.throws(() => decodePms150cMetadata(readback), /CRC failed/i);
});

test("notes capacity follows firmware size and enforces UTF-8 bytes", async () => {
  const firmware = await readFile(firmwareUrl, "utf8");
  const base = {
    unitNumber: "000000005",
    programmedAt: "2026-10-27T23:15:00.000Z",
    gitHash: "0123456789abcdef"
  };
  assert.doesNotThrow(() => preparePms150cFirmware(firmware, { ...base, notes: "a".repeat(538) }));
  assert.throws(() => preparePms150cFirmware(firmware, { ...base, notes: "a".repeat(539) }), /room for 538/i);
  assert.throws(() => preparePms150cFirmware(firmware, { ...base, notes: "😀".repeat(135) + "a" }), /room for 538/i);
});

test("raw readback formatter includes addresses, bytes, and ASCII", () => {
  const dump = formatRawHex(Uint8Array.from([0x4d, 0x4d, 0x50, 0x32, 0x00, 0xff]));
  assert.match(dump, /^0000: 4D 4D 50 32 00 FF/);
  assert.match(dump, /\|MMP2\.\.\|$/);
});
