from __future__ import annotations

from pathlib import Path

import pytest

from catalogus.alias_blokken import (
    AliasBlokRegister,
    default_register_path,
    load_alias_register,
)
from catalogus.errors import AliasRegisterError

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER_PATH = REPO_ROOT / "catalogus" / "data" / "alias-blokken.yaml"


def test_load_production_register() -> None:
    register = load_alias_register(REGISTER_PATH)
    assert "kondak" in register.blokken
    assert "tropaar" in register.blokken
    assert len(register.blokken) >= 2


def test_expand_kondak_block() -> None:
    register = load_alias_register(REGISTER_PATH)
    expanded = register.expand_term("Kondakion")
    assert expanded == register.expand_blok("kondak")
    assert "kondakion" in {t.casefold() for t in expanded}


def test_expand_unknown_term_passthrough() -> None:
    register = load_alias_register(REGISTER_PATH)
    assert register.expand_term("onbekend") == frozenset({"onbekend"})


def test_overlap_in_register_rejected(tmp_path: Path) -> None:
    path = tmp_path / "alias-blokken.yaml"
    path.write_text(
        "blokken:\n"
        "  a:\n"
        "    aliassen:\n"
        "      - gedeeld\n"
        "  b:\n"
        "    aliassen:\n"
        "      - gedeeld\n",
        encoding="utf-8",
    )
    with pytest.raises(AliasRegisterError, match="gedeeld"):
        load_alias_register(path)


def test_default_register_path_from_bron_root() -> None:
    assert default_register_path(bron_root=REPO_ROOT) == REGISTER_PATH


def test_expand_texts_preserves_order() -> None:
    register = AliasBlokRegister(
        blokken={"x": frozenset({"a", "b"})},
        _term_to_blok={"a": "x", "b": "x"},
    )
    assert set(register.expand_texts(("a",))) == {"a", "b"}
