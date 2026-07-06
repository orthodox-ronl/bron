#!/usr/bin/env python3
"""Sort generated Markdown glossary table rows by their first column."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$"
)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")


def split_markdown_table_row(row: str) -> list[str]:
    """Split a Markdown table row, preserving escaped pipes inside cells."""
    text = row.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False

    for char in text:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            current.append(char)
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)

    cells.append("".join(current).strip())
    return cells


def sort_key(row: str) -> str:
    first_cell = split_markdown_table_row(row)[0]
    link = MARKDOWN_LINK_RE.search(first_cell)
    label = link.group(1) if link else first_cell
    label = HTML_TAG_RE.sub("", label)
    label = label.replace("`", "")
    return label.casefold()


def sort_tables(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        if (
            i + 1 < len(lines)
            and lines[i].lstrip().startswith("|")
            and TABLE_SEPARATOR_RE.match(lines[i + 1])
        ):
            out.append(lines[i])
            out.append(lines[i + 1])
            i += 2

            rows: list[str] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(lines[i])
                i += 1

            out.extend(sorted(rows, key=sort_key))
            continue

        out.append(lines[i])
        i += 1

    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="generated/docs/glossary.md",
        help="Generated glossary markdown file to sort",
    )
    args = parser.parse_args()

    path = Path(args.path)
    original = path.read_text(encoding="utf-8")
    path.write_text(sort_tables(original), encoding="utf-8")
    print(f"Sorted glossary table rows: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
