---
doc_type: cli-man-page
audience: "P1 — Parochie-docs-maintainer; P5 — Docs-/tool-contributor"
---
# Catalogus-tool

De **catalogus**-CLI bouwt een [alias](@)-index uit [manifesten](@) en mappad, en lost
invoer op naar **[canoniek id](@)** volgens [terminologie §2.8](../specs/terminologie.md).

**Gebruikersverhalen** (workflows, beoogde GUI): [Catalogus — handleidingen](../manuals/catalogus/index.md).

**Sjablonen** (`:::include zoek=`, `default`, [`vsa resolve-catalogus`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/resolve-catalogus/)): [catalogus-samenstelling-zangstuk.md](../specs/catalogus-samenstelling-zangstuk.md).

## Installatie

Gebruik steeds **`python -m`** voor pip, pytest en catalogus — dan hoef je
`Scripts` niet op PATH te zetten en voorkom je mismatch tussen meerdere
Python-installaties op Windows.

```cmd
cd /d C:\Git\orthodox-ronl\bron
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

| Commando                                                      | Doel                                                 |
| ------------------------------------------------------------- | ---------------------------------------------------- |
| [`catalogus zoek`](#catalogus-zoek)                           | Vrije tekst + context → catalogus-pad                |
| [`catalogus resolve`](#catalogus-resolve)                     | [Alias](@) → [canoniek id](@) (per niveau)           |
| [`catalogus index validate`](#catalogus-index-validate)       | [Manifesten](@) en [alias](@)-conflicten controleren |
| [`catalogus aliases validate`](#catalogus-aliases-validate)   | Org-breed alias-blokkenregister valideren            |
| [`catalogus aliases sync`](#catalogus-aliases-sync)           | Gegenereerde alias-blokken naar yaml schrijven       |

### `catalogus zoek`

Vrije tekst + `default.*`-context → **catalogus-pad** (`lokaal:…` / `bron:…`).

Normatief contract: [catalogus-zoek-api.md](../specs/catalogus-zoek-api.md).

- **`zoek`** — strict: 0 / 1 / meerdere → fout of één pad.
- **`zoek_kandidaten`** — alle matches (review, `--lijst`).
- Default **`bestandsextensie`**: `.vsa`.

```cmd
python -m catalogus.cli zoek "Troparion" ^
  --content-root ..\VSA-demo\content-source ^
  --bron-root . ^
  --default-gelegenheid geboorte-moeder-gods

python -m catalogus.cli zoek "Cherubijnenhymne (Kastorski)" ^
  --content-root ..\VSA-demo\content-source ^
  --bron-root .
```

**Status:** **geïmplementeerd** (basis). Exitcode **1** = geen match of ambiguïteit (strict);
**0 regels** met `--lijst` = exit **1**.

**Parochie-context:** `--content-root` = parochie content-source (`lokaal/`); `--bron-root` =
org-bron. **Lokaal vóór bron**; bij lokaal-winst kan **`ZoekResult.ook_gevonden_in_bron`**
gevuld zijn — toon met **`--verbose`** (waarschuwing op stderr).

### `catalogus resolve`

Los [alias](@) of hoofdletter-variant op naar [canoniek id](@).

```cmd
python -m catalogus.cli resolve zangstuk "1e antifoon weekdagen" --content-root ..\VSA-demo\content-source
python -m catalogus.cli resolve uitvoeringsvorm --zangstuk antifoon-1-weekdagen --variant liturgikon-weekdagen Hemelum --content-root ..\VSA-demo\content-source
```

Niveaus: [zangstuk](@), [variant](@), [uitvoeringsvorm](@), [representatie](@).

Scope-flags:

| Niveau               | Verplichte flags                               |
| -------------------- | ---------------------------------------------- |
| [zangstuk](@)        | —                                              |
| [variant](@)         | `--zangstuk`                                   |
| [uitvoeringsvorm](@) | `--zangstuk`, `--variant`                      |
| [representatie](@)   | `--zangstuk`, `--variant`, `--uitvoeringsvorm` |

Index-bronnen (minstens één verplicht):

| Flag             | Inhoud                                                   |
| ---------------- | -------------------------------------------------------- |
| `--content-root` | Parochie content-source (met `lokaal/`)                  |
| `--bron-root`    | [Bron-repository](@) (met `zangstukken/`)                |
| `--fixture-root` | Extra root (tests, offline fixtures)                     |

### `catalogus index validate`

Controleer [manifesten](@) op ongeldige ids en [alias](@)-conflicten binnen scope.

```cmd
python -m catalogus.cli index validate --bron-root .
python -m catalogus.cli index validate --content-root ..\VSA-demo\content-source
```

### `catalogus aliases validate`

Valideer org-breed aliassen-register `catalogus/data/alias-blokken.yaml`
(geen overlap tussen blokken, geen lege lijsten). Zie
[alias-blokken-ontwerp](../plans/alias-blokken-ontwerp.md).

```cmd
python -m catalogus.cli aliases validate --bron-root .
```

### `catalogus aliases sync`

Schrijf gegenereerde alias-blokken naar `zangstuk.yaml` / `variant.yaml`. Handmatige
[aliassen](@) blijven boven het marker-blok; gegenereerde termen tellen alleen mee voor
**zoek** (niet voor resolver-scope — voorkomt conflicten tussen meerdere kondak/tropaar-stukken).

Trigger: `liturgische_rol:` / `alias_blok:` in yaml, anders id-prefix of term-fallback
(bijv. `kondak-zondag-toon-1` → blok `kondak`).

```cmd
python -m catalogus.cli aliases sync --bron-root .
python -m catalogus.cli aliases sync --check --bron-root .
python -m catalogus.cli aliases sync --dry-run --bron-root .
```

## Index-bronnen

De index wordt in het geheugen opgebouwd uit:

1. **Mappad** — mapnamen onder `lokaal/<zangstuk-id>/<variant-id>/<uitvoeringsvorm-id>/`
2. **[Manifesten](@)** — `variant.yaml`, `uitvoeringsvorm.yaml` (`aliases:` per entiteit)
3. **Bron** — `zangstukken/<zangstuk-id>/zangstuk.yaml` (`title`, `sources[].id`)
4. **Alias-blokken** — `catalogus/data/alias-blokken.yaml` breidt zoektermen uit (runtime)

Zie [parochie-lokaal zangstukken](../manuals/parochie-lokaal-zangstukken.md) voor
[manifest](@)-structuur.

## Resolver-contract

1. Normaliseer invoer: `strip()` + Unicode `casefold()`
2. Match [canoniek id](@) of geregistreerde [alias](@) binnen scope
3. Resultaat: [canoniek id](@), of fout (`NotFoundError`, `AmbiguousError`)

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

# Zoek-API (geïmplementeerd, basis):
ctx = ZoekContext.from_default_mapping(
    {"gelegenheid": "geboorte-moeder-gods"}
)
# lijst = zoek_kandidaten("Troparion", index=index, context=ctx)
# lijst.catalogus_paden
# result = zoek("Troparion", index=index, context=ctx)  # strict: 0/1/meerdere
```

Zie [catalogus-zoek-api.md](../specs/catalogus-zoek-api.md) voor volledig contract.

## Relatie tot VSA

- **Fase 2:** `catalogus` staat los van `vsa`; build/includes gebruikten relatieve paden.
- **Fase 3:** [VSA-tooling](@) importeert `catalogus` bij `id:…` / `lokaal:…` / `bron:…`-includes in markdown.
- **Fase 4:** `:::include zoek=` / `@include-vsa zoek=` → **`catalogus.zoek`**
  → catalogus-pad — [catalogus-zoek-api.md](../specs/catalogus-zoek-api.md) (**geïmplementeerd**, basis).

Zie [verhaal 1](../manuals/catalogus/rene-liturgie-geboorte-moeder-gods.md) en
[VSA — resolve-catalogus](https://orthodox-ronl.github.io/VSA-tooling/guides/parochie-lokaal-vsa/#vsa-resolve-catalogus).

## Tests

```cmd
cd /d C:\Git\orthodox-ronl\bron
scripts\test.cmd
```

Of handmatig:

```cmd
python -m pip install -e ".[dev]"
python -m pytest
```
