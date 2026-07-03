"""Zangstuk-catalogus: alias-index en resolver (bron §2.8)."""

from catalogus.alias_index import AliasIndex, VsaFileEntry
from catalogus.errors import AmbiguousError, IndexConflictError, InvalidIdError, NotFoundError
from catalogus.include_ref import IncludeRefError, is_logical_reference, parse_logical_reference
from catalogus.zoek import (
    ZOEK_NIVEAU,
    ZoekContext,
    ZoekLijstResult,
    ZoekMatch,
    ZoekResult,
    format_catalogus_pad,
    parse_bestandsextensie,
    zoek,
    zoek_kandidaten,
    zoek_kandidaten_met_roots,
    zoek_met_roots,
)

__all__ = [
    "AliasIndex",
    "AmbiguousError",
    "IncludeRefError",
    "IndexConflictError",
    "InvalidIdError",
    "NotFoundError",
    "VsaFileEntry",
    "ZOEK_NIVEAU",
    "ZoekContext",
    "ZoekLijstResult",
    "ZoekMatch",
    "ZoekResult",
    "format_catalogus_pad",
    "is_logical_reference",
    "parse_bestandsextensie",
    "parse_logical_reference",
    "zoek",
    "zoek_kandidaten",
    "zoek_kandidaten_met_roots",
    "zoek_met_roots",
]
