"""Catalogus zoek-API — contract fase 0; implementatie fase 4.

Normatief: docs/specs/catalogus-zoek-api.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from catalogus.alias_index import AliasIndex, VsaFileEntry
from catalogus.errors import AmbiguousError, MatchCandidate, NotFoundError
from catalogus.normalize import normalize_for_match

ZOEK_NIVEAU = "zoek"
_DEFAULT_BESTANDSEXTENSIE: frozenset[str] = frozenset({".vsa"})
_VALID_BRONNEN: frozenset[str] = frozenset({"bron", "lokaal"})
_SPEC_DOC = "docs/specs/catalogus-zoek-api.md"


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
        NotImplementedError: fase 0 stub.
    """
    _ = index
    _ = context
    _ = bestandsextensie
    normalized_query = _require_query(query)
    _ = normalized_query
    raise NotImplementedError(
        f"catalogus.zoek_kandidaten is nog niet geïmplementeerd; zie {_SPEC_DOC}"
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
        NotFoundError: geen match (fase 4).
        AmbiguousError: meerdere matches (fase 4).
        NotImplementedError: fase 0 stub (via ``zoek_kandidaten``).
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
        ook_gevonden_in_bron=(),
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
