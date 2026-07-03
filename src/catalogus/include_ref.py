from __future__ import annotations

from catalogus.errors import AmbiguousError, CatalogusError, NotFoundError

REF_PREFIXES = ("id:", "lokaal:", "bron:")


class IncludeRefError(CatalogusError):
    """Ongeldige logische include-referentie."""


def is_logical_reference(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in REF_PREFIXES)


def parse_logical_reference(reference: str) -> tuple[str, list[str]]:
    """Parse ``id:…``, ``lokaal:…`` of ``bron:…`` naar prefix en segmenten."""
    for prefix in REF_PREFIXES:
        if reference.startswith(prefix):
            body = reference[len(prefix) :]
            segments = [segment.strip() for segment in body.split("/") if segment.strip()]
            if not segments:
                raise IncludeRefError(
                    f"Logische referentie mist segmenten: {reference!r}"
                )
            if len(segments) > 4:
                raise IncludeRefError(
                    f"Maximaal vier segmenten (representatie-niveau): {reference!r}"
                )
            return prefix.rstrip(":"), segments
    raise IncludeRefError(f"Geen logische referentie: {reference!r}")


def segments_label(segments: list[str]) -> str:
    return "/".join(segments)
