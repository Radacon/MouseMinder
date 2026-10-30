import { createServer } from "node:http";
import { createHash, randomUUID } from "node:crypto";
import { execFile } from "node:child_process";
import { mkdir, readFile, rename, stat, writeFile } from "node:fs/promises";
import { dirname, extname, join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = dirname(fileURLToPath(import.meta.url));
const publicDir = join(root, "public");
const dataDir = process.env.DATA_DIR ? resolve(process.env.DATA_DIR) : join(root, "data");
const databasePath = join(dataDir, "programming-log.json");
const firmwarePath = join(root, "firmware", "slowclocksleep_PMS150C.ihx");
const gitRoot = resolve(root, "../..");
const port = Number(process.env.PORT || 8787);
const host = process.env.HOST || "0.0.0.0";
const execFileAsync = promisify(execFile);

const mimeTypes = new Map([
  [".html", "text/html; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".svg", "image/svg+xml"],
  [".ico", "image/x-icon"]
]);

let writeQueue = Promise.resolve();

async function getStationInfo() {
  try {
    const [{ stdout: hash }, { stdout: status }] = await Promise.all([
      execFileAsync("git", ["-C", gitRoot, "rev-parse", "HEAD"]),
      execFileAsync("git", ["-C", gitRoot, "status", "--porcelain", "--", "codebase/VSCODE_FreePDK"])
    ]);
    return { gitHash: hash.trim(), gitDirty: Boolean(status.trim()) };
  } catch {
    return { gitHash: cleanString(process.env.GIT_HASH, 40), gitDirty: true };
  }
}

const stationInfoPromise = getStationInfo();

async function ensureDatabase() {
  await mkdir(dataDir, { recursive: true });
  try {
    await stat(databasePath);
  } catch {
    await writeFile(databasePath, JSON.stringify({ schemaVersion: 1, records: [] }, null, 2) + "\n", "utf8");
  }
}

async function readDatabase() {
  await ensureDatabase();
  const parsed = JSON.parse(await readFile(databasePath, "utf8"));
  if (parsed?.schemaVersion !== 1 || !Array.isArray(parsed.records)) {
    throw new Error("Invalid programming-log.json format");
  }
  return parsed;
}

async function saveDatabase(database) {
  const temporaryPath = `${databasePath}.${process.pid}.tmp`;
  await writeFile(temporaryPath, JSON.stringify(database, null, 2) + "\n", "utf8");
  await rename(temporaryPath, databasePath);
}

function sendJson(response, statusCode, value) {
  const body = JSON.stringify(value, null, 2) + "\n";
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body),
    "Cache-Control": "no-store",
    "Permissions-Policy": "serial=(self)",
    "X-Content-Type-Options": "nosniff"
  });
  response.end(body);
}

async function readJsonBody(request) {
  const chunks = [];
  let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > 64 * 1024) throw new Error("Request body is too large");
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}

function cleanString(value, maxLength = 500) {
  return typeof value === "string" ? value.trim().slice(0, maxLength) : "";
}

function normalizeRecord(input) {
  const allowedResults = new Set(["success", "failure"]);
  const allowedActions = new Set(["program", "readback"]);
  if (!allowedActions.has(input?.action)) throw new Error("Invalid action");
  if (!allowedResults.has(input?.result)) throw new Error("Invalid result");
  const unitNumber = cleanString(input.unitNumber, 80);
  if (input.action === "program" && !/^\d{9}$/.test(unitNumber)) {
    throw new Error("Programming records require a 9-digit unit number");
  }

  return {
    id: randomUUID(),
    serverTimestamp: new Date().toISOString(),
    action: input.action,
    result: input.result,
    unitNumber,
    chip: cleanString(input.chip, 40),
    chipId: cleanString(input.chipId, 40),
    firmwareName: cleanString(input.firmwareName, 160),
    firmwareSha256: cleanString(input.firmwareSha256, 64),
    firmwareBytes: Number.isSafeInteger(input.firmwareBytes) ? input.firmwareBytes : null,
    programmerVersion: cleanString(input.programmerVersion, 180),
    calibration: cleanString(input.calibration, 300),
    notes: cleanString(input.notes, 1000),
    error: cleanString(input.error, 1000)
  };
}

async function firmwareInfo() {
  const bytes = await readFile(firmwarePath);
  return {
    name: "slowclocksleep_PMS150C.ihx",
    chip: "PMS150C",
    bytes: bytes.length,
    sha256: createHash("sha256").update(bytes).digest("hex")
  };
}

async function serveStatic(pathname, response) {
  const requested = pathname === "/" ? "index.html" : decodeURIComponent(pathname.slice(1));
  const filePath = resolve(publicDir, requested);
  if (filePath !== publicDir && !filePath.startsWith(publicDir + sep)) return false;

  try {
    const body = await readFile(filePath);
    response.writeHead(200, {
      "Content-Type": mimeTypes.get(extname(filePath)) || "application/octet-stream",
      "Content-Length": body.length,
      "Cache-Control": "no-cache",
      "Permissions-Policy": "serial=(self)",
      "X-Content-Type-Options": "nosniff"
    });
    response.end(body);
    return true;
  } catch {
    return false;
  }
}

const server = createServer(async (request, response) => {
  try {
    const url = new URL(request.url, `http://${request.headers.host || "localhost"}`);

    if (request.method === "GET" && url.pathname === "/api/health") {
      sendJson(response, 200, { ok: true, time: new Date().toISOString() });
      return;
    }

    if (request.method === "GET" && url.pathname === "/api/firmware/info") {
      sendJson(response, 200, await firmwareInfo());
      return;
    }

    if (request.method === "GET" && url.pathname === "/api/station-info") {
      sendJson(response, 200, await stationInfoPromise);
      return;
    }

    if (request.method === "GET" && url.pathname === "/api/firmware/standard") {
      const body = await readFile(firmwarePath);
      response.writeHead(200, {
        "Content-Type": "application/octet-stream",
        "Content-Length": body.length,
        "Content-Disposition": 'inline; filename="slowclocksleep_PMS150C.ihx"',
        "Cache-Control": "no-cache",
        "X-Content-Type-Options": "nosniff"
      });
      response.end(body);
      return;
    }

    if (request.method === "GET" && url.pathname === "/api/records") {
      const database = await readDatabase();
      sendJson(response, 200, database);
      return;
    }

    if (request.method === "POST" && url.pathname === "/api/records") {
      const record = normalizeRecord(await readJsonBody(request));
      await (writeQueue = writeQueue.catch(() => {}).then(async () => {
        const database = await readDatabase();
        if (record.action === "program" && record.result === "success" && database.records.some((existing) =>
          existing.action === "program" && existing.result === "success" && existing.unitNumber === record.unitNumber
        )) {
          throw new Error(`Unit ${record.unitNumber} already has a successful programming record`);
        }
        database.records.push(record);
        await saveDatabase(database);
      }));
      sendJson(response, 201, record);
      return;
    }

    if (request.method === "GET" && await serveStatic(url.pathname, response)) return;
    sendJson(response, 404, { error: "Not found" });
  } catch (error) {
    sendJson(response, 400, { error: error instanceof Error ? error.message : String(error) });
  }
});

await ensureDatabase();
server.listen(port, host, () => {
  console.log(`MouseMinder Programmer: http://localhost:${port}`);
  console.log(`JSON database: ${databasePath}`);
});
