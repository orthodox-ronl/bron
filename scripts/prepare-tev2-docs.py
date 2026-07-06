#!/usr/bin/env python3
"""Prepare a generated docs tree for TEV2 preprocessing."""

from __future__ import annotations

import shutil
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    source_docs = root / "docs"
    generated = root / "generated"
    generated_docs = generated / "docs"

    if generated.exists():
        shutil.rmtree(generated)
    generated.mkdir(exist_ok=True)

    ignore = shutil.ignore_patterns("__pycache__", ".pytest_cache")
    shutil.copytree(source_docs, generated_docs, ignore=ignore)
    shutil.copy2(root / "mkdocs.yml", generated / "mkdocs.yml")

    print(f"Prepared TEV2 docs staging tree: {generated_docs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
