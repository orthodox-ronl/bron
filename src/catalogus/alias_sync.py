from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from catalogus.alias_blokken import AliasBlokRegister, default_register_path, load_alias_register
from catalogus.errors import AliasSyncError
from catalogus.normalize import normalize_for_match

GENERATED_MARKER = re.compile(
    r"^\s*#\s*gegenereerd:\s*alias-blok\s+(.+?)\s*(?:—|-)\s*niet handmatig bewerken\s*$"
)
LIST_ITEM = re.compile(r"^(\s*)-\s+(.*)$")
TOP_LEVEL_KEY = re.compile(r"^[A-Za-z_].*:\s*")

_NO_TERM_FALLBACK_PREFIXES = (
    "troparion-melodie-",
    "troparion-melodie",
)


@dataclass(frozen=True)
class SyncTarget:
    path: Path
    zangstuk_id: str
    kind: str  # "zangstuk" | "variant"


@dataclass
class SyncResult:
    path: Path
    changed: bool
    blok_id: str | None = None
    skipped: bool = False
    reason: str = ""


def slugify_blok_id(blok_id: str) -> str:
    return normalize_for_match(blok_id).replace(" ", "-")


def resolve_blok_id(
    data: dict,
    zangstuk_id: str,
    register: AliasBlokRegister,
    *,
    context: str,
) -> str | None:
    """Bepaal alias-blok voor manifest (expliciet veld, slug-prefix, term-fallback)."""
    for key in ("liturgische_rol", "alias_blok"):
        raw = data.get(key)
        if raw is None or str(raw).strip() == "":
            continue
        blok = str(raw).strip()
        if blok in register.blokken:
            return blok
        raise AliasSyncError(
            f"Onbekend alias-blok '{blok}' ({key}) in {context}"
        )

    zid = zangstuk_id.strip()
    best: tuple[int, str] | None = None
    for blok_id in register.blokken:
        slug = slugify_blok_id(blok_id)
        if not slug:
            continue
        if zid == slug or zid.startswith(slug + "-"):
            if best is None or len(slug) > best[0]:
                best = (len(slug), blok_id)
    if best is not None:
        return best[1]

    for prefix in _NO_TERM_FALLBACK_PREFIXES:
        if zid == prefix.rstrip("-") or zid.startswith(prefix):
            return None

    first = zid.split("-", 1)[0]
    return register.blok_for_term(first)


def _alias_item_norm(item: str) -> str | None:
    text = item.strip()
    if not text:
        return None
    if text.startswith("{") and "text:" in text:
        m = re.search(r'text:\s*["\']?([^"\'}]+)', text)
        if m:
            return normalize_for_match(m.group(1))
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        text = text[1:-1]
    return normalize_for_match(text)


def _format_alias_line(indent: str, item: str) -> str:
    stripped = item.strip()
    if stripped.startswith("- "):
        stripped = stripped[2:].strip()
    if stripped.startswith("{") or stripped.startswith('"') or stripped.startswith("'"):
        return f"{indent}- {stripped}"
    if re.search(r"[:\#\[\]\{\}]", stripped):
        return f'{indent}- "{stripped}"'
    return f"{indent}- {stripped}"


def _parse_aliases_block(lines: list[str], start: int) -> tuple[list[str], str | None, int]:
    manual: list[str] = []
    blok_id: str | None = None
    in_generated = False
    i = start + 1

    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            i += 1
            continue
        if TOP_LEVEL_KEY.match(line) and not line.startswith(" "):
            break
        marker = GENERATED_MARKER.match(line)
        if marker:
            in_generated = True
            blok_id = marker.group(1).strip()
            i += 1
            continue
        match = LIST_ITEM.match(line)
        if match:
            item_text = match.group(2).strip()
            if not in_generated:
                manual.append(item_text)
            i += 1
            continue
        if line.lstrip().startswith("#"):
            i += 1
            continue
        break

    return manual, blok_id, i


def _build_aliases_lines(
    *,
    indent: str,
    manual: list[str],
    generated: list[str],
    blok_id: str,
) -> list[str]:
    out = [f"{indent.rstrip()}aliases:"]
    for item in manual:
        out.append(_format_alias_line(indent + "  ", item))
    if generated:
        out.append(
            f"{indent}  # gegenereerd: alias-blok {blok_id} — niet handmatig bewerken"
        )
        for item in generated:
            out.append(_format_alias_line(indent + "  ", item))
    return out


def _dedupe_manual(manual: list[str], generated: list[str]) -> list[str]:
    gen_norms = {_alias_item_norm(g) for g in generated}
    gen_norms.discard(None)
    kept: list[str] = []
    for item in manual:
        norm = _alias_item_norm(item)
        if norm is not None and norm in gen_norms:
            continue
        kept.append(item)
    return kept


def parse_generated_aliases(path: Path) -> list[str]:
    """Lees alias-termen uit het gegenereerde blok (tekst-marker in yaml)."""
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    aliases_start: int | None = None
    for i, line in enumerate(lines):
        bare = line.strip()
        if bare == "aliases:" or bare.startswith("aliases:"):
            aliases_start = i
            break
    if aliases_start is None:
        return []

    generated: list[str] = []
    in_generated = False
    for line in lines[aliases_start + 1 :]:
        if line.strip() == "":
            continue
        if TOP_LEVEL_KEY.match(line) and not line.startswith(" "):
            break
        marker = GENERATED_MARKER.match(line)
        if marker:
            in_generated = True
            continue
        match = LIST_ITEM.match(line)
        if match:
            if in_generated:
                generated.append(match.group(2).strip())
            continue
        if line.lstrip().startswith("#"):
            continue
        if in_generated:
            break
    return generated


def partition_yaml_aliases(
    path: Path, aliases: list[object]
) -> tuple[list[object], list[str]]:
    """Scheid handmatige resolver-aliassen van gegenereerde zoek-aliassen."""
    generated_raw = parse_generated_aliases(path)
    if not generated_raw:
        return aliases, []
    gen_norms = {_alias_item_norm(g) for g in generated_raw}
    gen_norms.discard(None)
    manual: list[object] = []
    for item in aliases:
        if isinstance(item, str):
            norm = _alias_item_norm(item)
            if norm is not None and norm in gen_norms:
                continue
        manual.append(item)
    return manual, generated_raw


def _find_aliases_insert_index(plain_lines: list[str]) -> int:
    """Index vóór aliases: — preferentie vóór sources:, anders na metadata."""
    for i, line in enumerate(plain_lines):
        bare = line.strip()
        if bare == "sources:" or bare.startswith("sources:"):
            return i
    insert_at = 0
    for i, line in enumerate(plain_lines):
        bare = line.strip()
        if TOP_LEVEL_KEY.match(line) and not line.startswith(" "):
            insert_at = i + 1
    return insert_at


def sync_aliases_in_text(
    text: str,
    *,
    blok_id: str,
    register: AliasBlokRegister,
) -> tuple[str, bool]:
    generated = sorted(register.expand_blok(blok_id), key=normalize_for_match)
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] = lines[-1] + "\n"

    aliases_start: int | None = None
    for i, line in enumerate(lines):
        bare = line.rstrip("\n")
        if bare == "aliases:" or bare.startswith("aliases:"):
            aliases_start = i
            break

    if aliases_start is None:
        plain_lines = [ln.rstrip("\n") for ln in lines]
        insert_at = _find_aliases_insert_index(plain_lines)
        new_block = [ln + "\n" for ln in _build_aliases_lines(
            indent="",
            manual=[],
            generated=generated,
            blok_id=blok_id,
        )]
        new_lines = lines[:insert_at] + new_block + lines[insert_at:]
        return "".join(new_lines), True

    plain_lines = [ln.rstrip("\n") for ln in lines]
    manual, _old_blok, end = _parse_aliases_block(plain_lines, aliases_start)
    manual = _dedupe_manual(manual, generated)
    new_block = _build_aliases_lines(
        indent="",
        manual=manual,
        generated=generated,
        blok_id=blok_id,
    )
    new_block_lines = [ln + "\n" for ln in new_block]
    new_lines = lines[:aliases_start] + new_block_lines + lines[end:]
    new_text = "".join(new_lines)
    old_text = "".join(lines)
    return new_text, new_text != old_text


def _load_manifest(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AliasSyncError(f"Verwacht yaml-mapping in {path}")
    return data


def sync_manifest_file(
    target: SyncTarget,
    register: AliasBlokRegister,
    *,
    dry_run: bool = False,
) -> SyncResult:
    data = _load_manifest(target.path)
    zangstuk_id = str(data.get("zangstuk-id", data.get("id", target.zangstuk_id)))
    blok_id = resolve_blok_id(
        data, zangstuk_id, register, context=str(target.path)
    )
    if blok_id is None:
        return SyncResult(
            path=target.path,
            changed=False,
            skipped=True,
            reason="geen alias-blok trigger",
        )

    text = target.path.read_text(encoding="utf-8")
    new_text, changed = sync_aliases_in_text(
        text, blok_id=blok_id, register=register
    )
    if changed and not dry_run:
        target.path.write_text(new_text, encoding="utf-8", newline="\n")
    return SyncResult(path=target.path, changed=changed, blok_id=blok_id)


def iter_sync_targets(
    *,
    bron_root: Path | None = None,
    content_root: Path | None = None,
) -> list[SyncTarget]:
    targets: list[SyncTarget] = []
    if bron_root is not None:
        root = bron_root.resolve()
        zangstukken = root / "zangstukken"
        if zangstukken.is_dir():
            for zdir in sorted(p for p in zangstukken.iterdir() if p.is_dir()):
                yaml_path = zdir / "zangstuk.yaml"
                if yaml_path.is_file():
                    targets.append(
                        SyncTarget(
                            path=yaml_path,
                            zangstuk_id=zdir.name,
                            kind="zangstuk",
                        )
                    )
    if content_root is not None:
        lokaal = content_root.resolve() / "lokaal"
        if lokaal.is_dir():
            for zdir in sorted(p for p in lokaal.iterdir() if p.is_dir()):
                for vdir in sorted(p for p in zdir.iterdir() if p.is_dir()):
                    yaml_path = vdir / "variant.yaml"
                    if yaml_path.is_file():
                        targets.append(
                            SyncTarget(
                                path=yaml_path,
                                zangstuk_id=zdir.name,
                                kind="variant",
                            )
                        )
    return targets


def run_alias_sync(
    *,
    register: AliasBlokRegister,
    bron_root: Path | None = None,
    content_root: Path | None = None,
    dry_run: bool = False,
    check: bool = False,
) -> list[SyncResult]:
    results: list[SyncResult] = []
    for target in iter_sync_targets(
        bron_root=bron_root, content_root=content_root
    ):
        results.append(
            sync_manifest_file(target, register, dry_run=dry_run or check)
        )
    return results


def load_register_for_sync(
    *,
    register_path: Path | None = None,
    bron_root: Path | None = None,
) -> AliasBlokRegister:
    path = register_path
    if path is None:
        path = default_register_path(bron_root=bron_root)
    return load_alias_register(path)
