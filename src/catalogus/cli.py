from __future__ import annotations

import argparse
import sys
from pathlib import Path

from catalogus.alias_blokken import (
    default_register_path,
    load_alias_register,
)
from catalogus.alias_index import AliasIndex
from catalogus.alias_sync import load_register_for_sync, run_alias_sync
from catalogus.errors import (
    AliasRegisterError,
    AliasSyncError,
    AmbiguousError,
    CatalogusError,
    IndexConflictError,
    InvalidIdError,
    NotFoundError,
)
from catalogus.zoek import (
    ZoekContext,
    parse_bestandsextensie,
    zoek_kandidaten_met_roots,
    zoek_met_roots,
)


def _add_root_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--content-root",
        type=Path,
        default=None,
        help="Pad naar content-source (met optionele lokaal/ submap)",
    )
    parser.add_argument(
        "--bron-root",
        type=Path,
        default=None,
        help="Pad naar bron-repository (met zangstukken/)",
    )
    parser.add_argument(
        "--fixture-root",
        type=Path,
        default=None,
        help="Extra root voor test-fixtures (met lokaal/ of zangstukken/)",
    )


def _build_index(args: argparse.Namespace) -> AliasIndex:
    if not any((args.content_root, args.bron_root, args.fixture_root)):
        raise SystemExit(
            "Geef minstens één van --content-root, --bron-root of --fixture-root"
        )
    return AliasIndex.build(
        content_root=args.content_root,
        bron_root=args.bron_root,
        fixture_root=args.fixture_root,
    )


def _cmd_resolve(args: argparse.Namespace) -> int:
    index = _build_index(args)
    niveau = args.niveau
    try:
        if niveau == "zangstuk":
            result = index.resolve_zangstuk(args.invoer)
        elif niveau == "variant":
            if not args.zangstuk:
                raise SystemExit("--zangstuk is verplicht voor variant")
            result = index.resolve_variant(args.zangstuk, args.invoer)
        elif niveau == "uitvoeringsvorm":
            if not args.zangstuk or not args.variant:
                raise SystemExit(
                    "--zangstuk en --variant zijn verplicht voor uitvoeringsvorm"
                )
            result = index.resolve_uitvoeringsvorm(
                args.zangstuk, args.variant, args.invoer
            )
        elif niveau == "representatie":
            if not args.zangstuk or not args.variant or not args.uitvoeringsvorm:
                raise SystemExit(
                    "--zangstuk, --variant en --uitvoeringsvorm zijn verplicht "
                    "voor representatie"
                )
            result = index.resolve_representatie(
                args.zangstuk,
                args.variant,
                args.uitvoeringsvorm,
                args.invoer,
            )
        else:
            raise SystemExit(f"Onbekend niveau: {niveau}")
    except (NotFoundError, AmbiguousError, InvalidIdError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(result)
    return 0


def _cmd_index_validate(args: argparse.Namespace) -> int:
    try:
        index = _build_index(args)
    except (IndexConflictError, InvalidIdError) as exc:
        print(exc, file=sys.stderr)
        return 1
    conflicts = index.validate()
    if conflicts:
        print(
            f"Alias-index bevat {len(conflicts)} conflict(en):",
            file=sys.stderr,
        )
        for conflict in conflicts:
            print(f"  - {conflict}", file=sys.stderr)
        return 1
    print("OK — geen alias-conflicten")
    return 0


def _cmd_aliases_validate(args: argparse.Namespace) -> int:
    path = args.register
    if path is None:
        path = default_register_path(bron_root=args.bron_root)
    try:
        register = load_alias_register(path)
    except AliasRegisterError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"OK — {len(register.blokken)} alias-blokken in {path}")
    return 0


def _cmd_aliases_sync(args: argparse.Namespace) -> int:
    if args.bron_root is None and args.content_root is None:
        args.bron_root = Path.cwd()

    try:
        register = load_register_for_sync(
            register_path=args.register,
            bron_root=args.bron_root,
        )
    except AliasRegisterError as exc:
        print(exc, file=sys.stderr)
        return 1

    if not any((args.content_root, args.bron_root)):
        raise SystemExit("Geef --bron-root en/of --content-root")

    try:
        results = run_alias_sync(
            register=register,
            bron_root=args.bron_root,
            content_root=args.content_root,
            dry_run=args.dry_run,
            check=args.check,
        )
    except AliasSyncError as exc:
        print(exc, file=sys.stderr)
        return 1

    changed = [r for r in results if r.changed]
    skipped = [r for r in results if r.skipped]

    for result in changed:
        prefix = "would update" if (args.dry_run or args.check) else "updated"
        print(f"{prefix}: {result.path} (alias-blok {result.blok_id})")

    if args.check and changed:
        print(
            f"Drift: {len(changed)} bestand(en) niet gesynchroniseerd",
            file=sys.stderr,
        )
        return 1

    if args.verbose:
        print(f"skipped: {len(skipped)}", file=sys.stderr)
        for result in skipped:
            print(f"  skip {result.path}: {result.reason}", file=sys.stderr)

    action = "check OK" if args.check else "sync OK"
    print(
        f"{action} — {len(results)} manifest(en), "
        f"{len(changed)} gewijzigd, {len(skipped)} overgeslagen"
    )
    return 0


def _cmd_zoek(args: argparse.Namespace) -> int:
    context = ZoekContext(
        gelegenheid=args.default_gelegenheid,
        gelegenheidstype=args.default_gelegenheidstype,
        toon=args.default_toon,
        uitvoeringsvorm=args.default_uitvoeringsvorm,
        gelegenheidsdatum=args.default_gelegenheidsdatum,
        referentie=args.default_referentie,
        bronnen=ZoekContext.from_default_mapping({}, bronnen=args.bronnen).bronnen,
    )
    bestandsextensie = parse_bestandsextensie(args.bestandsextensie)
    zoek_kwargs = {
        "content_root": args.content_root,
        "bron_root": args.bron_root,
        "fixture_root": args.fixture_root,
        "context": context,
        "bestandsextensie": bestandsextensie,
    }
    try:
        if args.lijst:
            lijst = zoek_kandidaten_met_roots(args.query, **zoek_kwargs)
            if not lijst.matches:
                print("Geen matches", file=sys.stderr)
                return 1
            for match in lijst.matches:
                print(match.catalogus_pad)
            return 0
        result = zoek_met_roots(args.query, **zoek_kwargs)
    except NotImplementedError as exc:
        print(exc, file=sys.stderr)
        return 2
    except (NotFoundError, AmbiguousError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    if args.verbose:
        print(f"pad: {result.path}", file=sys.stderr)
        print(
            f"ids: {result.entry.zangstuk_id}/"
            f"{result.entry.variant_id}/"
            f"{result.entry.uitvoeringsvorm_id}",
            file=sys.stderr,
        )
        if result.has_ook_in_bron:
            print(
                "Ook gevonden in bron: " + ", ".join(result.ook_gevonden_in_bron),
                file=sys.stderr,
            )
    print(result.catalogus_pad)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="catalogus",
        description="Zangstuk-catalogus: alias-resolver en index-validatie",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    resolve = sub.add_parser(
        "resolve",
        help="Los invoer op naar canoniek id (bron §2.8)",
    )
    resolve.add_argument(
        "niveau",
        choices=["zangstuk", "variant", "uitvoeringsvorm", "representatie"],
    )
    resolve.add_argument("invoer", help="Alias of canoniek id (invoergrens)")
    resolve.add_argument("--zangstuk", help="Scope: zangstuk-id of alias")
    resolve.add_argument("--variant", help="Scope: variant-id of alias")
    resolve.add_argument(
        "--uitvoeringsvorm",
        help="Scope: uitvoeringsvorm-id of alias (alleen representatie)",
    )
    _add_root_args(resolve)
    resolve.set_defaults(func=_cmd_resolve)

    index = sub.add_parser("index", help="Index-onderhoud")
    index_sub = index.add_subparsers(dest="index_command", required=True)

    validate = index_sub.add_parser(
        "validate",
        help="Controleer manifesten op alias-conflicten en ongeldige ids",
    )
    _add_root_args(validate)
    validate.set_defaults(func=_cmd_index_validate)

    aliases = sub.add_parser("aliases", help="Org-breed aliassen-register (alias-blokken)")
    aliases_sub = aliases.add_subparsers(dest="aliases_command", required=True)

    aliases_validate = aliases_sub.add_parser(
        "validate",
        help="Valideer catalogus/data/alias-blokken.yaml",
    )
    aliases_validate.add_argument(
        "--register",
        type=Path,
        default=None,
        help="Pad naar alias-blokken.yaml (default: onder --bron-root of repo-root)",
    )
    _add_root_args(aliases_validate)
    aliases_validate.set_defaults(func=_cmd_aliases_validate)

    aliases_sync = aliases_sub.add_parser(
        "sync",
        help="Schrijf gegenereerde alias-blokken naar manifesten",
    )
    aliases_sync.add_argument(
        "--register",
        type=Path,
        default=None,
        help="Pad naar alias-blokken.yaml (default: onder --bron-root of repo-root)",
    )
    aliases_sync.add_argument(
        "--dry-run",
        action="store_true",
        help="Toon wijzigingen zonder te schrijven",
    )
    aliases_sync.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 bij drift (yaml wijkt af van register)",
    )
    aliases_sync.add_argument(
        "--verbose",
        action="store_true",
        help="Toon overgeslagen manifesten op stderr",
    )
    _add_root_args(aliases_sync)
    aliases_sync.set_defaults(func=_cmd_aliases_sync)

    zoek_cmd = sub.add_parser(
        "zoek",
        help="Vrije tekst + default-context → catalogus-pad (API-contract fase 0)",
    )
    zoek_cmd.add_argument("query", help="Zoekstring (liturgische rol, titel, alias, …)")
    zoek_cmd.add_argument(
        "--default-gelegenheid",
        dest="default_gelegenheid",
        default=None,
        help="Filter: canoniek gelegenheid-id",
    )
    zoek_cmd.add_argument(
        "--default-gelegenheidstype",
        dest="default_gelegenheidstype",
        default=None,
        help="Filter: vast-feest | zondag-cyclus",
    )
    zoek_cmd.add_argument(
        "--default-toon",
        dest="default_toon",
        default=None,
        help="Filter: zondagstoonsysteem",
    )
    zoek_cmd.add_argument(
        "--default-uitvoeringsvorm",
        dest="default_uitvoeringsvorm",
        default=None,
        help="Default uitvoeringsvorm (alias toegestaan)",
    )
    zoek_cmd.add_argument(
        "--default-gelegenheidsdatum",
        dest="default_gelegenheidsdatum",
        default=None,
        help='Filter: "MM-DD"',
    )
    zoek_cmd.add_argument(
        "--default-referentie",
        dest="default_referentie",
        default=None,
        help="Herkomst-filter (§9 terminologie); geen catalogus-pad",
    )
    zoek_cmd.add_argument(
        "--bronnen",
        default=None,
        help="Doorzoekbare herkomsten: bron, lokaal, of bron,lokaal (default: beide)",
    )
    zoek_cmd.add_argument(
        "--bestandsextensie",
        default=None,
        help="Suffix-filter: vsa (default), pdf, alle, of komma-lijst (vsa,pdf)",
    )
    zoek_cmd.add_argument(
        "--lijst",
        action="store_true",
        help="Alle matches (catalogus-paden), i.p.v. strict één resultaat",
    )
    zoek_cmd.add_argument(
        "--verbose",
        action="store_true",
        help="Pad, ids en bron-hint op stderr (strict modus)",
    )
    _add_root_args(zoek_cmd)
    zoek_cmd.set_defaults(func=_cmd_zoek)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except CatalogusError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
