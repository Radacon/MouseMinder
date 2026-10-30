export const UNIT_NUMBER_WIDTH = 9;
const MAX_UNIT_NUMBER = 10 ** UNIT_NUMBER_WIDTH - 1;

export function formatUnitNumber(value) {
  const text = String(value ?? "").trim();
  if (!/^\d+$/.test(text)) throw new Error("Unit number must contain digits only");
  const number = Number.parseInt(text, 10);
  if (!Number.isSafeInteger(number) || number < 1 || number > MAX_UNIT_NUMBER) {
    throw new Error(`Unit number must be between 1 and ${MAX_UNIT_NUMBER}`);
  }
  return String(number).padStart(UNIT_NUMBER_WIDTH, "0");
}

export function incrementUnitNumber(value) {
  const current = Number.parseInt(formatUnitNumber(value), 10);
  if (current >= MAX_UNIT_NUMBER) throw new Error("The unit-number range is exhausted");
  return formatUnitNumber(current + 1);
}

export function nextUnitNumber(records) {
  let highest = 0;
  for (const record of records ?? []) {
    if (record?.action !== "program" || record?.result !== "success") continue;
    if (!/^\d{9}$/.test(record.unitNumber ?? "")) continue;
    highest = Math.max(highest, Number.parseInt(record.unitNumber, 10));
  }
  return formatUnitNumber(highest + 1);
}
