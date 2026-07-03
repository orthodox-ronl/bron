from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MatchCandidate:
    canonical_id: str
    context: str


class CatalogusError(Exception):
    """Basisfout voor catalogus-resolver."""


class NotFoundError(CatalogusError):
    def __init__(self, niveau: str, invoer: str, scope: str = "") -> None:
        self.niveau = niveau
        self.invoer = invoer
        self.scope = scope
        detail = f" in scope {scope}" if scope else ""
        super().__init__(f"Geen match voor {niveau} '{invoer}'{detail}")


class AmbiguousError(CatalogusError):
    def __init__(
        self,
        niveau: str,
        invoer: str,
        candidates: list[MatchCandidate],
        scope: str = "",
    ) -> None:
        self.niveau = niveau
        self.invoer = invoer
        self.candidates = candidates
        self.scope = scope
        detail = f" in scope {scope}" if scope else ""
        lines = ", ".join(f"{c.canonical_id} ({c.context})" for c in candidates)
        super().__init__(
            f"Ambiguïteit voor {niveau} '{invoer}'{detail}: {lines}"
        )


class IndexConflictError(CatalogusError):
    def __init__(self, conflicts: list[str]) -> None:
        self.conflicts = conflicts
        super().__init__(
            f"Alias-index bevat {len(conflicts)} conflict(en):\n"
            + "\n".join(f"  - {c}" for c in conflicts)
        )


class InvalidIdError(CatalogusError):
    def __init__(self, id_value: str, context: str) -> None:
        self.id_value = id_value
        self.context = context
        super().__init__(
            f"Ongeldig canoniek id '{id_value}' in {context} "
            "(verwacht [a-z0-9_-]+)"
        )


class PathNotFoundError(CatalogusError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AmbiguousPathError(CatalogusError):
    def __init__(self, message: str, candidates: list[str]) -> None:
        self.candidates = candidates
        super().__init__(message)
