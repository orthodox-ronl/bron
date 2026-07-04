"""Catalogus zoek-API.

Normatief: docs/specs/catalogus-zoek-api.md
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from catalogus.alias_index import AliasIndex, VsaFileEntry, ZoekIndexEntry
from catalogus.errors import AmbiguousError, MatchCandidate, NotFoundError
from catalogus.normalize import normalize_for_match

ZOEK_NIVEAU = "zoek"
_DEFAULT_BESTANDSEXTENSIE: frozenset[str] = frozenset({".vsa"})
_VALID_BRONNEN: frozenset[str] = frozenset({"bron", "lokaal"})
_SPEC_DOC = "docs/specs/catalogus-zoek-api.md"
_QUERY_SPLIT_RE = re.compile(r"[\s\-_/(),]+")


@dataclass(frozen=True)
class ZoekContext:
    """Liturgische context voor catalogus-zoekactie (mirror ``default.*``)."""

    gelegenheid: str | None = None
    gelegenheidstype: str | None = None
    toon: str | None = None
    uitvoeringsvorm: str | None = None
    gelegenheidsdatum: str | None = None
    referentie: str | None = None
    bronnen: frozenset[str] = frozenset({"bron", "lokaal"})

    @classmethod
    def from_default_mapping(
        cls,
        default: dict | None,
        *,
        bronnen: Iterable[str] | str | None = None,
    ) -> ZoekContext:
        data = default if isinstance(default, dict) else {}
        return cls(
            gelegenheid=_optional_str(data.get("gelegenheid")),
            gelegenheidstype=_optional_str(data.get("gelegenheidstype")),
            toon=_optional_str(data.get("toon")),
            uitvoeringsvorm=_optional_str(data.get("uitvoeringsvorm")),
            gelegenheidsdatum=_optional_str(data.get("gelegenheidsdatum")),
            referentie=_optional_str(data.get("referentie")),
            bronnen=_parse_bronnen(bronnen),
        )


@dataclass(frozen=True)
class ZoekMatch:
    """Één kandidaat na query-, context- en bestandsextensie-filter."""

    entry: VsaFileEntry
    catalogus_pad: str


@dataclass(frozen=True)
class ZoekLijstResult:
    """Alle matches voor een zoekactie (0..n)."""

    query: str
    query_normalized: str
    matches: tuple[ZoekMatch, ...]
    ook_gevonden_in_bron: tuple[str, ...] = ()

    @property
    def catalogus_paden(self) -> list[str]:
        return [match.catalogus_pad for match in self.matches]


@dataclass(frozen=True)
class ZoekResult:
    """Resultaat van één unieke catalogus-zoekactie (strict modus)."""

    query: str
    query_normalized: str
    entry: VsaFileEntry
    catalogus_pad: str
    ook_gevonden_in_bron: tuple[str, ...] = ()

    @property
    def path(self) -> Path:
        return self.entry.path

    @property
    def has_ook_in_bron(self) -> bool:
        return bool(self.ook_gevonden_in_bron)


def format_catalogus_pad(entry: VsaFileEntry) -> str:
    """Formatteer ``VsaFileEntry`` als logische referentie ``lokaal:…`` / ``bron:…``."""
    if entry.origin not in _VALID_BRONNEN:
        raise ValueError(f"Onbekende herkomst: {entry.origin!r}")

    segments = [
        entry.zangstuk_id,
        entry.variant_id,
        entry.uitvoeringsvorm_id,
    ]
    if entry.representatie_id != entry.uitvoeringsvorm_id:
        segments.append(entry.representatie_id)

    return f"{entry.origin}:{'/'.join(segments)}"


def parse_bestandsextensie(
    value: Iterable[str] | str | None,
) -> frozenset[str] | None:
    """Parse CLI/API-waarde naar suffix-set (``vsa`` → ``{".vsa"}``; ``alle`` → ``None``)."""
    if value is None:
        return _DEFAULT_BESTANDSEXTENSIE
    if isinstance(value, str):
        stripped = value.strip().lower()
        if not stripped or stripped == "vsa":
            return _DEFAULT_BESTANDSEXTENSIE
        if stripped == "alle":
            return None
        items = [part.strip() for part in stripped.split(",") if part.strip()]
    else:
        items = [str(item).strip() for item in value if str(item).strip()]
    if not items:
        return _DEFAULT_BESTANDSEXTENSIE
    return frozenset(
        item if item.startswith(".") else f".{item.lower()}" for item in items
    )


def zoek_kandidaten(
    query: str,
    *,
    index: AliasIndex,
    context: ZoekContext | None = None,
    bestandsextensie: frozenset[str] | None = _DEFAULT_BESTANDSEXTENSIE,
) -> ZoekLijstResult:
    """Zoek alle brondocument-kandidaten op vrije tekst + context.

    Raises:
        ValueError: lege query.
    """
    normalized_query = _require_query(query)
    ctx = context or ZoekContext()
    query_tokens = _query_tokens(normalized_query)

    lokaal_matches: list[ZoekMatch] = []
    bron_matches: list[ZoekMatch] = []

    for zoek_entry in index.zoek_entries:
        if zoek_entry.entry.origin not in ctx.bronnen:
            continue
        if not _matches_bestandsextensie(zoek_entry.entry.path, bestandsextensie):
            continue
        if not _matches_query(zoek_entry, query_tokens, normalized_query):
            continue
        if not _matches_context(zoek_entry, ctx, index):
            continue
        match = ZoekMatch(
            entry=zoek_entry.entry,
            catalogus_pad=format_catalogus_pad(zoek_entry.entry),
        )
        if zoek_entry.entry.origin == "lokaal":
            lokaal_matches.append(match)
        else:
            bron_matches.append(match)

    if lokaal_matches:
        winning = _dedupe_matches(lokaal_matches)
        ook_in_bron = tuple(
            sorted({match.catalogus_pad for match in _dedupe_matches(bron_matches)})
        )
    elif bron_matches:
        winning = _dedupe_matches(bron_matches)
        ook_in_bron = ()
    else:
        winning = ()
        ook_in_bron = ()

    return ZoekLijstResult(
        query=query.strip(),
        query_normalized=normalized_query,
        matches=winning,
        ook_gevonden_in_bron=ook_in_bron,
    )


def zoek_kandidaten_met_roots(
    query: str,
    *,
    content_root: Path | None = None,
    bron_root: Path | None = None,
    fixture_root: Path | None = None,
    context: ZoekContext | None = None,
    bestandsextensie: frozenset[str] | None = _DEFAULT_BESTANDSEXTENSIE,
) -> ZoekLijstResult:
    """Bouw ``AliasIndex`` uit roots en roep ``zoek_kandidaten`` aan."""
    if not any((content_root, bron_root, fixture_root)):
        raise ValueError(
            "Minstens één van content_root, bron_root of fixture_root is verplicht"
        )
    index = AliasIndex.build(
        content_root=content_root,
        bron_root=bron_root,
        fixture_root=fixture_root,
    )
    return zoek_kandidaten(
        query,
        index=index,
        context=context,
        bestandsextensie=bestandsextensie,
    )


def zoek(
    query: str,
    *,
    index: AliasIndex,
    context: ZoekContext | None = None,
    bestandsextensie: frozenset[str] | None = _DEFAULT_BESTANDSEXTENSIE,
) -> ZoekResult:
    """Zoek één brondocument op vrije tekst + context (strict).

    Raises:
        ValueError: lege query.
        NotFoundError: geen match.
        AmbiguousError: meerdere matches.
    """
    _require_query(query)
    lijst = zoek_kandidaten(
        query,
        index=index,
        context=context,
        bestandsextensie=bestandsextensie,
    )
    return _zoek_from_lijst(lijst)


def zoek_met_roots(
    query: str,
    *,
    content_root: Path | None = None,
    bron_root: Path | None = None,
    fixture_root: Path | None = None,
    context: ZoekContext | None = None,
    bestandsextensie: frozenset[str] | None = _DEFAULT_BESTANDSEXTENSIE,
) -> ZoekResult:
    """Bouw ``AliasIndex`` uit roots en roep ``zoek`` aan."""
    if not any((content_root, bron_root, fixture_root)):
        raise ValueError(
            "Minstens één van content_root, bron_root of fixture_root is verplicht"
        )
    index = AliasIndex.build(
        content_root=content_root,
        bron_root=bron_root,
        fixture_root=fixture_root,
    )
    return zoek(
        query,
        index=index,
        context=context,
        bestandsextensie=bestandsextensie,
    )


def _zoek_from_lijst(lijst: ZoekLijstResult) -> ZoekResult:
    """Strict modus: precies één match uit ``ZoekLijstResult``."""
    scope = f"query={lijst.query!r}"
    if not lijst.matches:
        raise NotFoundError(ZOEK_NIVEAU, lijst.query, scope)
    if len(lijst.matches) > 1:
        candidates = [
            MatchCandidate(canonical_id=match.catalogus_pad, context=match.catalogus_pad)
            for match in lijst.matches
        ]
        raise AmbiguousError(ZOEK_NIVEAU, lijst.query, candidates, scope)
    match = lijst.matches[0]
    return ZoekResult(
        query=lijst.query,
        query_normalized=lijst.query_normalized,
        entry=match.entry,
        catalogus_pad=match.catalogus_pad,
        ook_gevonden_in_bron=lijst.ook_gevonden_in_bron,
    )


def _require_query(query: str) -> str:
    stripped = query.strip()
    if not stripped:
        raise ValueError("Zoekquery mag niet leeg zijn")
    return normalize_for_match(stripped)


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _parse_bronnen(bronnen: Iterable[str] | str | None) -> frozenset[str]:
    if bronnen is None:
        return frozenset({"bron", "lokaal"})
    if isinstance(bronnen, str):
        items = [part.strip() for part in bronnen.split(",") if part.strip()]
    else:
        items = [str(item).strip() for item in bronnen if str(item).strip()]
    if not items:
        return frozenset({"bron", "lokaal"})
    invalid = sorted(set(items) - _VALID_BRONNEN)
    if invalid:
        raise ValueError(
            f"Ongeldige bronnen {invalid!r}; verwacht subset van {sorted(_VALID_BRONNEN)}"
        )
    return frozenset(items)


def _query_tokens(query_norm: str) -> list[str]:
    tokens = [token for token in _QUERY_SPLIT_RE.split(query_norm) if len(token) >= 2]
    return tokens or [query_norm]


def _matches_query(
    entry: ZoekIndexEntry,
    query_tokens: list[str],
    query_norm: str,
) -> bool:
    if query_norm in entry.search_terms:
        return True
    for token in query_tokens:
        if not any(
            token in term or term in token for term in entry.search_terms
        ):
            return False
    return True


def _matches_bestandsextensie(
    path: Path,
    bestandsextensie: frozenset[str] | None,
) -> bool:
    if bestandsextensie is None:
        return True
    return path.suffix.lower() in bestandsextensie


def _matches_context(
    entry: ZoekIndexEntry,
    context: ZoekContext,
    index: AliasIndex,
) -> bool:
    if context.gelegenheid:
        if _entry_has_gelegenheid_scope(entry, context.gelegenheid) and not _matches_gelegenheid(
            entry.gelegenheid,
            entry.entry.zangstuk_id,
            context.gelegenheid,
        ):
            return False
    if context.gelegenheidstype and entry.gelegenheidstype and not _matches_text_field(
        entry.gelegenheidstype, context.gelegenheidstype
    ):
        return False
    if context.toon and entry.toon and not _matches_text_field(entry.toon, context.toon):
        return False
    if context.referentie and entry.referentie and not _matches_text_field(
        entry.referentie, context.referentie
    ):
        return False
    if context.uitvoeringsvorm:
        try:
            resolved_uv = index.resolve_uitvoeringsvorm(
                entry.entry.zangstuk_id,
                entry.entry.variant_id,
                context.uitvoeringsvorm,
            )
        except NotFoundError:
            return False
        if entry.entry.uitvoeringsvorm_id != resolved_uv:
            return False
    return True


def _matches_gelegenheid(
    entry_gelegenheid: str | None,
    zangstuk_id: str,
    context_gelegenheid: str,
) -> bool:
    ctx = normalize_for_match(context_gelegenheid)
    if entry_gelegenheid:
        entry_norm = normalize_for_match(entry_gelegenheid)
        if ctx in entry_norm or entry_norm in ctx:
            return True
    return ctx in normalize_for_match(zangstuk_id)


def _entry_has_gelegenheid_scope(
    entry: ZoekIndexEntry,
    context_gelegenheid: str,
) -> bool:
    if entry.gelegenheid:
        return True
    ctx = normalize_for_match(context_gelegenheid)
    zangstuk_id = normalize_for_match(entry.entry.zangstuk_id)
    return ctx in zangstuk_id


def _matches_text_field(entry_value: str | None, context_value: str) -> bool:
    if not entry_value:
        return False
    entry_norm = normalize_for_match(entry_value)
    ctx_norm = normalize_for_match(context_value)
    return ctx_norm in entry_norm or entry_norm in ctx_norm


def _dedupe_matches(matches: list[ZoekMatch]) -> tuple[ZoekMatch, ...]:
    seen: set[str] = set()
    unique: list[ZoekMatch] = []
    for match in sorted(matches, key=lambda item: item.catalogus_pad):
        if match.catalogus_pad in seen:
            continue
        seen.add(match.catalogus_pad)
        unique.append(match)
    return tuple(unique)
