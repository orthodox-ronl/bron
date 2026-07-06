from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Literal

import yaml

from catalogus.alias_blokken import AliasBlokRegister, try_load_alias_register
from catalogus.alias_sync import partition_yaml_aliases
from catalogus.errors import (
    AmbiguousPathError,
    IndexConflictError,
    InvalidIdError,
    NotFoundError,
    PathNotFoundError,
)
from catalogus.include_ref import IncludeRefError, parse_logical_reference
from catalogus.normalize import is_canonical_id, normalize_for_match

Origin = Literal["lokaal", "bron"]


@dataclass(frozen=True)
class VsaFileEntry:
    zangstuk_id: str
    variant_id: str
    uitvoeringsvorm_id: str
    representatie_id: str
    path: Path
    origin: Origin


@dataclass(frozen=True)
class ZoekIndexEntry:
    """Doorzoekbare metadata bij één brondocument (`.vsa` of ander bestand)."""

    entry: VsaFileEntry
    title: str | None = None
    gelegenheid: str | None = None
    gelegenheidstype: str | None = None
    toon: str | None = None
    referentie: str | None = None
    search_terms: frozenset[str] = frozenset()


@dataclass
class _ScopeTable:
    """Lookup binnen één scope: genormaliseerde sleutel → canoniek id."""

    _entries: dict[str, tuple[str, str]] = field(default_factory=dict)
    conflicts: list[str] = field(default_factory=list)

    def register(self, alias_or_id: str, canonical_id: str, context: str) -> None:
        key = normalize_for_match(alias_or_id)
        if not key:
            return
        existing = self._entries.get(key)
        if existing is None:
            self._entries[key] = (canonical_id, context)
        elif existing[0] != canonical_id:
            self.conflicts.append(
                f"'{alias_or_id}' in {context} wijst naar '{canonical_id}', "
                f"maar is al geregistreerd als '{existing[0]}' ({existing[1]})"
            )

    def resolve(self, niveau: str, invoer: str, scope_label: str) -> str:
        key = normalize_for_match(invoer)
        if not key:
            raise NotFoundError(niveau, invoer, scope_label)
        match = self._entries.get(key)
        if match is None:
            raise NotFoundError(niveau, invoer, scope_label)
        return match[0]


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Verwacht yaml-mapping in {path}")
    return data


def _register_aliases(
    table: _ScopeTable,
    canonical_id: str,
    aliases: Iterable[object],
    context: str,
) -> None:
    table.register(canonical_id, canonical_id, context)
    for item in aliases:
        if isinstance(item, str):
            table.register(item, canonical_id, context)
        elif isinstance(item, dict) and "text" in item:
            table.register(str(item["text"]), canonical_id, context)


def _require_canonical_id(id_value: str, context: str) -> str:
    if not is_canonical_id(id_value):
        raise InvalidIdError(id_value, context)
    return id_value


@dataclass
class AliasIndex:
    """In-memory alias-index, opgebouwd uit manifesten en mappad."""

    zangstuk: _ScopeTable = field(default_factory=_ScopeTable)
    variant: dict[str, _ScopeTable] = field(default_factory=dict)
    uitvoeringsvorm: dict[tuple[str, str], _ScopeTable] = field(default_factory=dict)
    representatie: dict[tuple[str, str, str], _ScopeTable] = field(
        default_factory=dict
    )
    vsa_files: list[VsaFileEntry] = field(default_factory=list)
    zoek_entries: list[ZoekIndexEntry] = field(default_factory=list)
    _alias_register: AliasBlokRegister | None = field(default=None, repr=False)

    @classmethod
    def build(
        cls,
        *,
        content_root: Path | None = None,
        bron_root: Path | None = None,
        fixture_root: Path | None = None,
    ) -> AliasIndex:
        index = cls()
        index._alias_register = _load_alias_register_for_build(
            content_root=content_root,
            bron_root=bron_root,
            fixture_root=fixture_root,
        )
        if content_root is not None:
            index._scan_root(content_root.resolve(), "lokaal")
        if bron_root is not None:
            index._scan_root(bron_root.resolve(), "bron")
        if fixture_root is not None:
            index._scan_root(fixture_root.resolve(), "lokaal")
        index._raise_if_conflicts()
        return index

    def _scan_root(self, root: Path, origin: Origin) -> None:
        lokaal = root / "lokaal"
        if lokaal.is_dir():
            self._scan_lokaal(lokaal, origin)
        zangstukken = root / "zangstukken"
        if zangstukken.is_dir():
            self._scan_bron_zangstukken(zangstukken, origin)

    def _raise_if_conflicts(self) -> None:
        conflicts: list[str] = []
        conflicts.extend(self.zangstuk.conflicts)
        for table in self.variant.values():
            conflicts.extend(table.conflicts)
        for table in self.uitvoeringsvorm.values():
            conflicts.extend(table.conflicts)
        for table in self.representatie.values():
            conflicts.extend(table.conflicts)
        if conflicts:
            raise IndexConflictError(conflicts)

    def validate(self) -> list[str]:
        """Retourneer conflicten zonder exception (voor CLI validate)."""
        try:
            self._raise_if_conflicts()
        except IndexConflictError as exc:
            return list(exc.conflicts)
        return []

    def _variant_table(self, zangstuk_id: str) -> _ScopeTable:
        if zangstuk_id not in self.variant:
            self.variant[zangstuk_id] = _ScopeTable()
        return self.variant[zangstuk_id]

    def _uv_table(self, zangstuk_id: str, variant_id: str) -> _ScopeTable:
        key = (zangstuk_id, variant_id)
        if key not in self.uitvoeringsvorm:
            self.uitvoeringsvorm[key] = _ScopeTable()
        return self.uitvoeringsvorm[key]

    def _repr_table(
        self, zangstuk_id: str, variant_id: str, uitvoeringsvorm_id: str
    ) -> _ScopeTable:
        key = (zangstuk_id, variant_id, uitvoeringsvorm_id)
        if key not in self.representatie:
            self.representatie[key] = _ScopeTable()
        return self.representatie[key]

    def _register_vsa_file(
        self,
        *,
        zangstuk_id: str,
        variant_id: str,
        uitvoeringsvorm_id: str,
        representatie_id: str,
        path: Path,
        origin: Origin,
        title: str | None = None,
        gelegenheid: str | None = None,
        gelegenheidstype: str | None = None,
        toon: str | None = None,
        referentie: str | None = None,
        extra_search_texts: Iterable[str] | None = None,
    ) -> None:
        if not path.is_file():
            return
        entry = VsaFileEntry(
            zangstuk_id=zangstuk_id,
            variant_id=variant_id,
            uitvoeringsvorm_id=uitvoeringsvorm_id,
            representatie_id=representatie_id,
            path=path.resolve(),
            origin=origin,
        )
        self.vsa_files.append(entry)
        self.zoek_entries.append(
            ZoekIndexEntry(
                entry=entry,
                title=title,
                gelegenheid=gelegenheid,
                gelegenheidstype=gelegenheidstype,
                toon=toon,
                referentie=referentie,
                search_terms=_build_search_terms(
                    zangstuk_id,
                    variant_id,
                    uitvoeringsvorm_id,
                    representatie_id,
                    title,
                    *(extra_search_texts or ()),
                    register=self._alias_register,
                ),
            )
        )

    def _scan_lokaal(self, lokaal_root: Path, origin: Origin) -> None:
        for zangstuk_dir in sorted(p for p in lokaal_root.iterdir() if p.is_dir()):
            zangstuk_id = _require_canonical_id(
                zangstuk_dir.name, str(zangstuk_dir)
            )
            ctx_z = str(zangstuk_dir)
            _register_aliases(self.zangstuk, zangstuk_id, [zangstuk_id], ctx_z)

            for variant_dir in sorted(p for p in zangstuk_dir.iterdir() if p.is_dir()):
                variant_id = _require_canonical_id(
                    variant_dir.name, str(variant_dir)
                )
                ctx_v = str(variant_dir)
                variant_manifest = variant_dir / "variant.yaml"
                aliases: list[object] = [variant_id]
                title: str | None = None
                variant_gelegenheid: str | None = None
                variant_gelegenheidstype: str | None = None
                variant_toon: str | None = None
                variant_referentie: str | None = None
                generated_aliases: list[str] = []
                if variant_manifest.is_file():
                    data = _load_yaml(variant_manifest)
                    yaml_z = data.get("zangstuk-id", zangstuk_id)
                    yaml_v = data.get("variant-id", variant_id)
                    _require_canonical_id(str(yaml_z), str(variant_manifest))
                    _require_canonical_id(str(yaml_v), str(variant_manifest))
                    title = _metadata_str(data.get("title"))
                    variant_gelegenheid = _metadata_str(data.get("gelegenheid"))
                    variant_gelegenheidstype = _metadata_str(data.get("gelegenheidstype"))
                    variant_toon = _metadata_str(data.get("toon"))
                    variant_referentie = _metadata_str(data.get("referentie"))
                    raw_aliases = data.get("aliases") or []
                    manual_aliases, generated_aliases = partition_yaml_aliases(
                        variant_manifest, raw_aliases
                    )
                    aliases.extend(manual_aliases)
                    if title:
                        aliases.append(title)

                variant_table = self._variant_table(zangstuk_id)
                _register_aliases(variant_table, variant_id, aliases, ctx_v)

                if variant_manifest.is_file():
                    zangstuk_aliases: list[object] = list(manual_aliases)
                    if title:
                        zangstuk_aliases.append(title)
                    for alias in zangstuk_aliases:
                        if isinstance(alias, str):
                            self.zangstuk.register(alias, zangstuk_id, ctx_v)
                        elif isinstance(alias, dict) and "text" in alias:
                            self.zangstuk.register(
                                str(alias["text"]), zangstuk_id, ctx_v
                            )

                for uv_dir in sorted(p for p in variant_dir.iterdir() if p.is_dir()):
                    uv_id = _require_canonical_id(uv_dir.name, str(uv_dir))
                    ctx_uv = str(uv_dir)
                    uv_manifest = uv_dir / "uitvoeringsvorm.yaml"
                    uv_aliases: list[object] = [uv_id]
                    if uv_manifest.is_file():
                        data = _load_yaml(uv_manifest)
                        yaml_uv = data.get("uitvoeringsvorm-id", uv_id)
                        _require_canonical_id(str(yaml_uv), str(uv_manifest))
                        uv_aliases.extend(data.get("aliases") or [])
                        for repr_entry in data.get("representaties") or []:
                            if not isinstance(repr_entry, dict):
                                continue
                            repr_id = repr_entry.get("representatie-id")
                            if not repr_id:
                                continue
                            repr_id = _require_canonical_id(
                                str(repr_id), str(uv_manifest)
                            )
                            repr_table = self._repr_table(
                                zangstuk_id, variant_id, uv_id
                            )
                            repr_aliases = repr_entry.get("aliases") or []
                            _register_aliases(
                                repr_table,
                                repr_id,
                                [repr_id, *repr_aliases],
                                ctx_uv,
                            )
                            file_rel = repr_entry.get("file")
                            if file_rel:
                                self._register_vsa_file(
                                    zangstuk_id=zangstuk_id,
                                    variant_id=variant_id,
                                    uitvoeringsvorm_id=uv_id,
                                    representatie_id=repr_id,
                                    path=(uv_dir / str(file_rel)),
                                    origin=origin,
                                    title=title,
                                    gelegenheid=variant_gelegenheid,
                                    gelegenheidstype=variant_gelegenheidstype,
                                    toon=variant_toon,
                                    referentie=variant_referentie,
                                    extra_search_texts=_collect_alias_texts(
                                        aliases,
                                        generated_aliases,
                                        uv_aliases,
                                        repr_aliases,
                                        zangstuk_id,
                                        variant_id,
                                        uv_id,
                                        repr_id,
                                    ),
                                )

                    uv_table = self._uv_table(zangstuk_id, variant_id)
                    _register_aliases(uv_table, uv_id, uv_aliases, ctx_uv)

    def _scan_bron_zangstukken(self, zangstukken_root: Path, origin: Origin) -> None:
        for zangstuk_dir in sorted(p for p in zangstukken_root.iterdir() if p.is_dir()):
            zangstuk_id = _require_canonical_id(
                zangstuk_dir.name, str(zangstuk_dir)
            )
            yaml_path = zangstuk_dir / "zangstuk.yaml"
            aliases: list[object] = [zangstuk_id]
            gelegenheid: str | None = None
            gelegenheidstype: str | None = None
            toon: str | None = None
            title: str | None = None
            generated_aliases: list[str] = []
            if yaml_path.is_file():
                data = _load_yaml(yaml_path)
                yaml_id = str(data.get("id", zangstuk_id))
                _require_canonical_id(yaml_id, str(yaml_path))
                if yaml_id != zangstuk_id:
                    raise InvalidIdError(
                        yaml_id,
                        f"{yaml_path}: id komt niet overeen met mapnaam '{zangstuk_id}'",
                    )
                title = _metadata_str(data.get("title"))
                gelegenheid = _metadata_str(data.get("gelegenheid"))
                gelegenheidstype = _metadata_str(data.get("gelegenheidstype"))
                toon = _metadata_str(data.get("toon"))
                if title:
                    aliases.append(title)
                raw_aliases = data.get("aliases") or []
                manual_aliases, generated_aliases = partition_yaml_aliases(
                    yaml_path, raw_aliases
                )
                aliases.extend(manual_aliases)
                for source in data.get("sources") or []:
                    if not isinstance(source, dict):
                        continue
                    source_id = source.get("id")
                    if not source_id:
                        continue
                    source_id = _require_canonical_id(
                        str(source_id), str(yaml_path)
                    )
                    uv_table = self._uv_table(zangstuk_id, zangstuk_id)
                    source_aliases: list[object] = [source_id]
                    source_aliases.extend(source.get("aliases") or [])
                    _register_aliases(
                        uv_table,
                        source_id,
                        source_aliases,
                        str(yaml_path),
                    )
                    file_rel = source.get("file")
                    if file_rel:
                        self._register_vsa_file(
                            zangstuk_id=zangstuk_id,
                            variant_id=zangstuk_id,
                            uitvoeringsvorm_id=source_id,
                            representatie_id=source_id,
                            path=(zangstuk_dir / str(file_rel)),
                            origin=origin,
                            title=title,
                            gelegenheid=gelegenheid,
                            gelegenheidstype=gelegenheidstype,
                            toon=toon,
                            referentie=_metadata_str(source.get("reference")),
                            extra_search_texts=_collect_alias_texts(
                                aliases,
                                generated_aliases,
                                source_aliases,
                                zangstuk_id,
                                source.get("description"),
                                source.get("author"),
                                source.get("composer"),
                            ),
                        )
                        repr_table = self._repr_table(
                            zangstuk_id, zangstuk_id, source_id
                        )
                        _register_aliases(
                            repr_table,
                            source_id,
                            [source_id],
                            str(yaml_path),
                        )

            _register_aliases(
                self.zangstuk, zangstuk_id, aliases, str(zangstuk_dir)
            )
            # Plat bron-model: source-entries hangen onder (zangstuk-id, zangstuk-id).
            variant_table = self._variant_table(zangstuk_id)
            _register_aliases(
                variant_table, zangstuk_id, [zangstuk_id], str(zangstuk_dir)
            )

    def resolve_zangstuk(self, invoer: str) -> str:
        return self.zangstuk.resolve("zangstuk", invoer, "globaal")

    def resolve_variant(self, zangstuk_id: str, invoer: str) -> str:
        zangstuk_id = self.resolve_zangstuk(zangstuk_id)
        table = self.variant.get(zangstuk_id)
        if table is None:
            raise NotFoundError(
                "variant", invoer, f"zangstuk-id={zangstuk_id}"
            )
        return table.resolve("variant", invoer, f"zangstuk-id={zangstuk_id}")

    def resolve_uitvoeringsvorm(
        self, zangstuk_id: str, variant_id: str, invoer: str
    ) -> str:
        zangstuk_id = self.resolve_zangstuk(zangstuk_id)
        variant_id = self.resolve_variant(zangstuk_id, variant_id)
        key = (zangstuk_id, variant_id)
        table = self.uitvoeringsvorm.get(key)
        if table is None:
            raise NotFoundError(
                "uitvoeringsvorm",
                invoer,
                f"zangstuk-id={zangstuk_id}, variant-id={variant_id}",
            )
        return table.resolve(
            "uitvoeringsvorm",
            invoer,
            f"zangstuk-id={zangstuk_id}, variant-id={variant_id}",
        )

    def resolve_representatie(
        self,
        zangstuk_id: str,
        variant_id: str,
        uitvoeringsvorm_id: str,
        invoer: str,
    ) -> str:
        zangstuk_id = self.resolve_zangstuk(zangstuk_id)
        variant_id = self.resolve_variant(zangstuk_id, variant_id)
        uitvoeringsvorm_id = self.resolve_uitvoeringsvorm(
            zangstuk_id, variant_id, uitvoeringsvorm_id
        )
        key = (zangstuk_id, variant_id, uitvoeringsvorm_id)
        table = self.representatie.get(key)
        if table is None:
            raise NotFoundError(
                "representatie",
                invoer,
                (
                    f"zangstuk-id={zangstuk_id}, variant-id={variant_id}, "
                    f"uitvoeringsvorm-id={uitvoeringsvorm_id}"
                ),
            )
        return table.resolve(
            "representatie",
            invoer,
            (
                f"zangstuk-id={zangstuk_id}, variant-id={variant_id}, "
                f"uitvoeringsvorm-id={uitvoeringsvorm_id}"
            ),
        )

    def resolve_vsa_path(self, reference: str) -> Path:
        """Materialiseer logische referentie naar een `.vsa`-bestandspad."""
        try:
            scope, segments = parse_logical_reference(reference)
        except IncludeRefError as exc:
            raise PathNotFoundError(str(exc)) from exc

        if len(segments) == 2:
            zangstuk_id = self.resolve_zangstuk(segments[0])
            uitvoeringsvorm_id = self.resolve_uitvoeringsvorm(
                zangstuk_id, zangstuk_id, segments[1]
            )
            variant_id = zangstuk_id
            representatie_id: str | None = None
        elif len(segments) == 3:
            zangstuk_id = self.resolve_zangstuk(segments[0])
            variant_id = self.resolve_variant(zangstuk_id, segments[1])
            uitvoeringsvorm_id = self.resolve_uitvoeringsvorm(
                zangstuk_id, variant_id, segments[2]
            )
            representatie_id = None
        elif len(segments) == 4:
            zangstuk_id = self.resolve_zangstuk(segments[0])
            variant_id = self.resolve_variant(zangstuk_id, segments[1])
            uitvoeringsvorm_id = self.resolve_uitvoeringsvorm(
                zangstuk_id, variant_id, segments[2]
            )
            representatie_id = self.resolve_representatie(
                zangstuk_id, variant_id, uitvoeringsvorm_id, segments[3]
            )
        else:
            raise PathNotFoundError(
                f"Logische referentie vereist 2–4 segmenten: {reference!r}"
            )

        matches = [
            entry
            for entry in self.vsa_files
            if entry.zangstuk_id == zangstuk_id
            and entry.variant_id == variant_id
            and entry.uitvoeringsvorm_id == uitvoeringsvorm_id
            and (scope == "id" or entry.origin == scope)
            and (
                representatie_id is None
                or entry.representatie_id == representatie_id
            )
        ]
        if representatie_id is None:
            unique_paths = {str(entry.path) for entry in matches}
            if len(unique_paths) == 1:
                return matches[0].path
            if len(unique_paths) > 1:
                raise AmbiguousPathError(
                    f"Meerdere representaties voor {reference!r}; "
                    "geef een vierde segment (representatie-id)",
                    sorted(unique_paths),
                )
            raise PathNotFoundError(
                f"Geen .vsa-bestand gevonden voor {reference!r}"
            )

        if len(matches) == 1:
            return matches[0].path
        if len(matches) > 1:
            raise AmbiguousPathError(
                f"Meerdere .vsa-bestanden voor {reference!r}",
                sorted({str(entry.path) for entry in matches}),
            )
        raise PathNotFoundError(f"Geen .vsa-bestand gevonden voor {reference!r}")


def _metadata_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _collect_alias_texts(*values: object) -> list[str]:
    texts: list[str] = []
    for value in values:
        if value is None:
            continue
        if isinstance(value, str):
            if value.strip():
                texts.append(value)
            continue
        if isinstance(value, dict) and "text" in value:
            text = str(value["text"]).strip()
            if text:
                texts.append(text)
            continue
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
            texts.extend(_collect_alias_texts(*value))
    return texts


def _load_alias_register_for_build(
    *,
    content_root: Path | None,
    bron_root: Path | None,
    fixture_root: Path | None,
) -> AliasBlokRegister | None:
    for root in (bron_root, content_root, fixture_root):
        if root is not None:
            register = try_load_alias_register(bron_root=root.resolve())
            if register is not None:
                return register
    return try_load_alias_register()


def _expand_search_values(
    values: tuple[object, ...], register: AliasBlokRegister | None
) -> tuple[object, ...]:
    if register is None:
        return values
    expanded: list[object] = []
    for value in values:
        if isinstance(value, str):
            expanded.extend(register.expand_term(value))
        elif isinstance(value, dict) and "text" in value:
            expanded.extend(register.expand_term(str(value["text"])))
            expanded.append(value)
        else:
            expanded.append(value)
    return tuple(expanded)


def _build_search_terms(
    *values: object, register: AliasBlokRegister | None = None
) -> frozenset[str]:
    values = _expand_search_values(values, register)
    terms: set[str] = set()
    for value in values:
        if value is None:
            continue
        if isinstance(value, str):
            norm = normalize_for_match(value)
            if not norm:
                continue
            terms.add(norm)
            for token in re.split(r"[\s\-_/(),]+", norm):
                if len(token) >= 2:
                    terms.add(token)
            continue
        if isinstance(value, dict) and "text" in value:
            terms.update(_build_search_terms(str(value["text"])))
            continue
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict)):
            terms.update(_build_search_terms(*value))
    return frozenset(terms)
