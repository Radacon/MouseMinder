import assert from "node:assert/strict";
import { test } from "node:test";
import { formatUnitNumber, incrementUnitNumber, nextUnitNumber } from "../public/unit-number.js";

test("unit numbers are zero-padded to nine digits", () => {
  assert.equal(formatUnitNumber("3"), "000000003");
  assert.equal(formatUnitNumber("000000042"), "000000042");
});

test("unit number advances after success", () => {
  assert.equal(incrementUnitNumber("000000002"), "000000003");
  assert.equal(nextUnitNumber([
    { action: "program", result: "success", unitNumber: "000000001" },
    { action: "program", result: "failure", unitNumber: "000000099" },
    { action: "program", result: "success", unitNumber: "000000002" }
  ]), "000000003");
});

test("invalid unit numbers are rejected", () => {
  assert.throws(() => formatUnitNumber("unit-3"), /digits/i);
  assert.throws(() => formatUnitNumber("0"), /between/i);
});
