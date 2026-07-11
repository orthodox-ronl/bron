#!/usr/bin/env python3
"""Patch site_url, preview flag, and build_time in mkdocs.yml for CI builds."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) not in {3, 4, 5}:
        print(
            f"Usage: {sys.argv[0]} <site_url> <preview:true|false> [build_time [branch]]",
            file=sys.stderr,
        )
        return 2

    site_url = sys.argv[1].rstrip("/") + "/"
    preview = sys.argv[2].lower() in {"1", "true", "yes"}
    build_time = sys.argv[3] if len(sys.argv) >= 4 else ""
    branch = sys.argv[4] if len(sys.argv) >= 5 else ""

    path = Path("mkdocs.yml")
    text = path.read_text(encoding="utf-8")

    text, n_url = re.subn(
        r"^site_url:\s*.+$",
        f"site_url: {site_url}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n_url != 1:
        print("Could not patch site_url in mkdocs.yml", file=sys.stderr)
        return 1

    text, n_preview = re.subn(
        r"^  preview:\s*.*$",
        f"  preview: {str(preview).lower()}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n_preview != 1:
        print("Could not patch extra.preview in mkdocs.yml", file=sys.stderr)
        return 1

    text, n_time = re.subn(
        r'^  build_time:\s*.*$',
        f'  build_time: "{build_time}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n_time != 1:
        print("Could not patch extra.build_time in mkdocs.yml", file=sys.stderr)
        return 1

    text, n_branch = re.subn(
        r'^  branch:\s*.*$',
        f'  branch: "{branch}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n_branch != 1:
        print("Could not patch extra.branch in mkdocs.yml", file=sys.stderr)
        return 1

    path.write_text(text, encoding="utf-8")
    print(f"site_url={site_url} preview={preview} build_time={build_time!r} branch={branch!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
