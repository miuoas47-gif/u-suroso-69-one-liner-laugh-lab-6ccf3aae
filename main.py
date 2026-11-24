#!/usr/bin/env python3
"""One-Liner Laugh Lab — a robot vacuum's excuse after eating a sock.

Writes one original funny line to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output), validates it, and reads it back to verify.
Deterministic: the same bytes on every run. Standard library only,
no network, no arguments.
"""

import os
import sys

LINE = "In my defence, the sock was already on the floor \u2014 and I am, legally speaking, a vacuum."


def main() -> int:
    if not (1 <= len(LINE) <= 200):
        print(f"error: line is {len(LINE)} characters, must be 1-200", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("error: line must not be only whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    with open(path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != LINE + "\n":
        print("error: read-back verification failed", file=sys.stderr)
        return 1
    # Gate check on the file itself, as the scorer sees it: one line of
    # 1-200 characters (trailing newline excluded), not only whitespace.
    gated = back[:-1] if back.endswith("\n") else back
    if not (1 <= len(gated) <= 200) or not gated.strip() or "\n" in gated:
        print("error: entry.txt fails the 1-200 character gate", file=sys.stderr)
        return 1

    print(f"Wrote entry.txt ({len(LINE)} characters): {LINE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
