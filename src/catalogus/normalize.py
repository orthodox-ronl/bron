from __future__ import annotations

import re

CANONICAL_ID_RE = re.compile(r"^[a-z0-9_-]+$")


def normalize_for_match(text: str) -> str:
    return text.strip().casefold()


def canonical_form(text: str) -> str:
    return text.strip().lower()


def is_canonical_id(text: str) -> bool:
    return bool(CANONICAL_ID_RE.match(text))
