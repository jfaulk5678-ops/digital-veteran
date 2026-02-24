#!/usr/bin/env python3
"""
Find problematic files (same rules as find_problematic_files.py) and convert them to UTF-8 with .bak backups.
"""

import sys
from pathlib import Path

SKIP_DIRS = {".venv", "venv", ".git", "__pycache__"}
root = Path(".").resolve()
TRIED_ENCODINGS = ("utf-8", "utf-8-sig", "utf-16", "cp1252", "latin-1")

problematic = []
for p in root.rglob("*"):
    try:
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        with p.open("rb") as fh:
            head = fh.read(4096)
        if not head:
            continue
        try:
            head.decode("utf-8")
            continue
        except Exception:
            problematic.append(p)
    except Exception:
        continue

if not problematic:
    print("No problematic files to convert.")
    sys.exit(0)

converted = []
failed = []
for p in problematic:
    success = False
    for enc in TRIED_ENCODINGS:
        try:
            text = p.read_text(encoding=enc)
            # backup
            bak = p.with_suffix(p.suffix + ".bak")
            p.rename(bak)
            p.write_text(text, encoding="utf-8")
            print(f"Converted {p} (from {enc}) -> backup at {bak}")
            converted.append(str(p))
            success = True
            break
        except Exception as e:
            continue
    if not success:
        print(f"Failed to convert {p}")
        failed.append(str(p))

if failed:
    print("Some files failed to convert:")
    for f in failed:
        print(f)
    sys.exit(2)
print(f"Converted {len(converted)} files successfully.")
sys.exit(0)
