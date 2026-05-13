#!/usr/bin/env python3
"""
extract_voiceovers.py — Extract self.voiceover() strings from a manim script,
one per line, in order of appearance.

Usage:
    python extract_voiceovers.py -i scene.py              # prints to stdout
    python extract_voiceovers.py -i scene.py -o lines.txt # writes to file
"""

import argparse
import re
import sys
from pathlib import Path


def extract_voiceovers(path: str) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    pattern = re.compile(r"""self\.voiceover\(\s*(?:"([^"]+)"|'([^']+)')""")
    return [m.group(1) or m.group(2) for m in pattern.finditer(text)]


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("-i", "--input", required=True, help="Manim Python script")
    p.add_argument("-o", "--output", help="Output text file (default: stdout)")
    args = p.parse_args()

    lines = extract_voiceovers(args.input)
    if not lines:
        print("No self.voiceover() calls found.", file=sys.stderr)
        return 1

    text = "\n".join(lines)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {len(lines)} lines to {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
