from __future__ import annotations

from pathlib import Path

import pytest

from catalogus import AliasIndex, IndexConflictError, NotFoundError

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "alias-index"
REPO_ROOT = Path(__file__).resolve().parents[1]
VSA_DEMO_CONTENT = (
    REPO_ROOT.parent / "VSA-tooling" / "examples" / "hugo-demo" / "content-source"
)


@pytest.fixture
def fixture_index() -> AliasIndex:
    return AliasIndex.build(fixture_root=FIXTURE_ROOT)


def test_case_insensitive_uitvoeringsvorm(fixture_index: AliasIndex) -> None:
    assert (
        fixture_index.resolve_uitvoeringsvorm(
            "cherubijnenhymne", "kastorski", "Groningen"
        )
        == "groningen"
    )


def test_meertalig_variant_alias(fixture_index: AliasIndex) -> None:
    assert fixture_index.resolve_variant("cherubijnenhymne", "Касторский") == "kastorski"


def test_canonical_id_passthrough(fixture_index: AliasIndex) -> None:
    assert fixture_index.resolve_zangstuk("cherubijnenhymne") == "cherubijnenhymne"
    assert (
        fixture_index.resolve_uitvoeringsvorm(
            "cherubijnenhymne", "kastorski", "groningen"
        )
        == "groningen"
    )


def test_representatie_passthrough(fixture_index: AliasIndex) -> None:
    assert (
        fixture_index.resolve_representatie(
            "cherubijnenhymne",
            "kastorski",
            "groningen",
            "groningen-vsa",
        )
        == "groningen-vsa"
    )


def test_not_found(fixture_index: AliasIndex) -> None:
    with pytest.raises(NotFoundError):
        fixture_index.resolve_zangstuk("onbekend-zangstuk")


def test_index_conflict(tmp_path: Path) -> None:
    lokaal = tmp_path / "lokaal" / "test-zangstuk" / "variant-a"
    lokaal.mkdir(parents=True)
    (lokaal / "variant.yaml").write_text(
        "zangstuk-id: test-zangstuk\n"
        "variant-id: variant-a\n"
        "aliases:\n"
        "  - { text: gedeeld, lang: nl }\n",
        encoding="utf-8",
    )
    uv_b = tmp_path / "lokaal" / "test-zangstuk" / "variant-b"
    uv_dir = uv_b / "hemelum"
    uv_dir.mkdir(parents=True)
    (uv_b / "variant.yaml").write_text(
        "zangstuk-id: test-zangstuk\n"
        "variant-id: variant-b\n"
        "aliases:\n"
        "  - { text: gedeeld, lang: nl }\n",
        encoding="utf-8",
    )
    (uv_dir / "uitvoeringsvorm.yaml").write_text(
        "uitvoeringsvorm-id: hemelum\n", encoding="utf-8"
    )
    with pytest.raises(IndexConflictError):
        AliasIndex.build(fixture_root=tmp_path)


def test_bron_zangstuk_title_alias() -> None:
    index = AliasIndex.build(bron_root=REPO_ROOT)
    assert (
        index.resolve_zangstuk("Tropaar van de zondag, toon 1")
        == "troparion-zondag-toon-1"
    )


def test_bron_flat_source_as_uitvoeringsvorm() -> None:
    index = AliasIndex.build(bron_root=REPO_ROOT)
    assert (
        index.resolve_uitvoeringsvorm(
            "troparion-zondag-toon-1",
            "troparion-zondag-toon-1",
            "groningen",
        )
        == "groningen"
    )


@pytest.mark.skipif(
    not VSA_DEMO_CONTENT.is_dir(),
    reason="VSA-tooling hugo-demo niet aanwezig (sibling checkout)",
)
def test_hugo_demo_hemelum() -> None:
    index = AliasIndex.build(content_root=VSA_DEMO_CONTENT)
    assert index.resolve_zangstuk("1e antifoon weekdagen") == "antifoon-1-weekdagen"
    assert (
        index.resolve_variant("antifoon-1-weekdagen", "1e antifoon weekdagen")
        == "liturgikon-weekdagen"
    )
    assert (
        index.resolve_uitvoeringsvorm(
            "antifoon-1-weekdagen",
            "liturgikon-weekdagen",
            "Hemelum",
        )
        == "hemelum"
    )


def test_resolve_vsa_path_fixture() -> None:
    index = AliasIndex.build(fixture_root=FIXTURE_ROOT)
    path = index.resolve_vsa_path(
        "id:cherubijnenhymne/kastorski/Groningen"
    )
    assert path.name == "groningen.vsa"
    assert path.is_file()


def test_resolve_vsa_path_bron_two_segments() -> None:
    index = AliasIndex.build(bron_root=REPO_ROOT)
    assert (
        index.resolve_uitvoeringsvorm(
            "troparion-zondag-toon-1",
            "troparion-zondag-toon-1",
            "groningen",
        )
        == "groningen"
    )


def test_resolve_zondag_antifoon_pdf_paths() -> None:
    index = AliasIndex.build(bron_root=REPO_ROOT)
    assert index.resolve_zangstuk("zaligsprekingen") == "antifoon-3-zondag"
    path = index.resolve_vsa_path("bron:antifoon-1-zondag/groningen")
    assert path.name == "koormap-003.pdf"
    assert path.is_file()
