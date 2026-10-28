#!/usr/bin/env python3
"""Create deterministic MouseMinder PMS150C release metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


TAG_RE = re.compile(r"^firmware-v(?P<version>[0-9]+\.[0-9]+\.[0-9]+(?:[.-][0-9A-Za-z.-]+)?)$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
BINARY_NAME = "slowclocksleep_PMS150C.bin"
MANIFEST_NAME = "mouseminder-firmware.json"
CHECKSUM_NAME = f"{BINARY_NAME}.sha256"
LEGAL_WORDS = 0x3F6
ERASED_WORD = 0x1FFF
HOST_BLANK_WORD = 0xFFFF


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--sdcc-version", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def inspect_binary(data: bytes) -> tuple[int, int]:
    if not data or len(data) % 2:
        raise ValueError("PMS150C binary must contain complete 16-bit word containers")
    if len(data) > LEGAL_WORDS * 2:
        raise ValueError("PMS150C binary reaches excluded program words")

    last_used = -1
    for address in range(len(data) // 2):
        word = int.from_bytes(data[address * 2 : address * 2 + 2], "little")
        if word == HOST_BLANK_WORD:
            continue
        if word & ~ERASED_WORD:
            raise ValueError(f"word 0x{address:03X} exceeds 13 bits")
        last_used = address
    if last_used < 0:
        raise ValueError("binary contains no programmed words")
    if last_used + 1 != len(data) // 2:
        raise ValueError("release binary must not contain trailing host blank words")
    return len(data) // 2, last_used


def main() -> None:
    args = parse_args()
    tag_match = TAG_RE.fullmatch(args.tag)
    if not tag_match:
        raise ValueError("tag must use firmware-vMAJOR.MINOR.PATCH")
    commit = args.commit.lower()
    if not COMMIT_RE.fullmatch(commit):
        raise ValueError("commit must be a full 40-character lowercase Git hash")

    data = args.binary.read_bytes()
    words, last_used = inspect_binary(data)
    digest = hashlib.sha256(data).hexdigest()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / BINARY_NAME).write_bytes(data)
    (args.output / CHECKSUM_NAME).write_text(f"{digest}  {BINARY_NAME}\n", encoding="ascii")

    manifest = {
        "schema": "mouseminder-firmware-release/v1",
        "release": {
            "tag": args.tag,
            "version": tag_match.group("version"),
            "commit": commit,
        },
        "target": {
            "device": "PMS150C",
            "architecture": "pdk13",
            "code_bits": 13,
            "code_words": 0x400,
            "legal_words": LEGAL_WORDS,
            "excluded_start_word": LEGAL_WORDS,
            "excluded_end_word": 0x400,
            "word_encoding": "little-endian-16-bit-containers",
            "erased_word": "1FFF",
        },
        "firmware": {
            "asset_name": BINARY_NAME,
            "bytes": len(data),
            "words": words,
            "last_used_word": f"{last_used:03X}",
            "sha256": digest,
        },
        "calibration": {
            "type": "ILRC",
            "frequency_hz": 52000,
            "vdd_mv": 2800,
        },
        "toolchain": {
            "sdcc": args.sdcc_version.strip(),
            "source_directory": "codebase/VSCODE_FreePDK",
            "build_command": "make clean build",
        },
    }
    (args.output / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
