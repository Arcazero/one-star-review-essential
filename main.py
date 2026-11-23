#!/usr/bin/env python3
"""One-Star Review of Something Essential — make.fun entry.

Reads the single one-star review from review.txt (kept beside
this script), validates it, and writes it to /output/entry.txt: the line
plus one trailing newline, byte-identical to review.txt.
"""

import os
import sys

# Resolve review.txt against this script's own directory, not the process
# working directory: the grader runs the program with a different cwd,
# and a bare relative path would fail to find the file there.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REVIEW_PATH = os.path.join(SCRIPT_DIR, "review.txt")


def load_review() -> str:
    """Read and validate the review from review.txt next to this script."""
    with open(REVIEW_PATH, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    if not text.endswith("\n"):
        raise ValueError("review.txt must end with exactly one trailing newline")
    review = text[:-1]
    if not review:
        raise ValueError("review is empty")
    if review != review.strip():
        raise ValueError("review has leading or trailing whitespace")
    if "\n" in review or "\r" in review:
        raise ValueError("review must be a single line")
    if len(review) > 159:
        # Cap at 159, not 160: entry.txt holds the review plus one trailing
        # newline, and the gate counts the file at 1 to 160 characters.
        raise ValueError("review is over 159 characters")
    if text != review + "\n":
        raise ValueError("review.txt must be exactly one line plus one newline")
    return review


def main() -> None:
    review = load_review()
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(review + "\n")
    # Prove the output is byte-identical to review.txt before reporting success.
    with open(path, "rb") as f:
        written = f.read()
    with open(REVIEW_PATH, "rb") as f:
        source = f.read()
    if written != source:
        raise ValueError("output is not byte-identical to review.txt")
    print(review)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
