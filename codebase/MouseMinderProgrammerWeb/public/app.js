import {
  EasyPdkProgrammer,
  decodePms150cMetadata,
  formatRawHex,
  getPms150cMetadataCapacity,
  preparePms150cFirmware
} from "./easypdk.js";
import { formatUnitNumber, incrementUnitNumber, nextUnitNumber } from "./unit-number.js";

const elements = Object.fromEntries([
  "connectionBadge", "compatibilityNotice", "programmerVersion", "firmwareName", "firmwareHash", "gitHash",
  "connectButton", "disconnectButton", "probeButton", "programButton", "readButton", "unitNumber",
  "notes", "console", "clearConsoleButton", "historyBody", "exportButton", "readbackOutput",
  "metadataSummary", "rawHex", "notesLimit"
].map((id) => [id, document.getElementById(id)]));

const state = {
  firmwareText: "",
  firmwareInfo: null,
  stationInfo: { gitHash: "", gitDirty: true },
  metadataCapacity: null,
  records: [],
  busy: false
};
const serialAvailable = "serial" in navigator && window.isSecureContext;

const programmer = new EasyPdkProgrammer((message, type) => log(message, type));
const textEncoder = new TextEncoder();

function utf8Length(value) {
  return textEncoder.encode(value).length;
}

function truncateUtf8(value, maximumBytes) {
  let result = "";
  let bytes = 0;
  for (const character of value) {
    const characterBytes = utf8Length(character);
    if (bytes + characterBytes > maximumBytes) break;
    result += character;
    bytes += characterBytes;
  }
  return result;
}

function updateNotesLimit() {
  const maximumBytes = Math.max(0, state.metadataCapacity?.notesBytes ?? 0);
  elements.notesLimit.textContent = `${utf8Length(elements.notes.value)} / ${maximumBytes} UTF-8 bytes`;
  elements.notes.disabled = !state.metadataCapacity || maximumBytes === 0;
}

function log(message, type = "info") {
  const line = document.createElement("div");
  line.className = `console-line ${type}`;
  line.dataset.time = new Date().toLocaleTimeString();
  line.textContent = message;
  elements.console.append(line);
  elements.console.scrollTop = elements.console.scrollHeight;
}

function setConnected(connected) {
  elements.connectionBadge.textContent = connected ? "Programmer connected" : "Disconnected";
  elements.connectionBadge.className = `badge ${connected ? "badge-online" : "badge-offline"}`;
  elements.connectButton.disabled = connected || state.busy || !serialAvailable;
  elements.disconnectButton.disabled = !connected || state.busy;
  elements.probeButton.disabled = !connected || state.busy;
  elements.programButton.disabled = !connected || state.busy || !state.firmwareText;
  elements.readButton.disabled = !connected || state.busy;
}

function setBusy(busy) {
  state.busy = busy;
  setConnected(programmer.connected);
}

async function sha256(text) {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((value) => value.toString(16).padStart(2, "0")).join("");
}

async function loadFirmware() {
  const [infoResponse, firmwareResponse] = await Promise.all([
    fetch("api/firmware/info", { cache: "no-store" }),
    fetch("api/firmware/standard", { cache: "no-store" })
  ]);
  if (!infoResponse.ok || !firmwareResponse.ok) throw new Error("Could not load standard firmware");
  state.firmwareInfo = await infoResponse.json();
  state.firmwareText = await firmwareResponse.text();
  state.metadataCapacity = getPms150cMetadataCapacity(state.firmwareText);
  elements.notes.value = truncateUtf8(elements.notes.value, Math.max(0, state.metadataCapacity.notesBytes));
  updateNotesLimit();
  const prepared = preparePms150cFirmware(state.firmwareText);
  const browserHash = await sha256(state.firmwareText);
  if (browserHash !== state.firmwareInfo.sha256) throw new Error("Firmware checksum disagrees with the server");
  elements.firmwareName.textContent = `${state.firmwareInfo.name} · ${prepared.length} programmed bytes`;
  elements.firmwareHash.textContent = state.firmwareInfo.sha256;
  elements.firmwareHash.title = state.firmwareInfo.sha256;
  setConnected(programmer.connected);
  log(`Loaded ${state.firmwareInfo.name} (${prepared.codeWords} words, ${prepared.calibrations.length} calibration block).`);
}

async function loadStationInfo() {
  const response = await fetch("api/station-info", { cache: "no-store" });
  if (!response.ok) throw new Error("Could not load Git information");
  state.stationInfo = await response.json();
  const shortHash = state.stationInfo.gitHash ? state.stationInfo.gitHash.slice(0, 16) : "unavailable";
  elements.gitHash.textContent = `${shortHash}${state.stationInfo.gitDirty ? " · dirty" : ""}`;
}

async function loadRecords() {
  const response = await fetch("api/records", { cache: "no-store" });
  if (!response.ok) throw new Error("Could not load programming history");
  const database = await response.json();
  state.records = database.records || [];
  renderRecords();
  if (!elements.unitNumber.value) elements.unitNumber.value = nextUnitNumber(state.records);
}

function renderRecords() {
  elements.historyBody.replaceChildren();
  const recent = [...state.records].reverse().slice(0, 50);
  if (!recent.length) {
    const row = elements.historyBody.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 5;
    cell.className = "empty";
    cell.textContent = "No records yet.";
    return;
  }
  for (const record of recent) {
    const row = elements.historyBody.insertRow();
    const timestamp = new Date(record.serverTimestamp);
    row.insertCell().textContent = Number.isNaN(timestamp.valueOf()) ? record.serverTimestamp : timestamp.toLocaleString();
    row.insertCell().textContent = record.unitNumber || "—";
    row.insertCell().textContent = record.action;
    const result = row.insertCell();
    result.textContent = record.result;
    result.className = `result-${record.result}`;
    const firmware = row.insertCell();
    firmware.textContent = record.firmwareSha256 ? record.firmwareSha256.slice(0, 12) : "—";
    firmware.title = record.error || record.firmwareSha256 || "";
  }
}

async function saveRecord(record) {
  const response = await fetch("api/records", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(record)
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "Could not save programming record");
  state.records.push(result);
  renderRecords();
  return result;
}

function baseRecord(action, result, error = "") {
  return {
    action,
    result,
    unitNumber: elements.unitNumber.value.trim(),
    chip: "PMS150C",
    firmwareName: state.firmwareInfo?.name || "",
    firmwareSha256: state.firmwareInfo?.sha256 || "",
    firmwareBytes: state.firmwareInfo?.bytes || null,
    programmerVersion: programmer.version,
    notes: elements.notes.value.trim(),
    error
  };
}

function download(name, contents, type) {
  const url = URL.createObjectURL(new Blob([contents], { type }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = name;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function showReadback(data) {
  elements.readbackOutput.classList.remove("hidden");
  elements.rawHex.textContent = formatRawHex(data);
  elements.metadataSummary.replaceChildren();

  let metadata;
  try {
    metadata = decodePms150cMetadata(data);
  } catch (error) {
    const message = document.createElement("div");
    message.className = "metadata-error";
    message.textContent = error.message;
    elements.metadataSummary.append(message);
    return;
  }
  if (!metadata) {
    const message = document.createElement("div");
    message.className = "muted";
    message.textContent = "No MouseMinder production metadata was found on this PCB.";
    elements.metadataSummary.append(message);
    return;
  }

  const values = [
    ["Unit", metadata.unitNumber],
    ["Programmed", new Date(metadata.programmedAt).toLocaleString()],
    ["Git", `${metadata.gitHash || "unavailable"}${metadata.gitDirty ? " · dirty" : ""}`],
    ["CRC-16", `0x${metadata.crc16.toString(16).toUpperCase().padStart(4, "0")} valid`],
    ["Format", `MMP${metadata.formatVersion} · ${metadata.length} bytes`],
    ["Notes", metadata.notes || "—", "notes"]
  ];
  for (const [label, value, className = ""] of values) {
    const item = document.createElement("div");
    item.className = `metadata-item ${className}`.trim();
    const heading = document.createElement("strong");
    heading.textContent = label;
    const content = document.createElement("span");
    content.textContent = value;
    item.append(heading, content);
    elements.metadataSummary.append(item);
  }
}

elements.connectButton.addEventListener("click", async () => {
  setBusy(true);
  try {
    log("Waiting for serial-port selection...");
    const version = await programmer.connect();
    elements.programmerVersion.textContent = version;
    log(version, "success");
  } catch (error) {
    log(error.message || String(error), "error");
    await programmer.disconnect();
  } finally {
    setBusy(false);
  }
});

elements.disconnectButton.addEventListener("click", async () => {
  setBusy(true);
  await programmer.disconnect();
  elements.programmerVersion.textContent = "Connect the Easy PDK Programmer through Chrome.";
  log("Programmer disconnected.");
  setBusy(false);
});

elements.probeButton.addEventListener("click", async () => {
  setBusy(true);
  try {
    log("Probing target IC...");
    const probe = await programmer.probe();
    if (!probe.id) throw new Error("No target IC found");
    const description = `Probe response 0x${probe.id.toString(16).toUpperCase()} · ${probe.vdd.toFixed(2)} V VDD · ${probe.vpp.toFixed(2)} V VPP`;
    log(description, probe.supported ? "success" : "error");
  } catch (error) {
    log(error.message || String(error), "error");
  } finally {
    setBusy(false);
  }
});

elements.programButton.addEventListener("click", async () => {
  let unitNumber;
  try {
    unitNumber = formatUnitNumber(elements.unitNumber.value);
    elements.unitNumber.value = unitNumber;
  } catch (error) {
    elements.unitNumber.focus();
    log(error.message, "error");
    return;
  }
  const duplicate = state.records.some((record) => record.action === "program" && record.result === "success" && record.unitNumber === unitNumber);
  if (duplicate) {
    log(`Unit ${unitNumber} already has a successful programming record.`, "error");
    elements.unitNumber.focus();
    return;
  }
  const programmedAt = new Date();
  const metadata = {
    unitNumber,
    programmedAt,
    gitHash: state.stationInfo.gitHash,
    gitDirty: state.stationInfo.gitDirty,
    notes: elements.notes.value
  };
  try {
    preparePms150cFirmware(state.firmwareText, metadata);
  } catch (error) {
    log(error.message, "error");
    elements.notes.focus();
    return;
  }
  const gitLabel = state.stationInfo.gitHash ? state.stationInfo.gitHash.slice(0, 16) : "unavailable";
  const confirmed = window.confirm(
    `PMS150C is one-time programmable.\n\nPermanently program unit ${unitNumber}?\nDate: ${programmedAt.toLocaleString()}\nGit: ${gitLabel}${state.stationInfo.gitDirty ? " (dirty)" : ""}\nNotes: ${elements.notes.value || "none"}`
  );
  if (!confirmed) return;

  setBusy(true);
  let chipId = "";
  let programmed = false;
  try {
    const result = await programmer.programPms150c(state.firmwareText, metadata, (message) => log(message));
    programmed = true;
    chipId = `0x${result.probe.id.toString(16).toUpperCase()}`;
    const calibration = result.calibrationResults.map((item) => `${item.type}:${item.measuredFrequency}Hz:0x${item.value.toString(16).padStart(2, "0")}`).join(", ");
    try {
      await saveRecord({ ...baseRecord("program", "success"), chipId, calibration });
      log(`Unit ${unitNumber} programmed, calibrated, verified, and logged.`, "success");
    } catch (logError) {
      log(`Unit ${unitNumber} was programmed successfully, but its JSON record was not saved: ${logError.message}`, "error");
    }
    elements.unitNumber.value = incrementUnitNumber(unitNumber);
    elements.unitNumber.select();
  } catch (error) {
    const message = error.message || String(error);
    log(message, "error");
    if (!programmed) {
      try {
        await saveRecord({ ...baseRecord("program", "failure", message), chipId });
      } catch (logError) {
        log(`Programming record was not saved: ${logError.message}`, "error");
      }
    }
  } finally {
    setBusy(false);
  }
});

elements.readButton.addEventListener("click", async () => {
  setBusy(true);
  let readSucceeded = false;
  try {
    const result = await programmer.readPms150c((message) => log(message));
    readSucceeded = true;
    showReadback(result.data);
    const stamp = new Date().toISOString().replaceAll(":", "-").replace(/\.\d{3}Z$/, "Z");
    download(`PMS150C-readback-${stamp}.ihx`, result.ihex, "application/octet-stream");
    try {
      await saveRecord({ ...baseRecord("readback", "success"), chipId: `0x${result.probe.id.toString(16).toUpperCase()}` });
      log("Readback downloaded and logged.", "success");
    } catch (logError) {
      log(`Readback downloaded, but its JSON record was not saved: ${logError.message}`, "error");
    }
  } catch (error) {
    const message = error.message || String(error);
    log(message, "error");
    if (!readSucceeded) {
      try { await saveRecord(baseRecord("readback", "failure", message)); } catch {}
    }
  } finally {
    setBusy(false);
  }
});

elements.clearConsoleButton.addEventListener("click", () => elements.console.replaceChildren());

elements.unitNumber.addEventListener("input", () => {
  elements.unitNumber.value = elements.unitNumber.value.replace(/\D/g, "").slice(0, 9);
});

elements.unitNumber.addEventListener("blur", () => {
  if (!elements.unitNumber.value) return;
  try {
    elements.unitNumber.value = formatUnitNumber(elements.unitNumber.value);
  } catch (error) {
    log(error.message, "error");
  }
});

elements.notes.addEventListener("beforeinput", (event) => {
  if (!event.inputType.startsWith("insert")) return;
  const inserted = event.data ?? event.dataTransfer?.getData("text/plain");
  if (inserted === null || inserted === undefined) return;
  const start = elements.notes.selectionStart ?? elements.notes.value.length;
  const end = elements.notes.selectionEnd ?? start;
  const proposed = elements.notes.value.slice(0, start) + inserted + elements.notes.value.slice(end);
  const maximumBytes = Math.max(0, state.metadataCapacity?.notesBytes ?? 0);
  if (utf8Length(proposed) > maximumBytes) event.preventDefault();
});

elements.notes.addEventListener("input", () => {
  const maximumBytes = Math.max(0, state.metadataCapacity?.notesBytes ?? 0);
  if (utf8Length(elements.notes.value) > maximumBytes) {
    elements.notes.value = truncateUtf8(elements.notes.value, maximumBytes);
  }
  updateNotesLimit();
});

elements.exportButton.addEventListener("click", () => {
  download("mouseminder-programming-log.json", JSON.stringify({ schemaVersion: 1, records: state.records }, null, 2) + "\n", "application/json");
});

if (!serialAvailable) {
  elements.compatibilityNotice.classList.remove("hidden");
  elements.compatibilityNotice.textContent = !window.isSecureContext
    ? "Web Serial is blocked because this page is not secure. Use http://localhost or serve it through HTTPS."
    : "Web Serial is not supported by this browser. Use desktop Google Chrome.";
  elements.connectButton.disabled = true;
}

Promise.all([loadFirmware(), loadStationInfo(), loadRecords()]).catch((error) => log(error.message || String(error), "error"));
setConnected(false);
