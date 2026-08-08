---
doc_type: normative-spec
audience: "P2 — Bron-contentbeheerder; P6 — Spec-/PR-reviewer"
---
# Zangstuk-formaat

Status: specificatie (juni 2026). Schema van `zangstuk.yaml` en VSA-frontmatter.

## `zangstuk.yaml`

### Verplichte velden

```yaml
id: <string>          # gelijk aan mapnaam onder zangstukken/
title: <string>

sources:              # minstens één entry
  - id: <string>      # uniek binnen dit zangstuk
    # precies één van:
    file: <relatief pad>
    access:
      note: <string>
      contact: <string>   # en/of url:
    status: nog-niet-getranscribeerd
```

### Optionele liturgische metadata

Nederlandse sleutelnamen (aligned met catalogus `ZoekContext` / sessie-`default.*`):

```yaml
gelegenheid: <string>              # canoniek gelegenheid-id of leesbare omschrijving
gelegenheidsdatum: <"MM-DD">
gelegenheidstype: vast-feest | zondag-cyclus
toon: <integer>
koormap_nummer: <string>           # bijv. "8a" — niet de scan-sorteerprefix 010-
```

### Source-entry — optionele velden

```yaml
    based_on: <source-id>       # binnen hetzelfde zangstuk
    author: <string>
    composer: <string>
    arranger: <string>
    reference: <string>
    description: <string>
    language: <string>
    copyright_status: vrij | copyrighted | onbekend
    note: <string>
```

### Regels

- Exact één van `file:` / `access:` / `status: nog-niet-getranscribeerd` per source
- `based_on` verwijst naar een andere source **binnen hetzelfde zangstuk**
- Gedeelde scan: `file: ../ander-zangstuk-id/sources/scan/bestand.pdf`

## VSA-bestanden

[VSA-bestanden](@) bevatten [VSA-notatie](@) en hebben de extensie `.vsa`.

### Platte VSA

Geen `---`-kop: platte notatietekst, volledig ondersteund.

### VSA met YAML-frontmatter (optioneel)

```yaml
---
muziek:
  do: F4
  mode: major | minor
  tempo: 80
  meter: "4/4"          # optioneel
identificatie:
  title: <string>
  subtitle: <string>
  composer: <string>
  lyricist: <string>
  rights: <string>       # weergave op export; geen vervanging copyright_status
  language: nl
  toon: 1
---
```

**Voorrangsregel:** `zangstuk.yaml` is leidend voor overlappende identificatievelden.
Frontmatter dient voor gebruik van het [vsa-bestand](@) buiten deze repository.

### Parochie-samenstelling — optioneel `default:`

Wanneer een `.vsa` **`@include-vsa zoek=`** bevat of in een parochie-context staat,
mag frontmatter een **`default:`**-blok spiegelen (zelfde sleutels als markdown-sessie):

```yaml
---
default:
  gelegenheid: geboorte-moeder-gods
  gelegenheidstype: vast-feest
  uitvoeringsvorm: Groningen
muziek:
  do: F4
  mode: major
---
```

Dit is **`ZoekContext`** voor catalogus-zoekacties op *dit* bestand — niet hetzelfde
als `gelegenheid` / `toon` op **`zangstuk.yaml`** (catalog-metadata). Zie
[catalogus-zoek-api.md](catalogus-zoek-api.md) § twee contextlagen.

## Voorbeeld

```yaml
id: troparion-zondag-toon-1
title: Troparion - Zondag, toon 1
gelegenheid: zondag
gelegenheidstype: zondag-cyclus
toon: 1
sources:
  - id: scan-koormap-010
    file: sources/scan/010-troparion-kondakion-toon-1.pdf
    author: Liturgikon
    copyright_status: vrij
  - id: groningen
    file: sources/vsa/groningen.vsa
    based_on: scan-koormap-010
    author: Parochie Groningen
    copyright_status: vrij
```

Zie [Zangstuk toevoegen](../manuals/zangstuk-toevoegen.md) voor de workflow.
