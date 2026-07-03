from __future__ import annotations

from pathlib import Path

import pytest

from catalogus import (
    VsaFileEntry,
    ZoekContext,
    ZoekLijstResult,
    ZoekMatch,
    format_catalogus_pad,
    parse_bestandsextensie,
    zoek,
    zoek_kandidaten,
    zoek_kandidaten_met_roots,
    zoek_met_roots,
)
from catalogus.errors import AmbiguousError, NotFoundError
from catalogus.alias_index import AliasIndex
from catalogus.zoek import _zoek_from_lijst

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "alias-index"


def test_format_catalogus_pad_lokaal_drie_segmenten() -> None:
    entry = VsaFileEntry(
        zangstuk_id="antifoon-1-weekdagen",
        variant_id="liturgikon-weekdagen",
        uitvoeringsvorm_id="hemelum",
        representatie_id="hemelum",
        path=Path("/tmp/hemelum.vsa"),
        origin="lokaal",
    )
    assert (
        format_catalogus_pad(entry)
        == "lokaal:antifoon-1-weekdagen/liturgikon-weekdagen/hemelum"
    )


def test_format_catalogus_pad_met_representatie() -> None:
    entry = VsaFileEntry(
        zangstuk_id="cherubijnenhymne",
        variant_id="kastorski",
        uitvoeringsvorm_id="groningen",
        representatie_id="groningen-vsa",
        path=Path("/tmp/groningen.vsa"),
        origin="bron",
    )
    assert (
        format_catalogus_pad(entry)
        == "bron:cherubijnenhymne/kastorski/groningen/groningen-vsa"
    )


def test_zoek_context_from_default_mapping() -> None:
    ctx = ZoekContext.from_default_mapping(
        {
            "gelegenheid": "geboorte-moeder-gods",
            "gelegenheidstype": "vast-feest",
            "toon": 4,
            "uitvoeringsvorm": "Groningen",
        },
        bronnen="lokaal",
    )
    assert ctx.gelegenheid == "geboorte-moeder-gods"
    assert ctx.gelegenheidstype == "vast-feest"
    assert ctx.toon == "4"
    assert ctx.uitvoeringsvorm == "Groningen"
    assert ctx.bronnen == frozenset({"lokaal"})


def test_zoek_context_invalid_bronnen() -> None:
    with pytest.raises(ValueError, match="Ongeldige bronnen"):
        ZoekContext.from_default_mapping({}, bronnen="alle")


def test_parse_bestandsextensie_defaults() -> None:
    assert parse_bestandsextensie(None) == frozenset({".vsa"})
    assert parse_bestandsextensie("vsa") == frozenset({".vsa"})
    assert parse_bestandsextensie("alle") is None
    assert parse_bestandsextensie("pdf,vsa") == frozenset({".pdf", ".vsa"})


def test_zoek_lijst_result_catalogus_paden() -> None:
    entry = VsaFileEntry(
        zangstuk_id="a",
        variant_id="b",
        uitvoeringsvorm_id="c",
        representatie_id="c",
        path=Path("/tmp/c.vsa"),
        origin="bron",
    )
    lijst = ZoekLijstResult(
        query="Troparion",
        query_normalized="troparion",
        matches=(
            ZoekMatch(entry=entry, catalogus_pad=format_catalogus_pad(entry)),
        ),
    )
    assert lijst.catalogus_paden == ["bron:a/b/c"]


def test_zoek_from_lijst_strict_modes() -> None:
    entry = VsaFileEntry(
        zangstuk_id="a",
        variant_id="b",
        uitvoeringsvorm_id="c",
        representatie_id="c",
        path=Path("/tmp/c.vsa"),
        origin="bron",
    )
    pad = format_catalogus_pad(entry)
    match = ZoekMatch(entry=entry, catalogus_pad=pad)
    empty = ZoekLijstResult(query="Troparion", query_normalized="troparion", matches=())
    with pytest.raises(NotFoundError):
        _zoek_from_lijst(empty)
    ambiguous = ZoekLijstResult(
        query="Troparion",
        query_normalized="troparion",
        matches=(match, match),
    )
    with pytest.raises(AmbiguousError) as exc_info:
        _zoek_from_lijst(ambiguous)
    assert len(exc_info.value.candidates) == 2
    assert exc_info.value.candidates[0].canonical_id == pad
    result = _zoek_from_lijst(
        ZoekLijstResult(
            query="Troparion",
            query_normalized="troparion",
            matches=(match,),
        )
    )
    assert result.catalogus_pad == pad


def test_zoek_stub_raises_not_implemented(fixture_index: AliasIndex) -> None:
    with pytest.raises(NotImplementedError, match="catalogus-zoek-api"):
        zoek("Troparion", index=fixture_index)


def test_zoek_kandidaten_stub_raises_not_implemented(fixture_index: AliasIndex) -> None:
    with pytest.raises(NotImplementedError, match="catalogus-zoek-api"):
        zoek_kandidaten("Troparion", index=fixture_index)


def test_zoek_met_roots_stub_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="catalogus-zoek-api"):
        zoek_met_roots(
            "Troparion",
            fixture_root=FIXTURE_ROOT,
            context=ZoekContext(gelegenheid="geboorte-moeder-gods"),
        )


def test_zoek_kandidaten_met_roots_stub_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="catalogus-zoek-api"):
        zoek_kandidaten_met_roots(
            "Troparion",
            fixture_root=FIXTURE_ROOT,
            context=ZoekContext(gelegenheid="geboorte-moeder-gods"),
        )


def test_zoek_rejects_empty_query(fixture_index: AliasIndex) -> None:
    with pytest.raises(ValueError, match="leeg"):
        zoek("   ", index=fixture_index)


def test_zoek_met_roots_requires_root() -> None:
    with pytest.raises(ValueError, match="Minstens één"):
        zoek_met_roots("Troparion")


def test_zoek_kandidaten_met_roots_requires_root() -> None:
    with pytest.raises(ValueError, match="Minstens één"):
        zoek_kandidaten_met_roots("Troparion")


@pytest.fixture
def fixture_index() -> AliasIndex:
    return AliasIndex.build(fixture_root=FIXTURE_ROOT)
