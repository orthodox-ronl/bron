# Catalogus-tool

De **catalogus**-CLI bouwt een alias-index uit manifesten en mappad, en lost
invoer op naar **canoniek id** volgens [terminologie §2.8](../specs/terminologie.md).

**Gebruikersverhalen** (workflows, beoogde GUI): [Catalogus — handleidingen](../manuals/catalogus/index.md).

**Sjablonen** (`:::include zoek=`, `default`, `vsa resolve-catalogus`): [catalogus-samenstelling-zangstuk.md](../specs/catalogus-samenstelling-zangstuk.md).

## Installatie

Gebruik steeds **`python -m`** voor pip, pytest en catalogus — dan hoef je
`Scripts` niet op PATH te zetten en voorkom je mismatch tussen meerdere
Python-installaties op Windows.

```cmd
cd /d C:\Git\orthodox-groningen\bron
python -m pip install -e ".[dev]"
```

Alleen runtime (zonder pytest):

```cmd
python -m pip install -e .
```

Of via het testscript (installeert + pytest):

```cmd
scripts\test.cmd
```

## Commando's (fase 2)

### `catalogus zoek` (API-contract fase 0)

Vrije tekst + `default.*`-context → **catalogus-pad** (`lokaal:…` / `bron:…`).

Normatief contract: [catalogus-zoek-api.md](../specs/catalogus-zoek-api.md).

- **`zoek`** — strict: 0 / 1 / meerdere → fout of één pad.
- **`zoek_kandidaten`** — alle matches (review, `--lijst`).
- Default **`bestandsextensie`**: `.vsa`.

```cmd
python -m catalogus.cli zoek "Troparion" ^
  --content-root ..\VSA-tooling\examples\hugo-demo\content-source ^
  --bron-root . ^
  --default-gelegenheid geboorte-moeder-gods ^
  --default-uitvoeringsvorm Groningen

python -m catalogus.cli zoek "Troparion" --lijst --bron-root .
```

**Status:** CLI en Python-API aanwezig; **`zoek_kandidaten()`** werpt `NotImplementedError` tot fase 4.
Exitcode **2** = nog niet geïmplementeerd; **1** = geen match (na implementatie).

### `catalogus resolve`

Los alias of hoofdletter-variant op naar canoniek id.

```cmd
python -m catalogus.cli resolve zangstuk "1e antifoon weekdagen" --content-root ..\VSA-tooling\examples\hugo-demo\content-source
python -m catalogus.cli resolve uitvoeringsvorm --zangstuk antifoon-1-weekdagen --variant liturgikon-weekdagen Hemelum --content-root ..\VSA-tooling\examples\hugo-demo\content-source
```

Niveaus: `zangstuk`, `variant`, `uitvoeringsvorm`, `representatie`.

Scope-flags:

| Niveau          | Verplichte flags                                      |
| --------------- | ----------------------------------------------------- |
| zangstuk        | —                                                     |
| variant         | `--zangstuk`                                          |
| uitvoeringsvorm | `--zangstuk`, `--variant`                             |
| representatie   | `--zangstuk`, `--variant`, `--uitvoeringsvorm`        |

Index-bronnen (minstens één verplicht):

| Flag              | Inhoud                                              |
| ----------------- | --------------------------------------------------- |
| `--content-root`  | Parochie content-source (met `lokaal/`)             |
| `--bron-root`     | Bron-repository (met `zangstukken/`)                |
| `--fixture-root`  | Extra root (tests, offline fixtures)                |

### `catalogus index validate`

Controleer manifesten op ongeldige ids en alias-conflicten binnen scope.

```cmd
python -m catalogus.cli index validate --bron-root .
python -m catalogus.cli index validate --content-root ..\VSA-tooling\examples\hugo-demo\content-source
```

## Index-bronnen

Er is **geen** centraal alias-bestand. De index wordt in het geheugen opgebouwd uit:

1. **Mappad** — mapnamen onder `lokaal/<zangstuk-id>/<variant-id>/<uitvoeringsvorm-id>/`
2. **Manifesten** — `variant.yaml`, `uitvoeringsvorm.yaml` (`aliases:` per entiteit)
3. **Bron** — `zangstukken/<zangstuk-id>/zangstuk.yaml` (`title`, `sources[].id`)

Zie [parochie-lokaal zangstukken](../manuals/parochie-lokaal-zangstukken.md) voor manifest-structuur.

## Resolver-contract

1. Normaliseer invoer: `strip()` + Unicode `casefold()`
2. Match canoniek id of geregistreerde alias binnen scope
3. Resultaat: canoniek id `[a-z0-9_-]+`, of fout (`NotFoundError`, `AmbiguousError`)

`lang` in alias-yaml is metadata; matching negeert taal (casefold op `text`).

## Python-library

```python
from pathlib import Path
from catalogus import (
    AliasIndex,
    ZoekContext,
    format_catalogus_pad,
    zoek,
    zoek_kandidaten,
    zoek_met_roots,
)

index = AliasIndex.build(
    content_root=Path("content-source"),
    bron_root=Path("."),
)
index.resolve_uitvoeringsvorm(
    "antifoon-1-weekdagen", "liturgikon-weekdagen", "Hemelum"
)
# → "hemelum"

# Zoek-API (contract fase 0 — zoek_kandidaten() stub tot fase 4):
ctx = ZoekContext.from_default_mapping(
    {"gelegenheid": "geboorte-moeder-gods", "uitvoeringsvorm": "Groningen"}
)
# lijst = zoek_kandidaten("Troparion", index=index, context=ctx)
# lijst.catalogus_paden
# result = zoek("Troparion", index=index, context=ctx)  # strict: 0/1/meerdere
```

Zie [catalogus-zoek-api.md](../specs/catalogus-zoek-api.md) voor volledig contract.

## Relatie tot VSA

- **Fase 2:** `catalogus` staat los van `vsa`; build/includes gebruikten relatieve paden.
- **Fase 3:** VSA-tooling importeert `catalogus` bij `id:…` / `lokaal:…` / `bron:…`-includes in markdown.
- **Fase 4 (contract fase 0):** `:::include zoek=` / `@include-vsa zoek=` → **`catalogus.zoek`**
  → catalogus-pad — [API-contract](../specs/catalogus-zoek-api.md); implementatie gepland.

## Geplande commando's (fase 4)

| Commando | Repo | Doel |
| -------- | ---- | ---- |
| `catalogus zoek` | bron | **Contract fase 0** — implementatie volgt; zie [catalogus-zoek-api.md](../specs/catalogus-zoek-api.md) |
| **`vsa resolve-catalogus`** | VSA-tooling | Markdown: alle `zoek=` → `bron:…` / `lokaal:…` |
| **`@include-vsa`** expand | VSA-tooling | `.vsa`: `zoek=` → in-memory body-splice via `catalogus.zoek` |

Tot implementatie: per stuk `catalogus resolve`, of handmatig catalogus-pad in
`:::include` — zie [verhaal 1](../manuals/catalogus/rene-liturgie-geboorte-moeder-gods.md)
en [VSA — resolve-catalogus](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/parochie-lokaal-vsa.md#vsa-resolve-catalogus).

## Tests

```cmd
cd /d C:\Git\orthodox-groningen\bron
scripts\test.cmd
```

Of handmatig:

```cmd
python -m pip install -e ".[dev]"
python -m pytest
```
