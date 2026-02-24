#!/usr/bin/env python3
"""
Find files that may cause `black` UnicodeDecodeError: files that start with BOM bytes
or are not decodable as UTF-8 in their first 4KB. Skips .venv, venv, .git.
"""

import sys
from pathlib import Path

SKIP_DIRS = {".venv", "venv", ".git", "__pycache__"}
root = Path(".").resolve()
problematic = []
for p in root.rglob("*"):
    try:
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        # read the first chunk
        with p.open("rb") as fh:
            head = fh.read(4096)
        if not head:
            continue
        # check for UTF-16/UTF-32 BOMs or 0xff/0xfe at start
        if head.startswith(b"\xff\xfe") or head.startswith(b"\xfe\xff"):
            problematic.append((str(p), "UTF-16 BOM"))
            continue
        if head.startswith(b"\x00\x00\xfe\xff") or head.startswith(b"\xff\xfe\x00\x00"):
            problematic.append((str(p), "UTF-32 BOM"))
            continue
        # try to decode first chunk as utf-8
        try:
            head.decode("utf-8")
        except Exception as e:
            problematic.append((str(p), f"not-utf8: {e}"))
    except Exception:
        continue

if not problematic:
    print("No problematic files found.")
    sys.exit(0)

print("Problematic files:")
for p, reason in problematic:
    print(p + " -- " + reason)
sys.exit(2)
