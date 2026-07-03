"""Synchroniseer zangstuk.yaml met VSA-frontmatter (frontmatter is leidend)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_VSA_SRC = Path(__file__).resolve().parents[2] / "VSA-tooling" / "src"
if not _VSA_SRC.is_dir():
    _VSA_SRC = Path(__file__).resolve().parents[1].parent / "VSA-tooling" / "src"
if _VSA_SRC.is_dir() and str(_VSA_SRC) not in sys.path:
    sys.path.insert(0, str(_VSA_SRC))

from vsa.yaml_frontmatter import parse_vsa_frontmatter  # noqa: E402

OCCASION = "Zondag (opstandingscyclus)"


def _tone_from_id(zangstuk_id: str) -> int:
    m = re.search(r"-toon-(\d+)$", zangstuk_id)
    if not m:
        raise ValueError(f"Geen toon in id: {zangstuk_id}")
    return int(m.group(1))


def _scan_sources(zangstuk_id: str, scan_dir: Path) -> list[tuple[str, str]]:
    tone = _tone_from_id(zangstuk_id)
    files = {p.name for p in scan_dir.glob("*.jpg")}
    primary_name = "koormap-5.jpg" if tone == 5 else "koormap.jpg"

    sources: list[tuple[str, str]] = []
    if primary_name in files:
        sources.append(("koormap-scan", f"sources/scan/{primary_name}"))

    for name in sorted(files):
        if name == primary_name:
            continue
        sources.append(("koormap-scan-alt", f"sources/scan/{name}"))
    return sources


def _format_vsa_zangstuk(zangstuk_id: str, ident: dict) -> str:
    tone = int(ident["tone"])
    lines = [
        f"id: {zangstuk_id}",
        f"title: {ident['title']}",
        f"gelegenheid: {OCCASION}",
        "gelegenheidstype: zondag-cyclus",
        f"toon: {tone}",
        "sources:",
        "  - id: groningen",
        "    file: sources/vsa/groningen.vsa",
        "    author: Parochie Groningen",
        f"    composer: {ident['composer']}",
        f"    reference: {ident['bron']}",
        f"    language: {ident['language']}",
        "    copyright_status: vrij",
    ]
    return "\n".join(lines) + "\n"


def _format_melodie_zangstuk(zangstuk_id: str, tone: int, sources: list[tuple[str, str]]) -> str:
    lines = [
        f"id: {zangstuk_id}",
        f"title: Tropaarmelodie van de zondag, toon {tone}",
        f"gelegenheid: {OCCASION}",
        "gelegenheidstype: zondag-cyclus",
        f"toon: {tone}",
        "sources:",
    ]
    for sid, rel in sources:
        lines.extend(
            [
                f"  - id: {sid}",
                f"    file: {rel}",
                "    reference: koormap Groningen",
                "    copyright_status: vrij",
            ]
        )
    return "\n".join(lines) + "\n"


def sync_zangstukken(root: Path) -> int:
    updated = 0
    for zdir in sorted(root.iterdir()):
        if not zdir.is_dir():
            continue
        zangstuk_id = zdir.name
        yaml_path = zdir / "zangstuk.yaml"
        vsa_path = zdir / "sources" / "vsa" / "groningen.vsa"
        scan_dir = zdir / "sources" / "scan"

        if vsa_path.is_file():
            fm, _ = parse_vsa_frontmatter(vsa_path.read_text(encoding="utf-8"))
            ident = fm.get("identificatie") or {}
            new_text = _format_vsa_zangstuk(zangstuk_id, ident)
        elif zangstuk_id.startswith("troparion-melodie-toon-") and scan_dir.is_dir():
            tone = _tone_from_id(zangstuk_id)
            sources = _scan_sources(zangstuk_id, scan_dir)
            new_text = _format_melodie_zangstuk(zangstuk_id, tone, sources)
        else:
            continue

        if not yaml_path.is_file() or yaml_path.read_text(encoding="utf-8") != new_text:
            yaml_path.write_text(new_text, encoding="utf-8")
            print(f"updated: {zangstuk_id}")
            updated += 1
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--zangstukken-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "zangstukken",
    )
    args = parser.parse_args()
    count = sync_zangstukken(args.zangstukken_root.resolve())
    print(f"Klaar: {count} bestand(en) bijgewerkt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
