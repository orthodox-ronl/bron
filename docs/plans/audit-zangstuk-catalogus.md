---
doc_type: plan
audience: "P5 — Docs-/tool-contributor; P6 — Spec-/PR-reviewer"
---
# Audit zangstuk-catalogus (fase 1)

**Datum:** 2026-07-04  
**Doel:** handmatige review met Rene vóór hernoemen van zangstuk-id's.

## Bronnen

- **Bron-repo:** `C:\Git\orthodox-groningen\bron`
- **Content-root (lokaal):** `C:\Git\orthodox-groningen\VSA-demo\content-source`

---

## Validatie (automatisch)

### `catalogus index validate` — OK

```text
OK — geen alias-conflicten
```

### `vsa validate zangstukken` — OK

```text
OK
```

### `check_zangstuk_yaml_vsa.py` — FOUT (yaml ↔ VSA-frontmatter)

Script vergelijkt `zangstuk.yaml` met VSA-frontmatter in `sources/vsa/groningen.vsa`.
Let op: het script leest nog **`tone`** (verouderd); bron-yaml gebruikt canoniek **`toon`**.

```text
kondak-zondag-toon-{1..8}: tone yaml=None frontmatter={1..8}
troparion-zondag-toon-{1..8}: tone yaml=None frontmatter={1..8}
kondak-zondag-toon-3: reference mismatch
```

**Review-vraag:** yaml heeft wél `toon: N` — mismatch is deels **tooling** (veldnaam `tone` vs `toon`), deels inhoud (reference toon 3).

---

## Zoek-proef (Rene-workflow)

Standaard filter: alleen `.vsa`-bestanden. **PDF-scans worden niet gevonden via `zoek`.**

| Query | Context | resolve zangstuk | zoek (strict) | zoek --lijst (aantal) |
| ----- | ------- | ---------------- | ------------- | --------------------- |
| `1e antifoon weekdagen` | geen default | `antifoon-1-weekdagen` | ambigu (2 kandidaten) | 2 — zie detail |
| `1e antifoon weekdagen` | default.uitvoeringsvorm=Hemelum | `antifoon-1-weekdagen` | lokaal:antifoon-1-weekdagen/liturgikon-weekdagen/hemelum | 1 |
| `1e antifoon zondag` | geen default | `antifoon-1-zondag` | geen match | 0 |
| `Kondak` | gelegenheidstype=zondag-cyclus, toon=3 | — | bron:kondak-zondag-toon-3/kondak-zondag-toon-3/groningen | 1 |
| `Troparion` | gelegenheidstype=zondag-cyclus, toon=3 | — | bron:troparion-zondag-toon-3/troparion-zondag-toon-3/groningen | 1 |
| `Tropaar` | gelegenheidstype=zondag-cyclus, toon=3 | — | bron:troparion-zondag-toon-3/troparion-zondag-toon-3/groningen | 1 |
| `Kondakion` | gelegenheid=geboorte-moeder-gods | — | bron:kondak-geboorte-moeder-gods/kondak-geboorte-moeder-gods/liturgikon | 1 |
| `Cherubijnenhymne` | geen default | — | lokaal:cherubijnenhymne/kastorski/groningen | 1 |

### Zoek --lijst detail

**`1e antifoon weekdagen`** (geen default):

- `lokaal:antifoon-1-weekdagen/liturgikon-weekdagen/hemelum`
- `lokaal:antifoon-1-weekdagen/liturgikon-weekdagen/liturgikon`

---

## Inventaris bron (`zangstukken/`)

| zangstuk-id | title | gelegenheidstype | toon | bronbestanden | flags |
| ----------- | ----- | ---------------- | ---- | ------------- | ----- |
| `antifoon-1-zondag` | 1e antifoon (zondag) | zondag-cyclus | — | groningen:.pdf | gelegenheidssoort-in-id |
| `antifoon-2-zondag` | 2e antifoon (zondag) | zondag-cyclus | — | groningen:.pdf | gelegenheidssoort-in-id |
| `antifoon-3-zondag` | 3e antifoon (zondag) — Zaligsprekingen | zondag-cyclus | — | groningen:.pdf | gelegenheidssoort-in-id |
| `kondak-geboorte-moeder-gods` | Kondakion — Geboorte Moeder Gods | vast-feest | 4 | liturgikon:.vsa | — |
| `kondak-zondag-toon-1` | Kondak van de zondag, toon 1 | zondag-cyclus | 1 | groningen:.vsa | gelegenheidssoort-in-id |
| `kondak-zondag-toon-2` | Kondak van de zondag, toon 2 | zondag-cyclus | 2 | groningen:.vsa | gelegenheidssoort-in-id |
| `kondak-zondag-toon-3` | Kondak van de zondag, toon 3 | zondag-cyclus | 3 | groningen:.vsa | gelegenheidssoort-in-id |
| `kondak-zondag-toon-4` | Kondak van de zondag, toon 4 | zondag-cyclus | 4 | groningen:.vsa | gelegenheidssoort-in-id |
| `kondak-zondag-toon-5` | Kondak van de zondag, toon 5 | zondag-cyclus | 5 | groningen:.vsa | gelegenheidssoort-in-id |
| `kondak-zondag-toon-6` | Kondak van de zondag, toon 6 | zondag-cyclus | 6 | groningen:.vsa | gelegenheidssoort-in-id |
| `kondak-zondag-toon-7` | Kondak van de zondag, toon 7 | zondag-cyclus | 7 | groningen:.vsa | gelegenheidssoort-in-id |
| `kondak-zondag-toon-8` | Kondak van de zondag, toon 8 | zondag-cyclus | 8 | groningen:.vsa | gelegenheidssoort-in-id |
| `troparion-geboorte-moeder-gods` | Troparion — Geboorte Moeder Gods | vast-feest | 4 | liturgikon:.vsa | — |
| `troparion-melodie-toon-1` | Tropaarmelodie van de zondag, toon 1 | zondag-cyclus | 1 | koormap-scan:.jpg, koormap-scan-alt:.jpg | — |
| `troparion-melodie-toon-2` | Tropaarmelodie van de zondag, toon 2 | zondag-cyclus | 2 | koormap-scan:.jpg, koormap-scan-alt:.jpg | — |
| `troparion-melodie-toon-3` | Tropaarmelodie van de zondag, toon 3 | zondag-cyclus | 3 | koormap-scan:.jpg | — |
| `troparion-melodie-toon-4` | Tropaarmelodie van de zondag, toon 4 | zondag-cyclus | 4 | koormap-scan:.jpg, koormap-scan-alt:.jpg | — |
| `troparion-melodie-toon-5` | Tropaarmelodie van de zondag, toon 5 | zondag-cyclus | 5 | koormap-scan:.jpg, koormap-scan-alt:.jpg | — |
| `troparion-melodie-toon-6` | Tropaarmelodie van de zondag, toon 6 | zondag-cyclus | 6 | koormap-scan:.jpg | — |
| `troparion-melodie-toon-7` | Tropaarmelodie van de zondag, toon 7 | zondag-cyclus | 7 | koormap-scan:.jpg | — |
| `troparion-melodie-toon-8` | Tropaarmelodie van de zondag, toon 8 | zondag-cyclus | 8 | koormap-scan:.jpg | — |
| `troparion-zondag-toon-1` | Tropaar van de zondag, toon 1 | zondag-cyclus | 1 | groningen:.vsa | gelegenheidssoort-in-id |
| `troparion-zondag-toon-2` | Tropaar van de zondag, toon 2 | zondag-cyclus | 2 | groningen:.vsa | gelegenheidssoort-in-id |
| `troparion-zondag-toon-3` | Tropaar van de zondag, toon 3 | zondag-cyclus | 3 | groningen:.vsa | gelegenheidssoort-in-id |
| `troparion-zondag-toon-4` | Tropaar van de zondag, toon 4 | zondag-cyclus | 4 | groningen:.vsa | gelegenheidssoort-in-id |
| `troparion-zondag-toon-5` | Tropaar van de zondag, toon 5 | zondag-cyclus | 5 | groningen:.vsa | gelegenheidssoort-in-id |
| `troparion-zondag-toon-6` | Tropaar van de zondag, toon 6 | zondag-cyclus | 6 | groningen:.vsa | gelegenheidssoort-in-id |
| `troparion-zondag-toon-7` | Tropaar van de zondag, toon 7 | zondag-cyclus | 7 | groningen:.vsa | gelegenheidssoort-in-id |
| `troparion-zondag-toon-8` | Tropaar van de zondag, toon 8 | zondag-cyclus | 8 | groningen:.vsa | gelegenheidssoort-in-id |

---

## Inventaris lokaal (`content-source/lokaal/`)

| zangstuk-id | variant-id | title | gelegenheidstype | repr | flags |
| ----------- | ---------- | ----- | ---------------- | ---- | ----- |
| `antifoon-1-weekdagen` | `liturgikon-weekdagen` | 1e antifoon weekdagen (Liturgikon-melodielijn) | — | hemelum/hemelum.vsa, liturgikon/liturgikon.vsa | gelegenheidssoort-in-id (zangstuk); gelegenheidssoort-in-id (variant); gelegenheidstype-ontbreekt |
| `antifoon-2-weekdagen` | `liturgikon-weekdagen` | 2e antifoon weekdagen (Liturgikon-melodielijn) | — | hemelum/hemelum.vsa, liturgikon/liturgikon.vsa | gelegenheidssoort-in-id (zangstuk); gelegenheidssoort-in-id (variant); gelegenheidstype-ontbreekt |
| `antifoon-3-weekdagen` | `liturgikon-weekdagen` | 3e antifoon weekdagen (Liturgikon-melodielijn) | — | liturgikon/liturgikon.vsa | gelegenheidssoort-in-id (zangstuk); gelegenheidssoort-in-id (variant); gelegenheidstype-ontbreekt |
| `cherubijnenhymne` | `kastorski` | Cherubijnenhymne (Kastorski) | — | groningen/groningen-vsa.vsa | gelegenheidstype-ontbreekt |

---

## Review-checklist (handmatig met Rene)

Per rij met flags:

1. **Klopt title** met inhoud bronbestand (Liturgikon-pagina / koormap-ref)?
2. **Ontbrekende gelegenheidstype** — welke waarde hoort hier (weekdagen-liturgie)?
3. **gelegenheidssoort-in-id** — kan id korter zodra metadata/zoek werkt?
4. **Zoek-proef** — welke `default.*` hoort in sjabloon/sessie?

**Totaal met flags:** 23 van 31 rijen.

### Belangrijkste bevindingen voor de review

1. **`zoek "1e antifoon zondag"` faalt** terwijl `resolve` wél `antifoon-1-zondag` vindt — oorzaak: bron-antifoon is **PDF**, zoek filtert op `.vsa`.
2. **`zoek "1e antifoon weekdagen"` is ambigu** (hemelum + liturgikon) zonder `default.uitvoeringsvorm`.
3. **Lokaal weekdagen-antifoon** mist `gelegenheidstype` in `variant.yaml` — gelegenheid zit alleen in title/alias.
4. **Id vs title:** `troparion-zondag-toon-N` (id) vs "Tropaar" (title) — aliassen dekken zoek op Troparion/Tropaar af.
5. **Antifoon weekdagen vs zondag** zijn **verschillende stukken** (`antifoon-1-weekdagen` lokaal vs `antifoon-1-zondag` bron) — samenvoegen tot `antifoon-1` vereist werkende disambiguatie.
6. **yaml ↔ VSA-frontmatter:** `check_zangstuk_yaml_vsa.py` faalt op kondak/troparion zondag — deels veldnaam `tone` vs `toon` in script, deels echte reference-mismatch (toon 3).

### Alle flags (compact)

**Bron — gelegenheidssoort-in-id (19):** alle `antifoon-*-zondag`, `kondak-zondag-toon-*`, `troparion-zondag-toon-*`.

**Lokaal — gelegenheidssoort-in-id + gelegenheidstype-ontbreekt (4 varianten):** `antifoon-{1,2,3}-weekdagen/liturgikon-weekdagen`, `cherubijnenhymne/kastorski`.

---

## Legenda flags

| Flag | Betekenis |
| ---- | --------- |
| `gelegenheidssoort-in-id` | id bevat `weekdagen` of `zondag` |
| `gelegenheidstype-ontbreekt` | geen `gelegenheidstype` in yaml/manifest |
| `yaml-id≠map` | id wijkt af van mapnaam |
| `title-type-mismatch` | id-prefix past niet bij title |
| `bronbestand-ontbreekt` | file-pad bestaat niet |

---

## Herhaalbaar maken

```cmd
cd /d C:\Git\orthodox-groningen\bron
python -m pip install -e ".[dev]"
python -m catalogus.cli index validate --bron-root . --content-root ..\VSA-demo\content-source
vsa validate zangstukken
python scripts\check_zangstuk_yaml_vsa.py
```

*(Gepland: `python -m catalogus.cli index report -o docs\plans\audit-zangstuk-catalogus.md` — nog toe te voegen als vast CLI-commando.)*
