from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from catalogus.errors import AliasRegisterError
from catalogus.normalize import normalize_for_match


def default_register_path(*, bron_root: Path | None = None) -> Path:
    """Pad naar org-breed aliassen-register."""
    if bron_root is not None:
        return bron_root.resolve() / "catalogus" / "data" / "alias-blokken.yaml"
    repo_root = Path(__file__).resolve().parents[2]
    return repo_root / "catalogus" / "data" / "alias-blokken.yaml"


@dataclass(frozen=True)
class AliasBlokRegister:
    """In-memory aliassen-register: blok-id → synoniemset."""

    blokken: dict[str, frozenset[str]]
    _term_to_blok: dict[str, str]

    def blok_for_term(self, term: str) -> str | None:
        return self._term_to_blok.get(normalize_for_match(term))

    def expand_blok(self, blok_id: str) -> frozenset[str]:
        aliases = self.blokken.get(blok_id)
        if aliases is None:
            raise AliasRegisterError(f"Onbekend alias-blok '{blok_id}'")
        return aliases

    def expand_term(self, term: str) -> frozenset[str]:
        blok_id = self.blok_for_term(term)
        if blok_id is None:
            return frozenset({term})
        return self.expand_blok(blok_id)

    def expand_texts(self, texts: tuple[str, ...]) -> tuple[str, ...]:
        """Breid teksten uit via blokken; behoud volgorde, geen duplicaten."""
        seen: set[str] = set()
        result: list[str] = []
        for text in texts:
            for candidate in self.expand_term(text):
                key = normalize_for_match(candidate)
                if key in seen:
                    continue
                seen.add(key)
                result.append(candidate)
        return tuple(result)

    def validate(self) -> list[str]:
        """Retourneer validatiefouten (leeg = ok)."""
        errors: list[str] = []
        for blok_id, aliases in self.blokken.items():
            if not str(blok_id).strip():
                errors.append("Lege blok-id")
            if not aliases:
                errors.append(f"Blok '{blok_id}' heeft geen aliassen")
        return errors


def load_alias_register(path: Path) -> AliasBlokRegister:
    """Laad en valideer aliassen-register van schijf."""
    if not path.is_file():
        raise AliasRegisterError(f"Aliassen-register niet gevonden: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise AliasRegisterError(f"Verwacht yaml-mapping in {path}")

    blokken_raw = raw.get("blokken")
    if not isinstance(blokken_raw, dict):
        raise AliasRegisterError(f"Verwacht sleutel 'blokken' in {path}")

    blokken: dict[str, frozenset[str]] = {}
    term_to_blok: dict[str, str] = {}
    conflicts: list[str] = []

    for blok_id, entry in blokken_raw.items():
        blok_key = str(blok_id).strip()
        if not blok_key:
            conflicts.append("Lege blok-id in register")
            continue

        if not isinstance(entry, dict):
            conflicts.append(f"Blok '{blok_key}': verwacht mapping met 'aliassen'")
            continue

        aliases_raw = entry.get("aliassen")
        if not isinstance(aliases_raw, list) or not aliases_raw:
            conflicts.append(f"Blok '{blok_key}': 'aliassen' moet een niet-lege lijst zijn")
            continue

        members: list[str] = []
        seen_in_blok: set[str] = set()
        for item in aliases_raw:
            if not isinstance(item, str):
                conflicts.append(
                    f"Blok '{blok_key}': alias moet string zijn, got {type(item).__name__}"
                )
                continue
            text = item.strip()
            if not text:
                conflicts.append(f"Blok '{blok_key}': lege alias")
                continue
            norm = normalize_for_match(text)
            if norm in seen_in_blok:
                continue
            seen_in_blok.add(norm)
            members.append(text)

            existing_blok = term_to_blok.get(norm)
            if existing_blok is not None and existing_blok != blok_key:
                conflicts.append(
                    f"Alias '{text}' komt voor in blok '{existing_blok}' en '{blok_key}'"
                )
            term_to_blok[norm] = blok_key

        if members:
            blokken[blok_key] = frozenset(members)

    if conflicts:
        raise AliasRegisterError(
            f"Aliassen-register {path} bevat {len(conflicts)} fout(en):\n"
            + "\n".join(f"  - {c}" for c in conflicts)
        )

    register = AliasBlokRegister(blokken=blokken, _term_to_blok=term_to_blok)
    errors = register.validate()
    if errors:
        raise AliasRegisterError(
            f"Aliassen-register {path} is ongeldig:\n"
            + "\n".join(f"  - {e}" for e in errors)
        )
    return register


def try_load_alias_register(
    path: Path | None = None, *, bron_root: Path | None = None
) -> AliasBlokRegister | None:
    """Laad register indien aanwezig; anders None (geen fout)."""
    resolved = path if path is not None else default_register_path(bron_root=bron_root)
    if not resolved.is_file():
        return None
    return load_alias_register(resolved)
