"""Unit tests for scripts/inject-glossary-termrefs.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "inject-glossary-termrefs.py"


def _load():
    spec = importlib.util.spec_from_file_location("inject_glossary_termrefs", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def inj():
    return _load()


def test_abbr_alias_converters_use_termref_not_md_link():
    text = Path("docs/tev2-config.yaml").read_text(encoding="utf-8")
    assert "Afkorting van [{{#if glossaryTerm}}{{glossaryTerm}}" in text
    assert "Alias voor [{{#if glossaryTerm}}{{glossaryTerm}}" in text
    assert "]({{term}}@)." in text
    assert "Afkorting van [{{#if glossaryTerm}}{{noRefs glossaryTerm}}" not in text
    assert "{{noRefs glossaryText}}" not in text
    assert "{{glossaryText}}" in text
    # Abbr/alias description must use TermRef, not a second terms/… link.
    for line in text.splitlines():
        if "Afkorting van" in line or "Alias voor" in line:
            assert "]({{term}}@)." in line
            assert "terms/{{term}}.md)." not in line
            assert "localize navurl}})." not in line


def test_inject_wraps_other_terms_skips_self(inj):
    entries = [
        {
            "term": "zangstuk",
            "scopetag": "bron",
            "formPhrases": ["zangstuk", "zangstukken"],
            "glossaryTerm": "Zangstuk",
        },
        {
            "term": "variant",
            "scopetag": "bron",
            "formPhrases": ["variant", "varianten"],
            "glossaryTerm": "Variant",
        },
    ]
    phrases = inj.build_phrase_index(entries, "bron")
    text = (
        "Een verzameling van zangstukken en varianten. "
        "Zie ook zangstuk zelf."
    )
    skip = inj.own_term_keys("zangstuk", entries)
    out = inj.inject_into_text(text, phrases, skip)
    assert "[varianten](variant@)" in out or "[Varianten](variant@)" in out
    assert "[variant](variant@)" in out or "varianten" in out
    # Self formphrases must stay plain.
    assert "[zangstukken](zangstuk@)" not in out
    assert "[zangstuk](zangstuk@)" not in out
    assert "zangstukken" in out


def test_inject_skips_existing_links_and_code(inj):
    entries = [
        {
            "term": "variant",
            "scopetag": "bron",
            "formPhrases": ["variant"],
        },
    ]
    phrases = inj.build_phrase_index(entries, "bron")
    text = "Al gedaan: [variant](@) en `variant` en [x](https://example.com/variant)."
    out = inj.inject_into_text(text, phrases, skip_terms=set())
    assert out.count("[variant]") == 1  # only the existing TermRef showtext
    assert "`variant`" in out


def test_sanitize_at_in_termref_showtext(inj):
    out = inj.sanitize_termref_showtexts(
        "Alias voor [@include-vsa](include-vsa@)."
    )
    assert out == "Alias voor [include-vsa](include-vsa@)."


def test_inject_foreign_scope_suffix(inj):
    entries = [
        {
            "term": "zangstuk",
            "scopetag": "bron",
            "formPhrases": ["zangstuk"],
        },
    ]
    phrases = inj.build_phrase_index(entries, "vsa-tooling")
    out = inj.inject_into_text("dit zangstuk hier", phrases, skip_terms=set())
    assert "[zangstuk](zangstuk@bron)" in out


def test_process_glossary_row(inj):
    entries = [
        {
            "term": "afgeleide",
            "scopetag": "bron",
            "formPhrases": ["afgeleide", "afgeleiden"],
        },
        {
            "term": "bronbestand",
            "scopetag": "bron",
            "formPhrases": ["bronbestand", "bronbestanden"],
        },
    ]
    phrases = inj.build_phrase_index(entries, "bron")
    src = """| Term | Definitie |
| ---- | --------- |
| [Afgeleide](terms/afgeleide.md) | Uit een bronbestand gemaakt. **Opmerking**: geen bronbestand. |
"""
    out = inj.process_glossary(src, phrases, entries)
    row = [ln for ln in out.splitlines() if "terms/afgeleide.md" in ln][0]
    assert "[bronbestand](bronbestand@)" in row
    assert "[afgeleide](afgeleide@)" not in row
    assert "[Afgeleide](afgeleide@)" not in row
    assert "[afgeleiden](afgeleide@)" not in row


def test_load_mrg_entries_ignores_foreign_scope_files(inj, tmp_path):
    """Imported mrg.tev2.yaml must not feed phrase inject (CI mrg-import)."""
    (tmp_path / "mrg.bron.yaml").write_text(
        "terminology:\n  scopetag: bron\nentries:\n"
        "  - term: zangstuk\n    scopetag: bron\n    formPhrases: [zangstuk]\n",
        encoding="utf-8",
    )
    (tmp_path / "mrg.tev2.yaml").write_text(
        "terminology:\n  scopetag: tev2\nentries:\n"
        "  - term: scope\n    scopetag: tev2\n    formPhrases: [scope]\n",
        encoding="utf-8",
    )
    paths = inj.mrg_paths_for_scope(tmp_path, "bron")
    assert [p.name for p in paths] == ["mrg.bron.yaml"]
    entries = inj.load_mrg_entries(tmp_path, "bron")
    assert [e["term"] for e in entries] == ["zangstuk"]
    phrases = inj.build_phrase_index(entries, "bron")
    assert all(term == "zangstuk" for _ph, term, _suf in phrases)
