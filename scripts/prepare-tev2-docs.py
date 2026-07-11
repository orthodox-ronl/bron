#!/usr/bin/env python3
"""Prepare a generated docs tree for TEV2 preprocessing."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


def _disable_git_plugin(mkdocs_path: Path) -> None:
    """Disable git-revision-date-localized in the generated mkdocs.yml.

    The git plugin looks up history by file path.  Files in generated/docs/ are
    TEV2-processed copies of docs/ and have no git history, so the plugin emits
    WARNING for every page.  MkDocs --strict turns those warnings into fatal
    errors.  Disabling the plugin here keeps the generated build clean while
    leaving the plugin active in the source mkdocs.yml for local `mkdocs serve`.
    """
    text = mkdocs_path.read_text(encoding="utf-8")
    patched, n = re.subn(
        r"^(\s*- git-revision-date-localized:)",
        r"\1\n      enabled: false",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n != 1:
        print("WARNING: could not disable git-revision-date-localized in generated mkdocs.yml", file=sys.stderr)
        return
    mkdocs_path.write_text(patched, encoding="utf-8")
    print("Disabled git-revision-date-localized plugin in generated mkdocs.yml")


def _patch_saf_website(generated_docs: Path, mkdocs_path: Path) -> None:
    """Patch saf.yaml website to match the site_url already set in mkdocs.yml.

    TRRT uses saf.yaml's `website` to build absolute navurls (e.g.
    https://orthodox-groningen.github.io/bron/preview/terms/representatie).
    The publication check then verifies those localized links start with the
    correct URL prefix.  When building for a preview branch the prefix is
    /bron/preview/, but a hardcoded production website value in saf.yaml would
    generate /bron/terms/... links that fail the check.  Patching only the
    staging copy keeps docs/saf.yaml untouched in the working tree.
    """
    mkdocs_text = mkdocs_path.read_text(encoding="utf-8")
    m = re.search(r"^site_url:\s*(\S+)", mkdocs_text, re.MULTILINE)
    if not m:
        print("WARNING: could not read site_url from mkdocs.yml", file=sys.stderr)
        return

    website = m.group(1).strip().rstrip("/")

    saf_path = generated_docs / "saf.yaml"
    if not saf_path.exists():
        return

    saf_text = saf_path.read_text(encoding="utf-8")
    saf_patched, n = re.subn(
        r"^(\s+website:\s*)\S+$",
        lambda hit: hit.group(1) + website,
        saf_text,
        count=1,
        flags=re.MULTILINE,
    )
    if n != 1:
        print("WARNING: could not patch website in saf.yaml", file=sys.stderr)
        return

    saf_path.write_text(saf_patched, encoding="utf-8")
    print(f"Patched saf.yaml website: {website}")


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
    mkdocs_dest = generated / "mkdocs.yml"
    shutil.copy2(root / "mkdocs.yml", mkdocs_dest)

    _patch_saf_website(generated_docs, mkdocs_dest)
    _disable_git_plugin(mkdocs_dest)

    print(f"Prepared TEV2 docs staging tree: {generated_docs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
