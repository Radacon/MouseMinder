export const PMS150C = Object.freeze({
  name: "PMS150C",
  id12bit: 0x0a16,
  type: 0x12,
  addressBits: 12,
  codeBits: 13,
  codeWords: 0x400,
  excludeFirstInstruction: false,
  excludeStart: 0x3f6,
  excludeEnd: 0x400,
  vddCommandRead: 3.0,
  vppCommandRead: 5.0,
  vddRead: 3.0,
  vppRead: 5.0,
  vddCommandWrite: 4.3,
  vppCommandWrite: 8.0,
  vddWrite: 5.8,
  vppWrite: 10.5,
  writeBlockSize: 2,
  writeBlockClockGroups: 1,
  writeBlockClocksPerGroup: 8
});

const COMMAND = Object.freeze({
  VERSION: "I",
  TIMING: "T",
  SET_BUFFER: "S",
  GET_BUFFER: "G",
  PROBE: "P",
  BLANK_CHECK: "Z",
  READ: "R",
  WRITE: "W",
  VERIFY: "V",
  CALIBRATE: "C"
});

const ACK = "A".charCodeAt(0);
const ERROR_MESSAGES = [
  "unknown", "unknown", "unknown", "unknown", "unknown", "unknown", "unknown", "unknown",
  "unknown", "unknown", "chip is not blank", "verify failed", "command acknowledgement failed or wrong IC ID",
  "high VPP/VDD setup failed", "VPP/VDD setup failed", "unknown"
];

const CO_BC_FIXUP = 0x1000;
const CO_BC_SETREG0 = 0x2000;
const CO_BC_SETREG1 = 0x4000;
const CO_BC_SETREG2 = 0x8000;
const CO_AC_NOP = 0x0100;
const CO_AC_SETIMM = 0x0200;
const CO_VAL_FREQ_00 = 0x0001;
const CO_VAL_FREQ_08 = 0x0002;
const CO_VAL_FREQ_16 = 0x0003;
const CO_VAL_FREQ_24 = 0x0004;
const CO_VAL_MVOL_00 = 0x0010;
const CO_VAL_MVOL_08 = 0x0011;
const CO_VAL_CAL_REG0 = 0x0020;
const CO_VAL_CAL_REG1 = 0x0021;
const CO_VAL_CAL_REG2 = 0x0022;
const CO_VAL_CAL_TYP = 0x0030;

export const PMS150C_METADATA = Object.freeze({
  endGuardWord: PMS150C.excludeStart - 1,
  endWord: PMS150C.excludeStart,
  headerBytes: 28,
  formatVersion: 2,
  legacyGuardWord: 0x380,
  legacyDataWord: 0x381,
  legacyCapacityBytes: PMS150C.excludeStart - 0x381
});

const calibrationAlgorithms = [
  {
    name: "RC13",
    loopCycles: 7,
    unknown: false,
    words: [
      [0x1452, 0xffff, 0x0f71, CO_AC_NOP],
      [0x1443, 0xffff, 0x0f8d, CO_AC_NOP],
      [0x1400, 0xff00, 0x17ff, CO_AC_SETIMM | CO_VAL_CAL_TYP],
      [0x1400, 0xff00, 0x1001, CO_AC_NOP | CO_VAL_FREQ_00],
      [0x1400, 0xff00, 0x0f70, CO_AC_NOP | CO_VAL_FREQ_08],
      [0x1400, 0xff00, 0x0080, CO_BC_SETREG0 | CO_VAL_FREQ_16],
      [0x1400, 0xff00, 0x0c90, CO_AC_NOP | CO_VAL_FREQ_24],
      [0x1400, 0xff00, 0x1001, CO_AC_NOP | CO_VAL_MVOL_00],
      [0x1400, 0xff00, 0x0e70, CO_AC_NOP | CO_VAL_MVOL_08],
      [0x1400, 0xff00, 0x1804, CO_BC_FIXUP | CO_AC_NOP | CO_VAL_CAL_REG0]
    ]
  },
  {
    name: "BG13",
    loopCycles: 7,
    unknown: false,
    words: [
      [0x1442, 0xffff, 0x1709, CO_AC_NOP],
      [0x1447, 0xffff, 0x0091, CO_AC_NOP],
      [0x1400, 0xff00, 0x0f8d, CO_AC_NOP | CO_VAL_CAL_TYP],
      [0x1400, 0xff00, 0x1784, CO_AC_NOP | CO_VAL_MVOL_00],
      [0x1400, 0xff00, 0x0080, CO_BC_SETREG1 | CO_AC_NOP | CO_VAL_MVOL_08],
      [0x1400, 0xff00, 0x17a3, CO_AC_NOP | CO_VAL_CAL_REG0],
      [0x1400, 0xff00, 0x0080, CO_BC_SETREG2 | CO_AC_NOP | CO_VAL_CAL_REG1],
      [0x1400, 0xff00, 0x17ff, CO_AC_SETIMM | CO_VAL_CAL_REG2],
      [0x1400, 0xffff, 0x0f70, CO_AC_NOP],
      [0x1400, 0xffff, 0x0080, CO_BC_SETREG0],
      [0x1400, 0xffff, 0x0c90, CO_AC_NOP],
      [0x1400, 0xffff, 0x1001, CO_AC_NOP],
      [0x1400, 0xffff, 0x0e70, CO_AC_NOP],
      [0x1400, 0xffff, 0x1808, CO_BC_FIXUP | CO_AC_NOP]
    ]
  },
  {
    name: "UNKNOWN13",
    loopCycles: 0,
    unknown: true,
    words: Array.from({ length: 6 }, () => [0x1400, 0xff00, 0, 0])
  }
];

function hexByte(value) {
  return (value & 0xff).toString(16).toUpperCase().padStart(2, "0");
}

function createHexLine(type, address, bytes) {
  let sum = bytes.length + (address & 0xff) + ((address >>> 8) & 0xff) + type;
  let line = `:${hexByte(bytes.length)}${address.toString(16).toUpperCase().padStart(4, "0")}${hexByte(type)}`;
  for (const byte of bytes) {
    sum += byte;
    line += hexByte(byte);
  }
  return `${line}${hexByte(-sum)}\n`;
}

export function parseIntelHex(text, capacity = 0x2000) {
  const data = new Uint8Array(capacity);
  data.fill(0xff);
  let length = 0;
  let eof = false;

  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line) continue;
    if (!line.startsWith(":") || line.length < 11 || line.length % 2 === 0) {
      throw new Error("Invalid Intel HEX record");
    }
    const record = [];
    for (let index = 1; index < line.length; index += 2) {
      const value = Number.parseInt(line.slice(index, index + 2), 16);
      if (!Number.isInteger(value)) throw new Error("Invalid Intel HEX byte");
      record.push(value);
    }
    if (record.reduce((sum, value) => sum + value, 0) % 256 !== 0) {
      throw new Error("Intel HEX checksum failed");
    }
    const count = record[0];
    const address = (record[1] << 8) | record[2];
    const type = record[3];
    if (record.length !== count + 5) throw new Error("Intel HEX byte count mismatch");
    if (type === 1) {
      eof = true;
      break;
    }
    if (type !== 0) throw new Error(`Unsupported Intel HEX record type ${type}`);
    if (address + count > capacity) throw new Error("Firmware exceeds supported address space");
    data.set(record.slice(4, 4 + count), address);
    length = Math.max(length, address + count);
  }

  if (!eof) throw new Error("Intel HEX end-of-file record is missing");
  if (length === 0) throw new Error("Firmware contains no data");
  return { data, length };
}

export function toIntelHex(data) {
  let output = "";
  for (let address = 0; address < data.length; address += 32) {
    output += createHexLine(0, address, data.slice(address, address + 32));
  }
  return output + createHexLine(1, 0, new Uint8Array());
}

export function formatRawHex(data) {
  const lines = [];
  for (let address = 0; address < data.length; address += 16) {
    const bytes = data.slice(address, address + 16);
    const hex = [...bytes].map((value) => hexByte(value)).join(" ").padEnd(47, " ");
    const ascii = [...bytes].map((value) => value >= 32 && value <= 126 ? String.fromCharCode(value) : ".").join("");
    lines.push(`${address.toString(16).toUpperCase().padStart(4, "0")}: ${hex}  |${ascii}|`);
  }
  return lines.join("\n");
}

function getWord(data, wordAddress) {
  const offset = wordAddress * 2;
  return data[offset] | (data[offset + 1] << 8);
}

function setWord(data, wordAddress, value) {
  const offset = wordAddress * 2;
  data[offset] = value & 0xff;
  data[offset + 1] = (value >>> 8) & 0xff;
}

function crc16Ccitt(data) {
  let crc = 0xffff;
  for (const byte of data) {
    crc ^= byte << 8;
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc & 0x8000) ? ((crc << 1) ^ 0x1021) & 0xffff : (crc << 1) & 0xffff;
    }
  }
  return crc;
}

function writeU32(data, offset, value) {
  const unsigned = value >>> 0;
  data[offset] = unsigned & 0xff;
  data[offset + 1] = (unsigned >>> 8) & 0xff;
  data[offset + 2] = (unsigned >>> 16) & 0xff;
  data[offset + 3] = (unsigned >>> 24) & 0xff;
}

function writeU16(data, offset, value) {
  data[offset] = value & 0xff;
  data[offset + 1] = (value >>> 8) & 0xff;
}

function metadataCrc(bytes, crcOffset) {
  const copy = bytes.slice();
  copy[crcOffset] = 0;
  copy[crcOffset + 1] = 0;
  return crc16Ccitt(copy);
}

export function encodePms150cMetadata({ unitNumber, programmedAt = new Date(), gitHash = "", gitDirty = false, notes = "" }) {
  if (!/^\d{9}$/.test(String(unitNumber))) throw new Error("Metadata requires a 9-digit unit number");
  const numericUnit = Number.parseInt(unitNumber, 10);
  if (numericUnit < 1) throw new Error("Metadata unit number must be greater than zero");

  const timestamp = Math.floor(new Date(programmedAt).getTime() / 1000);
  if (!Number.isSafeInteger(timestamp) || timestamp < 1 || timestamp > 0xffffffff) {
    throw new Error("Metadata programming date is invalid");
  }

  const noteBytes = new TextEncoder().encode(String(notes));
  const bytes = new Uint8Array(PMS150C_METADATA.headerBytes + noteBytes.length);
  bytes.set(new TextEncoder().encode("MMP2"), 0);
  bytes[4] = PMS150C_METADATA.formatVersion;
  bytes[5] = gitDirty ? 1 : 0;
  writeU16(bytes, 6, bytes.length);
  writeU16(bytes, 8, noteBytes.length);
  writeU32(bytes, 12, numericUnit);
  writeU32(bytes, 16, timestamp);

  const normalizedHash = String(gitHash).trim().toLowerCase();
  if (normalizedHash && !/^[0-9a-f]{16,40}$/.test(normalizedHash)) throw new Error("Git hash must be hexadecimal");
  if (normalizedHash) {
    for (let index = 0; index < 8; index += 1) {
      bytes[20 + index] = Number.parseInt(normalizedHash.slice(index * 2, index * 2 + 2), 16);
    }
  }
  bytes.set(noteBytes, PMS150C_METADATA.headerBytes);
  const crc = metadataCrc(bytes, 10);
  writeU16(bytes, 10, crc);
  return bytes;
}

function decodeLegacyMetadata(data) {
  const guardInstruction = 0x1800 | PMS150C_METADATA.legacyGuardWord;
  if (getWord(data, PMS150C_METADATA.legacyGuardWord) !== guardInstruction) return null;
  const prefix = new Uint8Array(6);
  for (let index = 0; index < prefix.length; index += 1) prefix[index] = getWord(data, PMS150C_METADATA.legacyDataWord + index) & 0xff;
  if (new TextDecoder().decode(prefix.slice(0, 4)) !== "MMP1") return null;
  const length = prefix[5];
  if (length < 26 || length > PMS150C_METADATA.legacyCapacityBytes) throw new Error("Legacy metadata length is invalid");

  const bytes = new Uint8Array(length);
  for (let index = 0; index < length; index += 1) {
    const word = getWord(data, PMS150C_METADATA.legacyDataWord + index);
    if (word > 0xff) throw new Error("Metadata word contains unexpected high bits");
    bytes[index] = word;
  }
  const storedCrc = bytes[8] | (bytes[9] << 8);
  const calculatedCrc = metadataCrc(bytes, 8);
  if (storedCrc !== calculatedCrc) throw new Error(`Metadata CRC failed (stored 0x${storedCrc.toString(16).padStart(4, "0")}, calculated 0x${calculatedCrc.toString(16).padStart(4, "0")})`);

  const notesLength = bytes[7];
  if (26 + notesLength !== length) throw new Error("Metadata notes length is invalid");
  const unitNumber = readU32(bytes, 10);
  const timestamp = readU32(bytes, 14);
  const gitBytes = bytes.slice(18, 26);
  const gitHash = gitBytes.some((value) => value !== 0) ? [...gitBytes].map(hexByte).join("").toLowerCase() : "";

  return {
    formatVersion: bytes[4],
    unitNumber: String(unitNumber).padStart(9, "0"),
    programmedAt: new Date(timestamp * 1000).toISOString(),
    gitHash,
    gitDirty: Boolean(bytes[6] & 1),
    notes: new TextDecoder("utf-8", { fatal: true }).decode(bytes.slice(26)),
    crc16: storedCrc,
    length,
    dataWord: PMS150C_METADATA.legacyDataWord
  };
}

function decodeCurrentMetadataAt(data, dataWord) {
  const guardWord = dataWord - 1;
  if (getWord(data, guardWord) !== (0x1800 | guardWord)) return null;
  if (getWord(data, PMS150C_METADATA.endGuardWord) !== (0x1800 | PMS150C_METADATA.endGuardWord)) return null;
  const prefix = new Uint8Array(12);
  for (let index = 0; index < prefix.length; index += 1) {
    const word = getWord(data, dataWord + index);
    if (word > 0xff) return null;
    prefix[index] = word;
  }
  if (new TextDecoder().decode(prefix.slice(0, 4)) !== "MMP2") return null;
  if (prefix[4] !== PMS150C_METADATA.formatVersion) throw new Error(`Unsupported metadata format ${prefix[4]}`);
  const length = readU16(prefix, 6);
  if (length < PMS150C_METADATA.headerBytes || dataWord + length > PMS150C_METADATA.endGuardWord) {
    throw new Error("Metadata length is invalid");
  }
  const bytes = new Uint8Array(length);
  for (let index = 0; index < length; index += 1) {
    const word = getWord(data, dataWord + index);
    if (word > 0xff) throw new Error("Metadata word contains unexpected high bits");
    bytes[index] = word;
  }
  const storedCrc = readU16(bytes, 10);
  const calculatedCrc = metadataCrc(bytes, 10);
  if (storedCrc !== calculatedCrc) throw new Error(`Metadata CRC failed (stored 0x${storedCrc.toString(16).padStart(4, "0")}, calculated 0x${calculatedCrc.toString(16).padStart(4, "0")})`);
  const notesLength = readU16(bytes, 8);
  if (PMS150C_METADATA.headerBytes + notesLength !== length) throw new Error("Metadata notes length is invalid");
  const unitNumber = readU32(bytes, 12);
  const timestamp = readU32(bytes, 16);
  const gitBytes = bytes.slice(20, 28);
  const gitHash = gitBytes.some((value) => value !== 0) ? [...gitBytes].map(hexByte).join("").toLowerCase() : "";
  return {
    formatVersion: bytes[4],
    unitNumber: String(unitNumber).padStart(9, "0"),
    programmedAt: new Date(timestamp * 1000).toISOString(),
    gitHash,
    gitDirty: Boolean(bytes[5] & 1),
    notes: new TextDecoder("utf-8", { fatal: true }).decode(bytes.slice(PMS150C_METADATA.headerBytes)),
    crc16: storedCrc,
    length,
    dataWord
  };
}

export function decodePms150cMetadata(data) {
  if (data.length < PMS150C_METADATA.endWord * 2) return null;
  for (let dataWord = 1; dataWord <= PMS150C_METADATA.endGuardWord - PMS150C_METADATA.headerBytes; dataWord += 1) {
    const metadata = decodeCurrentMetadataAt(data, dataWord);
    if (metadata) return metadata;
  }
  return decodeLegacyMetadata(data);
}

function metadataCapacityForLength(currentLength) {
  const applicationWords = Math.ceil(currentLength / 2);
  const dataWord = applicationWords + 1;
  return {
    applicationWords,
    dataWord,
    notesBytes: PMS150C_METADATA.endGuardWord - dataWord - PMS150C_METADATA.headerBytes
  };
}

export function getPms150cMetadataCapacity(text) {
  const parsed = parseIntelHex(text);
  let length = parsed.length;
  if (length === PMS150C.codeWords * 2) length -= 2;
  return metadataCapacityForLength(length);
}

function injectPms150cMetadata(data, currentLength, metadata) {
  const capacity = metadataCapacityForLength(currentLength);
  const bytes = encodePms150cMetadata(metadata);
  const noteBytes = bytes.length - PMS150C_METADATA.headerBytes;
  if (noteBytes > capacity.notesBytes) {
    throw new Error(`Embedded notes are ${noteBytes} bytes; this firmware has room for ${capacity.notesBytes}`);
  }
  if (capacity.notesBytes < 0 || capacity.dataWord + bytes.length > PMS150C_METADATA.endGuardWord) {
    throw new Error("Firmware leaves no room for production metadata");
  }
  for (let word = capacity.applicationWords; word < PMS150C_METADATA.endWord; word += 1) {
    if (getWord(data, word) !== 0xffff) throw new Error(`Firmware already uses metadata word 0x${word.toString(16).toUpperCase()}`);
  }
  setWord(data, capacity.applicationWords, 0x1800 | capacity.applicationWords);
  for (let index = 0; index < bytes.length; index += 1) setWord(data, capacity.dataWord + index, bytes[index]);
  setWord(data, PMS150C_METADATA.endGuardWord, 0x1800 | PMS150C_METADATA.endGuardWord);
  return PMS150C_METADATA.endWord * 2;
}

function findPattern(data, wordCount, algorithm) {
  for (let position = 0; position <= wordCount - algorithm.words.length; position += 1) {
    let matches = true;
    for (let index = 0; index < algorithm.words.length; index += 1) {
      const [searchOpcode, searchMask] = algorithm.words[index];
      if ((getWord(data, position + index) & searchMask) !== searchOpcode) {
        matches = false;
        break;
      }
    }
    if (matches) return position;
  }
  return -1;
}

function insertOneCalibration(data, length) {
  const wordCount = Math.floor(length / 2);
  let algorithmIndex = -1;
  let position = -1;
  for (let index = 0; index < calibrationAlgorithms.length; index += 1) {
    position = findPattern(data, wordCount, calibrationAlgorithms[index]);
    if (position >= 0) {
      algorithmIndex = index;
      break;
    }
  }
  if (algorithmIndex < 0) return null;

  const algorithm = calibrationAlgorithms[algorithmIndex];
  if (algorithm.unknown) throw new Error("Unknown firmware calibration block");

  const calibration = {
    algorithmIndex,
    algorithm: algorithm.name,
    loopCycles: algorithm.loopCycles,
    position,
    type: 0,
    frequency: 0,
    millivolt: 0
  };
  let register0 = 0;
  let register1 = 0;
  let register2 = 0;

  for (let index = 0; index < algorithm.words.length; index += 1) {
    const value = getWord(data, position + index) & 0xff;
    switch (algorithm.words[index][3] & 0xff) {
      case CO_VAL_FREQ_00: calibration.frequency |= value; break;
      case CO_VAL_FREQ_08: calibration.frequency |= value << 8; break;
      case CO_VAL_FREQ_16: calibration.frequency |= value << 16; break;
      case CO_VAL_FREQ_24: calibration.frequency += value * 0x1000000; break;
      case CO_VAL_MVOL_00: calibration.millivolt |= value; break;
      case CO_VAL_MVOL_08: calibration.millivolt |= value << 8; break;
      case CO_VAL_CAL_TYP: calibration.type = value; break;
      case CO_VAL_CAL_REG0: register0 = value; break;
      case CO_VAL_CAL_REG1: register1 = value; break;
      case CO_VAL_CAL_REG2: register2 = value; break;
      default: break;
    }
  }

  for (let index = 0; index < algorithm.words.length; index += 1) {
    const [, , calibrationOpcode, flags] = algorithm.words[index];
    let opcode = calibrationOpcode;
    if (flags & CO_BC_SETREG0) opcode |= register0;
    if (flags & CO_BC_SETREG1) opcode |= register1;
    if (flags & CO_BC_SETREG2) opcode |= register2;
    if (flags & CO_BC_FIXUP) opcode += position;
    setWord(data, position + index, opcode);
  }

  return calibration;
}

function removeCalibration(data, calibration, value) {
  const algorithm = calibrationAlgorithms[calibration.algorithmIndex];
  for (let index = 0; index < algorithm.words.length; index += 1) {
    const flags = algorithm.words[index][3];
    if (flags & CO_AC_SETIMM) {
      setWord(data, calibration.position + index, (getWord(data, calibration.position + index) & 0xff00) | value);
    }
    if (flags & CO_AC_NOP) setWord(data, calibration.position + index, 0);
  }
}

export function preparePms150cFirmware(text, metadata = null) {
  const parsed = parseIntelHex(text);
  if (parsed.length > PMS150C.codeWords * 2) throw new Error("Firmware is too large for PMS150C");
  const data = parsed.data;
  let length = parsed.length;
  let fuse = null;

  if (length === PMS150C.codeWords * 2) {
    fuse = data[length - 2] | (data[length - 1] << 8);
    length -= 2;
  }

  if (metadata) length = injectPms150cMetadata(data, length, metadata);

  const calibrations = [];
  for (let index = 0; index < 16; index += 1) {
    const calibration = insertOneCalibration(data, length);
    if (!calibration) break;
    calibrations.push(calibration);
  }

  return {
    data: data.slice(0, length),
    length,
    codeWords: Math.ceil(length / 2),
    fuse,
    calibrations
  };
}

function pushU8(output, value) {
  output.push(value & 0xff);
}

function pushU16(output, value) {
  output.push(value & 0xff, (value >>> 8) & 0xff);
}

function pushU32(output, value) {
  const unsigned = value >>> 0;
  output.push(unsigned & 0xff, (unsigned >>> 8) & 0xff, (unsigned >>> 16) & 0xff, (unsigned >>> 24) & 0xff);
}

function pushVoltage(output, value) {
  pushU32(output, Math.round(value * 1000));
}

function readU16(data, offset = 0) {
  return data[offset] | (data[offset + 1] << 8);
}

function readU32(data, offset = 0) {
  return (data[offset] | (data[offset + 1] << 8) | (data[offset + 2] << 16) | (data[offset + 3] << 24)) >>> 0;
}

function resultError(result) {
  if (result >= 0xfff0) return ERROR_MESSAGES[result & 0x0f];
  return null;
}

function assertIcResult(result, operation) {
  const error = resultError(result);
  if (error) throw new Error(`${operation}: ${error}`);
  if (result !== PMS150C.id12bit) {
    throw new Error(`${operation}: unexpected IC response 0x${result.toString(16).toUpperCase()}`);
  }
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

export class EasyPdkProgrammer {
  constructor(log = () => {}) {
    this.log = log;
    this.port = null;
    this.reader = null;
    this.readerTask = null;
    this.receiveBytes = [];
    this.waiters = new Set();
    this.desynchronized = false;
    this.busy = false;
    this.version = "";
  }

  get connected() {
    return Boolean(this.port?.readable && this.port?.writable && !this.desynchronized);
  }

  async connect() {
    if (!("serial" in navigator)) throw new Error("Web Serial is unavailable. Use desktop Chrome over localhost or HTTPS.");
    if (this.port) await this.disconnect();

    this.port = await navigator.serial.requestPort();
    await this.port.open({ baudRate: 115200, dataBits: 8, stopBits: 1, parity: "none", flowControl: "none", bufferSize: 65536 });
    try {
      await this.port.setSignals({ dataTerminalReady: true });
    } catch {
      // Some serial drivers do not expose signal control.
    }

    this.receiveBytes = [];
    this.desynchronized = false;
    this.reader = this.port.readable.getReader();
    this.readerTask = this.#pumpReader();
    await delay(100);
    this.receiveBytes = [];
    this.version = await this.getVersion();
    const match = this.version.match(/PROTO:(\d+)\.(\d+)/i);
    if (!match || match[1] !== "1" || match[2] !== "4") {
      await this.disconnect();
      throw new Error(`Programmer protocol mismatch: ${this.version.trim()}`);
    }
    await this.setTiming(10000, 20);
    return this.version;
  }

  async disconnect() {
    const port = this.port;
    this.port = null;
    for (const waiter of this.waiters) waiter();
    this.waiters.clear();
    try { await this.reader?.cancel(); } catch {}
    try { await this.readerTask; } catch {}
    this.reader = null;
    this.readerTask = null;
    try { await port?.close(); } catch {}
    this.receiveBytes = [];
    this.version = "";
  }

  async #pumpReader() {
    try {
      while (true) {
        const { value, done } = await this.reader.read();
        if (done) break;
        if (value?.length) {
          this.receiveBytes.push(...value);
          for (const waiter of this.waiters) waiter();
          this.waiters.clear();
        }
      }
    } catch (error) {
      if (this.port) {
        this.desynchronized = true;
        this.log(`Serial read failed: ${error.message || error}`, "error");
      }
    } finally {
      try { this.reader?.releaseLock(); } catch {}
    }
  }

  async #readExact(length, timeoutMs) {
    const deadline = Date.now() + timeoutMs;
    while (this.receiveBytes.length < length) {
      const remaining = deadline - Date.now();
      if (remaining <= 0) {
        this.desynchronized = true;
        throw new Error("Programmer response timed out; reconnect the programmer");
      }
      await new Promise((resolve) => {
        let timer;
        const wake = () => {
          clearTimeout(timer);
          this.waiters.delete(wake);
          resolve();
        };
        this.waiters.add(wake);
        timer = setTimeout(wake, remaining);
      });
    }
    return new Uint8Array(this.receiveBytes.splice(0, length));
  }

  async #command(command, payload = new Uint8Array(), timeoutMs = 500) {
    if (!this.connected) throw new Error("Programmer is not connected");
    if (payload.length > 255) throw new Error("Protocol payload exceeds 255 bytes");
    const packet = new Uint8Array(2 + payload.length);
    packet[0] = command.charCodeAt(0);
    packet[1] = payload.length;
    packet.set(payload, 2);

    const writer = this.port.writable.getWriter();
    try {
      await writer.write(packet);
    } finally {
      writer.releaseLock();
    }

    const header = await this.#readExact(3, timeoutMs);
    const responseLength = header[1] | (header[2] << 8);
    const response = await this.#readExact(responseLength, timeoutMs);
    if (header[0] !== ACK) {
      const detail = new TextDecoder().decode(response).trim();
      throw new Error(`Programmer rejected ${command}${detail ? `: ${detail}` : ""}`);
    }
    return response;
  }

  async #resultCommand(command, payload, timeoutMs) {
    const response = await this.#command(command, payload, timeoutMs);
    if (response.length !== 2) throw new Error(`Invalid ${command} response length`);
    return readU16(response);
  }

  async #exclusive(operation) {
    if (this.busy) throw new Error("Another programmer operation is already running");
    this.busy = true;
    try {
      return await operation();
    } finally {
      this.busy = false;
    }
  }

  async getVersion() {
    return new TextDecoder().decode(await this.#command(COMMAND.VERSION, new Uint8Array(), 1000)).trim();
  }

  async setTiming(frequencyHz, phaseMicroseconds) {
    const payload = [];
    pushU32(payload, frequencyHz);
    pushU32(payload, phaseMicroseconds);
    await this.#command(COMMAND.TIMING, new Uint8Array(payload));
  }

  async probe() {
    return this.#exclusive(async () => {
      await this.setTiming(10000, 20);
      return this.#probeUnlocked();
    });
  }

  async #probeUnlocked() {
    const response = await this.#command(COMMAND.PROBE, new Uint8Array(), 35000);
    if (response.length !== 16) throw new Error("Invalid probe response");
    const id = readU32(response, 0);
    const error = id <= 0xffff ? resultError(id) : null;
    if (error) throw new Error(`Probe: ${error}`);
    const probe = {
      id,
      vpp: readU32(response, 4) / 1000,
      vdd: readU32(response, 8) / 1000,
      type: response[12]
    };
    probe.supported = probe.type === PMS150C.type && ((probe.id >>> 6) & 0x0fff) === PMS150C.id12bit;
    return probe;
  }

  #memoryPayload(mode, count, extra = []) {
    const output = [];
    pushU16(output, PMS150C.id12bit);
    pushU8(output, PMS150C.type);
    pushVoltage(output, mode === "write" ? PMS150C.vddCommandWrite : PMS150C.vddCommandRead);
    pushVoltage(output, mode === "write" ? PMS150C.vppCommandWrite : PMS150C.vppCommandRead);
    pushVoltage(output, mode === "write" ? PMS150C.vddWrite : PMS150C.vddRead);
    pushVoltage(output, mode === "write" ? PMS150C.vppWrite : PMS150C.vppRead);
    output.push(...extra);
    pushU16(output, count);
    return new Uint8Array(output);
  }

  #blankCheckPayload() {
    const extra = [PMS150C.addressBits, PMS150C.codeBits];
    const payload = Array.from(this.#memoryPayload("read", PMS150C.codeWords, extra));
    pushU8(payload, PMS150C.excludeFirstInstruction ? 1 : 0);
    pushU16(payload, PMS150C.excludeStart);
    pushU16(payload, PMS150C.excludeEnd);
    return new Uint8Array(payload);
  }

  #readPayload(count) {
    const extra = [];
    pushU16(extra, 0);
    pushU8(extra, PMS150C.addressBits);
    pushU16(extra, 0);
    pushU8(extra, PMS150C.codeBits);
    return this.#memoryPayload("read", count, extra);
  }

  #writePayload(count, address = 0, dataOffset = 0) {
    const extra = [];
    pushU16(extra, address);
    pushU8(extra, PMS150C.addressBits);
    pushU16(extra, dataOffset);
    pushU8(extra, PMS150C.codeBits);
    const payload = Array.from(this.#memoryPayload("write", count, extra));
    pushU8(payload, PMS150C.writeBlockSize);
    pushU8(payload, PMS150C.writeBlockClockGroups);
    pushU8(payload, PMS150C.writeBlockClocksPerGroup);
    return new Uint8Array(payload);
  }

  #verifyPayload(count) {
    const extra = [];
    pushU16(extra, 0);
    pushU8(extra, PMS150C.addressBits);
    pushU16(extra, 0);
    pushU8(extra, PMS150C.codeBits);
    const payload = Array.from(this.#memoryPayload("read", count, extra));
    pushU8(payload, PMS150C.excludeFirstInstruction ? 1 : 0);
    pushU16(payload, PMS150C.excludeStart);
    pushU16(payload, PMS150C.excludeEnd);
    return new Uint8Array(payload);
  }

  async #setBuffer(data, baseOffset = 0) {
    for (let offset = 0; offset < data.length; offset += 252) {
      const chunk = data.slice(offset, offset + 252);
      const payload = new Uint8Array(2 + chunk.length);
      payload[0] = (baseOffset + offset) & 0xff;
      payload[1] = ((baseOffset + offset) >>> 8) & 0xff;
      payload.set(chunk, 2);
      await this.#command(COMMAND.SET_BUFFER, payload);
    }
  }

  async #getBuffer(length, baseOffset = 0) {
    const output = new Uint8Array(length);
    for (let offset = 0; offset < length; offset += 63) {
      const chunkLength = Math.min(63, length - offset);
      const request = [];
      pushU16(request, baseOffset + offset);
      pushU16(request, chunkLength);
      const response = await this.#command(COMMAND.GET_BUFFER, new Uint8Array(request));
      if (response.length !== chunkLength) throw new Error("Programmer returned an invalid buffer length");
      output.set(response, offset);
    }
    return output;
  }

  async programPms150c(firmwareText, metadata = null, progress = () => {}) {
    const prepared = preparePms150cFirmware(firmwareText, metadata);
    return this.#exclusive(async () => {
      await this.setTiming(10000, 20);
      progress("Probing PMS150C...");
      const probe = await this.#probeUnlocked();
      if (!probe.id) throw new Error("No target IC found");
      if (!probe.supported) throw new Error(`Target is not a supported PMS150C (response 0x${probe.id.toString(16).toUpperCase()})`);

      progress("Blank-checking OTP memory...");
      const blankResult = await this.#resultCommand(COMMAND.BLANK_CHECK, this.#blankCheckPayload(), 10000);
      assertIcResult(blankResult, "Blank check");

      progress(`Transferring ${prepared.length} firmware bytes...`);
      await this.#setBuffer(prepared.data);

      progress(`Programming ${prepared.codeWords} words...`);
      const writeResult = await this.#resultCommand(COMMAND.WRITE, this.#writePayload(prepared.codeWords), 20000);
      assertIcResult(writeResult, "Write");

      progress("Verifying firmware...");
      const verifyResult = await this.#resultCommand(COMMAND.VERIFY, this.#verifyPayload(prepared.codeWords), 10000);
      assertIcResult(verifyResult, "Verify");

      const calibrationResults = [];
      for (const calibration of [...prepared.calibrations].sort((a, b) => a.position - b.position)) {
        const typeName = calibration.type === 1 ? "IHRC" : calibration.type === 2 ? "ILRC" : calibration.type === 3 ? "BandGap" : "unknown";
        progress(`Calibrating ${typeName}...`);
        const request = [];
        pushU32(request, calibration.type);
        pushU32(request, calibration.millivolt);
        pushU32(request, calibration.frequency);
        pushU32(request, calibration.loopCycles);
        const response = await this.#command(COMMAND.CALIBRATE, new Uint8Array(request), 100000);
        if (response.length !== 8) throw new Error("Invalid calibration response");
        const value = response[0];
        const measuredFrequency = readU32(response, 4);
        if ((calibration.type === 1 || calibration.type === 2) && Math.abs(measuredFrequency - calibration.frequency) > calibration.frequency / 10) {
          throw new Error(`${typeName} calibration is out of range (${measuredFrequency} Hz)`);
        }
        removeCalibration(prepared.data, calibration, value);
        await this.#setBuffer(prepared.data);
        const calibrationWrite = await this.#resultCommand(COMMAND.WRITE, this.#writePayload(prepared.codeWords), 20000);
        assertIcResult(calibrationWrite, "Calibration write");
        calibrationResults.push({ type: typeName, value, targetFrequency: calibration.frequency, measuredFrequency });
      }

      if (prepared.fuse !== null) {
        const safeFuse = prepared.fuse | 1;
        progress(`Writing fuse 0x${safeFuse.toString(16).toUpperCase().padStart(4, "0")}...`);
        const fuseBytes = new Uint8Array([safeFuse & 0xff, safeFuse >>> 8]);
        const fuseAddress = PMS150C.codeWords - 1;
        await this.#setBuffer(fuseBytes, fuseAddress * 2);
        const fuseResult = await this.#resultCommand(COMMAND.WRITE, this.#writePayload(1, fuseAddress, fuseAddress), 20000);
        assertIcResult(fuseResult, "Fuse write");
      }

      progress("Programming complete.");
      return { probe, calibrationResults, bytes: prepared.length, words: prepared.codeWords };
    });
  }

  async readPms150c(progress = () => {}) {
    return this.#exclusive(async () => {
      await this.setTiming(10000, 20);
      progress("Probing PMS150C...");
      const probe = await this.#probeUnlocked();
      if (!probe.id) throw new Error("No target IC found");
      if (!probe.supported) throw new Error("Target is not a supported PMS150C");
      progress(`Reading ${PMS150C.codeWords} words...`);
      const result = await this.#resultCommand(COMMAND.READ, this.#readPayload(PMS150C.codeWords), 10000);
      assertIcResult(result, "Read");
      const data = await this.#getBuffer(PMS150C.codeWords * 2);
      progress("Readback complete.");
      return { probe, data, ihex: toIntelHex(data) };
    });
  }
}
