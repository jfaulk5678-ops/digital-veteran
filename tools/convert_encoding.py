#!/usr/bin/env python3
"""
Scan the repo for text files with given extensions that are not valid UTF-8.
Optionally convert them to UTF-8 with a .bak backup.

Usage:
  python tools/convert_encoding.py       # lists files that are not UTF-8
  python tools/convert_encoding.py --convert  # convert found files to UTF-8 (creates .bak)
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

EXTS = {".py", ".md", ".txt", ".yml", ".yaml", ".json", ".rst", ".ini", ".cfg", ".csv"}
SKIP_DIRS = {".venv", "venv", ".git", "__pycache__"}

TRIED_ENCODINGS = ("utf-8", "utf-8-sig", "cp1252", "latin-1")


def find_text_files(root: Path):
    for p in root.rglob("*"):
        if p.is_file():
            parts = set(p.parts)
            if parts & SKIP_DIRS:
                continue
            if p.suffix.lower() in EXTS:
                yield p


def is_utf8(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8")
        return True
    except Exception:
        return False


def detect_encoding_and_read(path: Path):
    for enc in TRIED_ENCODINGS:
        try:
            return enc, path.read_text(encoding=enc)
        except Exception:
            continue
    return None, None


def convert_to_utf8(path: Path) -> bool:
    enc, text = detect_encoding_and_read(path)
    if enc is None:
        return False
    if enc == "utf-8":
        return True
    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)
    path.write_text(text, encoding="utf-8")
    return True


def main():
    root = Path(".").resolve()
    convert = "--convert" in sys.argv
    bad = []
    for f in find_text_files(root):
        if not is_utf8(f):
            bad.append(str(f))
    if not bad:
        print("")
        print("No non-UTF-8 text files found.")
        return 0
    print("Non-UTF-8 files:")
    for p in bad:
        print(p)
    if convert:
        print("\nConverting files (backups with .bak)...")
        converted = []
        failed = []
        for p in bad:
            ok = convert_to_utf8(Path(p))
            (converted if ok else failed).append(p)
        print(f"Converted: {len(converted)} files")
        if failed:
            print("Failed to convert:")
            for p in failed:
                print(p)
            return 2
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
