#!/usr/bin/env python3
"""News-image entry for make.fun bounty news-image-20261119.

Sum up 19 November 2026 world news in one image. The image is drawn
by generate_image.py (Pillow, build time only) and stored in this
repository as entry.png. This program is stdlib-only: it copies that
image to the grader's output directory, so it runs with no network,
no extra packages, and writes byte-identical output on every run.

Usage (local):  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
Grader:        python3 -P -s /bot/main.py  (MAKEFUN_OUTPUT_DIR=/output)
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    src = HERE / "entry.png"
    if not src.is_file():
        print("entry.png missing", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # copyfile is deterministic: same input bytes, same output bytes.
    shutil.copyfile(src, out_dir / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
