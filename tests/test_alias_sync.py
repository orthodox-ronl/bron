from __future__ import annotations

from pathlib import Path

import pytest

from catalogus.alias_blokken import load_alias_register
from catalogus.alias_sync import (
    resolve_blok_id,
    run_alias_sync,
    sync_aliases_in_text,
)
from catalogus.errors import AliasSyncError

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER_PATH = REPO_ROOT / "catalogus" / "data" / "alias-blokken.yaml"


@pytest.fixture
def register():
    return load_alias_register(REGISTER_PATH)


def test_resolve_kondak_from_id_prefix(register) -> None:
    blok = resolve_blok_id(
        {},
        "kondak-geboorte-moeder-gods",
        register,
        context="test",
    )
    assert blok == "kondak"


def test_resolve_tropaar_from_troparion_id(register) -> None:
    blok = resolve_blok_id(
        {},
        "troparion-zondag-toon-1",
        register,
        context="test",
    )
    assert blok == "tropaar"


def test_resolve_troparion_melodie_skipped(register) -> None:
    blok = resolve_blok_id(
        {},
        "troparion-melodie-toon-3",
        register,
        context="test",
    )
    assert blok is None


def test_resolve_explicit_liturgische_rol(register) -> None:
    blok = resolve_blok_id(
        {"liturgische_rol": "antifoon"},
        "onbekend-id",
        register,
        context="test",
    )
    assert blok == "antifoon"


def test_unknown_liturgische_rol_raises(register) -> None:
    with pytest.raises(AliasSyncError, match="Onbekend alias-blok"):
        resolve_blok_id(
            {"liturgische_rol": "niet-bestaand"},
            "x",
            register,
            context="test.yaml",
        )


def test_sync_writes_generated_block(tmp_path: Path, register) -> None:
    yaml_path = tmp_path / "zangstuk.yaml"
    yaml_path.write_text(
        "id: kondak-test\n"
        "title: Test\n"
        "aliases:\n"
        "  - Handmatig\n",
        encoding="utf-8",
    )
    text = yaml_path.read_text(encoding="utf-8")
    new_text, changed = sync_aliases_in_text(text, blok_id="kondak", register=register)
    assert changed
    assert "gegenereerd: alias-blok kondak" in new_text
    assert "Handmatig" in new_text
    assert "kondakion" in new_text
    assert new_text.index("Handmatig") < new_text.index("gegenereerd:")


def test_sync_idempotent(tmp_path: Path, register) -> None:
    yaml_path = tmp_path / "zangstuk.yaml"
    yaml_path.write_text(
        "id: kondak-test\naliases:\n  - x\n",
        encoding="utf-8",
    )
    text = yaml_path.read_text(encoding="utf-8")
    new_text, _ = sync_aliases_in_text(text, blok_id="kondak", register=register)
    _, changed_again = sync_aliases_in_text(new_text, blok_id="kondak", register=register)
    assert not changed_again


def test_sync_inserts_before_sources(tmp_path: Path, register) -> None:
    yaml_path = tmp_path / "zangstuk.yaml"
    yaml_path.write_text(
        "id: troparion-zondag-toon-1\n"
        "title: Tropaar\n"
        "toon: 1\n"
        "sources:\n"
        "  - id: groningen\n"
        "    file: sources/vsa/groningen.vsa\n",
        encoding="utf-8",
    )
    text = yaml_path.read_text(encoding="utf-8")
    new_text, changed = sync_aliases_in_text(
        text, blok_id="tropaar", register=register
    )
    assert changed
    assert new_text.index("aliases:") < new_text.index("sources:")
    data = __import__("yaml").safe_load(new_text)
    assert "aliases" in data
    assert isinstance(data["sources"], list)
    assert data["sources"][0]["id"] == "groningen"


def test_run_sync_on_fixture_zangstuk(tmp_path: Path, register) -> None:
    zdir = tmp_path / "zangstukken" / "kondak-demo"
    zdir.mkdir(parents=True)
    (zdir / "zangstuk.yaml").write_text(
        "id: kondak-demo\n"
        "title: Demo\n",
        encoding="utf-8",
    )
    results = run_alias_sync(register=register, bron_root=tmp_path)
    assert len(results) == 1
    assert results[0].changed
    content = (zdir / "zangstuk.yaml").read_text(encoding="utf-8")
    assert "gegenereerd: alias-blok kondak" in content


def test_check_detects_drift(tmp_path: Path, register) -> None:
    zdir = tmp_path / "zangstukken" / "kondak-demo"
    zdir.mkdir(parents=True)
    (zdir / "zangstuk.yaml").write_text(
        "id: kondak-demo\naliases:\n  - oud\n",
        encoding="utf-8",
    )
    drift = run_alias_sync(register=register, bron_root=tmp_path, check=True)
    assert drift[0].changed
