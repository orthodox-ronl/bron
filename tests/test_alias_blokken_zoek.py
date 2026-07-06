from __future__ import annotations

from pathlib import Path

import pytest

from catalogus import AliasIndex
from catalogus.alias_blokken import load_alias_register
from catalogus.zoek import ZoekContext, zoek_met_roots

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER_PATH = REPO_ROOT / "catalogus" / "data" / "alias-blokken.yaml"


def test_kondak_synonym_in_search_index() -> None:
    """Zoek op 'Kondak' moet stuk vinden dat alleen 'Kondakion' in yaml heeft."""
    load_alias_register(REGISTER_PATH)  # register moet valide zijn
    index = AliasIndex.build(bron_root=REPO_ROOT)
    matches = [
        entry
        for entry in index.zoek_entries
        if entry.entry.zangstuk_id == "kondak-geboorte-moeder-gods"
    ]
    assert matches
    terms = matches[0].search_terms
    assert "kondak" in terms
    assert "kondakion" in terms


def test_zoek_kondak_vindt_kondakion_yaml() -> None:
    result = zoek_met_roots(
        "Kondak",
        bron_root=REPO_ROOT,
        context=ZoekContext(
            gelegenheid="geboorte-moeder-gods",
            gelegenheidstype="vast-feest",
        ),
        bestandsextensie={".vsa"},
    )
    assert result.entry.zangstuk_id == "kondak-geboorte-moeder-gods"


def test_zoek_tropaar_vindt_troparion_yaml() -> None:
    result = zoek_met_roots(
        "Tropaar",
        bron_root=REPO_ROOT,
        context=ZoekContext(
            gelegenheid="geboorte-moeder-gods",
            gelegenheidstype="vast-feest",
        ),
        bestandsextensie={".vsa"},
    )
    assert result.entry.zangstuk_id == "troparion-geboorte-moeder-gods"
