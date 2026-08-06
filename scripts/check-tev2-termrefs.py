from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TERMREF_RE = re.compile(
    r"(?:(?<=[^`\\])|^)"
    r"\[(?=[^@\n\]]+\]\([^@)]*@[:a-z0-9_-]*\))"
    r"(?P<showtext>[^@\n\]]+)\]"
    r"\((?:(?:(?P<type>[a-z0-9_-]*):)?)(?:(?P<term>[^@\n:#)]*?)?(?:#(?P<trait>[^@\n:#)]*))?)?@(?P<scopetag>[a-z0-9_-]*)(?::(?P<vsntag>[a-z0-9_-]*))?\)"
)


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def strip_yaml_frontmatter(text: str) -> tuple[str, int]:
    if not text.startswith("---"):
        return text, 0

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text, 0

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            offset = sum(len(part) for part in lines[: index + 1])
            return "".join(lines[index + 1 :]), offset

    return text, 0


def line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    previous_newline = text.rfind("\n", 0, index)
    column = index + 1 if previous_newline == -1 else index - previous_newline
    return line, column


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail when TEv2 TermRefs remain unresolved in generated Markdown."
    )
    parser.add_argument("root", type=Path, help="Generated Markdown root to inspect.")
    args = parser.parse_args()

    root = args.root
    if not root.is_dir():
        print(f"ERROR: generated Markdown root not found: {root}", file=sys.stderr)
        return 1

    findings: list[str] = []
    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        body, offset = strip_yaml_frontmatter(text)
        for match in TERMREF_RE.finditer(body):
            line, column = line_col(text, offset + match.start())
            findings.append(f"{path}:{line}:{column}: {match.group(0)}")

    if findings:
        print("ERROR: unresolved TEv2 TermRefs remain after TRRT:", file=sys.stderr)
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1

    print(f"OK: no unresolved TEv2 TermRefs in {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
