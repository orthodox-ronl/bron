from __future__ import annotations

import argparse
import sys
from pathlib import Path

from catalogus.alias_index import AliasIndex
from catalogus.errors import (
    AmbiguousError,
    CatalogusError,
    IndexConflictError,
    InvalidIdError,
    NotFoundError,
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

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except CatalogusError as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
