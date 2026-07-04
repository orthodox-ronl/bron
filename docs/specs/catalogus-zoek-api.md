# Catalogus — zoek-API (contract)

Status: **normatief contract** (fase 0); implementatie **`catalogus.zoek`** volgt in fase 4.

Gerelateerd: [catalogus-samenstelling-zangstuk.md](catalogus-samenstelling-zangstuk.md),
[catalogus-architectuur.md](catalogus-architectuur.md), [terminologie §2.8](terminologie.md),
[zangstuk-formaat.md](zangstuk-formaat.md), [exportcontracten](../reference/exportcontracten.md).

Consumenten:

- markdown `:::include … zoek="…"` → **`vsa resolve-catalogus`** (VSA-tooling);
- `.vsa` **`@include-vsa zoek="…"`** → in-memory expand (VSA-tooling).

Beide roepen **dezelfde** Python-API aan; geen dubbele zoeklogica in VSA-tooling.

---

## Doel

Gegeven een **vrije zoekstring**, optionele **liturgische context** (`default.*`) en optioneel
**bestandsextensie-filter** levert de catalogus **exact één** brondocument, uitgedrukt als:

1. **`Path`** — absoluut pad naar het brondocument op schijf;
2. **`catalogus_pad`** — logische referentie `lokaal:…` of `bron:…` (niet `id:`);
3. **`VsaFileEntry`** — canonieke ids + herkomst (ook bij niet-`.vsa`-bestanden).

**Geen** relatieve paden in het contract. Lokale registratie loopt via manifesten onder
`content-root/lokaal/`.

Default **`bestandsextensie`**: `{".vsa"}` — verplicht voor `@include-vsa` en exporttypes
`svg` / `coria` / `mxl`. Andere extensies (bijv. `.pdf`) alleen op expliciet verzoek.

---

## Parochie-context (normatief)

`catalogus` draait in de praktijk **in de context van een parochie-repo** (Hugo
**content-source**, demo: `examples/hugo-demo/content-source`).

| Root | Betekenis |
| ---- | --------- |
| **`--content-root`** | Parochie content-source; indexeert **`lokaal/`** (parochie-register) |
| **`--bron-root`** | Org-bron-repo (`zangstukken/`); optioneel maar gebruikelijk |

**Zoekscope:** standaard doorzoekt de catalogus **beide** (`context.bronnen` default
`bron` + `lokaal`). De implementatie bouwt één index uit beide roots.

**Voorrang:** bij dezelfde query en context geldt **lokaal vóór bron**:

1. Kandidaten in **`lokaal/`** bepalen de uitkomst (strict: 0 / 1 / >1).
2. Alleen als **geen** lokaal-kandidaat overblijft, valt de keuze terug op **bron**.
3. Meerdere lokaal-kandidaten → **`AmbiguousError`** — **niet** stil overschakelen naar bron.

**Cross-origin hint:** wanneer de gekozen match **`origin=lokaal`** is en dezelfde query
(+ context + extensie) **ook** minstens één match in **bron** opleverde, vult
**`ZoekResult.ook_gevonden_in_bron`** de bijbehorende **`catalogus_pad`**-waarden.
Doel: auteur alert maken om te verifiëren dat de parochie-lokale versie de bedoelde is.
Geen wijziging van de gekozen match.

Consumenten tonen de hint als **waarschuwing** (stderr, validate-warning, `--verbose`),
niet als fout.

---

## Zoekgedrag (abstract)

De API specificeert **niet** welke yaml-velden geïndexeerd worden. Implementatie doorzoekt
alle teksten en velden die de catalogus uit manifesten, mapnamen, ids, aliassen en
liturgische metadata kent.

1. Normaliseer `query` ([§2.8](terminologie.md)).
2. Verzamel kandidaten waar genormaliseerde query matcht op doorzoekbare tekst (titels,
   aliassen, id-slugs, optionele metadata — ranking in implementatie-PR).
3. Pas **`ZoekContext`**-filters toe (`gelegenheid`, `toon`, `uitvoeringsvorm`, …).
4. Pas **`bestandsextensie`** toe op `entry.path.suffix`.
5. Uitkomst (strict modus **`zoek`**, na parochie-voorrang):
   - **Geen** kandidaat → `NotFoundError` (`niveau="zoek"`).
   - **Meerdere** kandidaten binnen de winnende herkomst → `AmbiguousError`.
   - **Precies één** → `ZoekResult` (+ eventueel **`ook_gevonden_in_bron`**).

Bij conflict tussen context en metadata: **context filtert**; geen stille fallback.

**Liturgische rol** (`zoek="Troparion"`) is geen apart API-veld — het is schrijfconventie
voor de zoekstring; zie [catalogus-samenstelling-zangstuk.md](catalogus-samenstelling-zangstuk.md).

---

## Twee contextlagen (geen conflict)

Zoeken gebruikt **twee** soorten context; die zijn **complementair**, geen dubbeling:

| Laag | Waar | Rol |
| ---- | ---- | --- |
| **`ZoekContext`** | `default.*` in **markdown-sessie** of **`default:`** in **ouder-`.vsa`** | *Deze* zoekactie / *deze* samenstelling: welk feest, welke default-uitvoeringsvorm, … |
| **Catalog-metadata** | `zangstuk.yaml`, `variant.yaml`, `uitvoeringsvorm.yaml`, titels, aliassen | Geïndexeerd materiaal; **`ZoekContext` filtert** welke kandidaten passen |

**Markdown-samenstelling:** Rene zet `default.gelegenheid` in de **sessie-**frontmatter;
`zoek="Troparion"` blijft een liturgische rol — zie
[catalogus-samenstelling-zangstuk.md](catalogus-samenstelling-zangstuk.md).

**Standalone / samengesteld `.vsa`:** dezelfde `ZoekContext`-sleutels onder **`default:`**
in de **ouder-**.vsa-frontmatter (conventie: [zangstuk-formaat.md](zangstuk-formaat.md)).
Geen verplichting om `gelegenheid` in het **included** stuk zelf te herhalen.

**`zangstuk.yaml`-metadata** (`gelegenheid`, `toon`, …) beschrijft het stuk in de catalogus;
**`ZoekContext`** beschrijft waarvoor *nu* gezocht wordt. Beide horen te bestaan.

---

## Python-API

Module: `catalogus.zoek` (pakket **catalogus** in bron-repo).

### `ZoekContext`

Liturgische context; spiegelt `default.*` uit markdown- of `.vsa`-frontmatter.

| Veld               | Type              | Betekenis                                              |
| ------------------ | ----------------- | ------------------------------------------------------ |
| `gelegenheid`      | `str \| None`     | Canoniek gelegenheid-id (sessie)                       |
| `gelegenheidstype` | `str \| None`     | `vast-feest` \| `zondag-cyclus`                        |
| `toon`             | `str \| None`     | Zondagstoonsysteem (canoniek of invoer)                |
| `uitvoeringsvorm`  | `str \| None`     | Default uitvoeringsvorm (alias toegestaan op invoer)   |
| `gelegenheidsdatum`| `str \| None`     | `"MM-DD"`                                              |
| `referentie`       | `str \| None`     | Herkomst-filter ([§9](terminologie.md)); geen pad      |
| `bronnen`          | `frozenset[str]`  | `"bron"`, `"lokaal"` — default beide                   |

Factory:

```python
ZoekContext.from_default_mapping(
    default: dict | None,
    *,
    bronnen: Iterable[str] | str | None = None,
) -> ZoekContext
```

Leest sleutels onder `default` (yaml-frontmatter) en normaliseert `bronnen` uit optionele
sibling `bronnen:` (`bron` \| `lokaal` \| lijst).

### `ZoekMatch`

Één kandidaat na query-, context- en bestandsextensie-filter.

| Veld            | Type           | Betekenis                          |
| --------------- | -------------- | ---------------------------------- |
| `entry`         | `VsaFileEntry` | Canonieke ids + pad + `origin`     |
| `catalogus_pad` | `str`          | `lokaal:…` / `bron:…`              |

### `ZoekLijstResult`

Resultaat van **`zoek_kandidaten`** — alle matches, desgevraagd.

| Veld               | Type              | Betekenis                    |
| ------------------ | ----------------- | ---------------------------- |
| `query`            | `str`             | Originele zoekstring         |
| `query_normalized` | `str`             | Na `normalize_for_match`     |
| `matches`          | `list[ZoekMatch]` | 0..n kandidaten (gesorteerd) |

Property **`catalogus_paden`**: `[m.catalogus_pad for m in matches]`.

### `ZoekResult`

Resultaat van **`zoek`** (strict: precies één match).

| Veld               | Type           | Betekenis                    |
| ------------------ | -------------- | ---------------------------- |
| `query`            | `str`          | Originele zoekstring         |
| `query_normalized` | `str`          | Na `normalize_for_match`     |
| `entry`            | `VsaFileEntry` | Gekozen brondocument         |
| `catalogus_pad`    | `str`          | `lokaal:…` / `bron:…`        |
| `ook_gevonden_in_bron` | `tuple[str, …]` | `catalogus_pad` in bron bij lokaal-winst; anders leeg |

Property **`path`**: `entry.path`.

Property **`has_ook_in_bron`**: `bool` — `len(ook_gevonden_in_bron) > 0`.

**`catalogus_pad`** gebruikt prefix **`lokaal:`** of **`bron:`** volgens `entry.origin`
(lokaal wint bij dubbele registratie). Prefix **`id:`** is **geen** uitkomst van zoek.

Helper (fase 0):

```python
format_catalogus_pad(entry: VsaFileEntry) -> str
```

### `zoek_kandidaten`

```python
def zoek_kandidaten(
    query: str,
    *,
    index: AliasIndex,
    context: ZoekContext | None = None,
    bestandsextensie: frozenset[str] | None = frozenset({".vsa"}),
) -> ZoekLijstResult:
    ...
```

**Kern-API.** Retourneert **alle** matches (0, 1 of meer). Geen exception bij
ambiguïteit — bedoeld voor review-UI, CLI `--lijst`, en als basis voor `zoek()`.

- `bestandsextensie=None` → geen filter op suffix.
- Default `{".vsa"}` → alleen `.vsa`-bestanden.

Convenience:

```python
def zoek_kandidaten_met_roots(
    query: str,
    *,
    content_root: Path | None = None,
    bron_root: Path | None = None,
    fixture_root: Path | None = None,
    context: ZoekContext | None = None,
    bestandsextensie: frozenset[str] | None = frozenset({".vsa"}),
) -> ZoekLijstResult:
    ...
```

### `zoek`

```python
def zoek(
    query: str,
    *,
    index: AliasIndex,
    context: ZoekContext | None = None,
    bestandsextensie: frozenset[str] | None = frozenset({".vsa"}),
) -> ZoekResult:
    ...
```

Strict wrapper om **`zoek_kandidaten`**:

| `len(matches)` | Gedrag |
| -------------- | ------ |
| 0              | `NotFoundError` — scope vermeldt query en filter (bijv. geen `.vsa`) |
| 1              | `ZoekResult` |
| >1 (zelfde herkomst) | `AmbiguousError` — `candidates` uit die herkomst |

Bij **lokaal-winst** met bron-matches: vul **`ook_gevonden_in_bron`**; geen exception.

Convenience:

```python
def zoek_met_roots(
    query: str,
    *,
    content_root: Path | None = None,
    bron_root: Path | None = None,
    fixture_root: Path | None = None,
    context: ZoekContext | None = None,
    bestandsextensie: frozenset[str] | None = frozenset({".vsa"}),
) -> ZoekResult:
    ...
```

**Precondities**

- `query` niet leeg na `strip()`.
- Minstens één index-root bij `*_met_roots`.
- Consumenten met herhaalde zoekacties: bouw **`AliasIndex` eenmaal**, roep `zoek` /
  `zoek_kandidaten` met `index=` aan (niet per call `*_met_roots`).

**Status fase 0:** `zoek_kandidaten()` werpt `NotImplementedError`. `zoek()` delegeert
daarnaartoe. `format_catalogus_pad`, `ZoekContext`, `ZoekMatch`, `ZoekLijstResult` zijn
geïmplementeerd.

---

## Consumentenmatrix

| Consument              | Context uit              | `bestandsextensie` | Gebruikt              |
| ---------------------- | ------------------------ | ------------------ | --------------------- |
| `@include-vsa zoek=`   | ouder-`.vsa` `default`   | `.vsa` (default)   | `result.path`         |
| `vsa resolve-catalogus`| markdown `default`       | `.vsa` (default)   | `result.catalogus_pad`|
| `catalogus zoek` CLI   | flags                    | `.vsa` (default)   | stdout `catalogus_pad`|
| Review / debug         | idem                     | expliciet          | `zoek_kandidaten`     |

`result.path` is **leidend**; geen verplichte `resolve_vsa_path`-verificatie daarna.

---

## CLI — `catalogus zoek`

```cmd
cd /d C:\Git\orthodox-groningen\bron
python -m catalogus.cli zoek "Troparion" ^
  --content-root ..\VSA-tooling\examples\hugo-demo\content-source ^
  --bron-root . ^
  --default-gelegenheid geboorte-moeder-gods ^
  --default-uitvoeringsvorm Groningen
```

| Flag                         | Mapt naar                          |
| ---------------------------- | ---------------------------------- |
| `query` (positioneel)        | `zoek(query, …)`                   |
| `--lijst`                    | `zoek_kandidaten` i.p.v. `zoek`    |
| `--bestandsextensie`         | suffix-filter (default `vsa`)      |
| `--default-gelegenheid`      | `context.gelegenheid`              |
| `--default-gelegenheidstype` | `context.gelegenheidstype`         |
| `--default-toon`             | `context.toon`                     |
| `--default-uitvoeringsvorm`  | `context.uitvoeringsvorm`          |
| `--default-gelegenheidsdatum`| `context.gelegenheidsdatum`        |
| `--default-referentie`       | `context.referentie`               |
| `--bronnen`                  | `context.bronnen`                  |
| `--content-root`, …          | index-roots                        |

**Uitvoer (na implementatie):**

- zonder `--lijst`: één regel **`catalogus_pad`**.
- **`--verbose`**: pad + ids op stderr; bij **`ook_gevonden_in_bron`**: waarschuwing
  *«Ook gevonden in bron: …»* (één regel per pad of komma-gescheiden).
- met `--lijst`: één **`catalogus_pad`** per regel (0 regels = exit 1); optioneel
  `--verbose` groepeert per herkomst (`lokaal:` / `bron:`).

---

## Ambiguïteit en auteur-workflow

**Strict `zoek`** (build, validate, expand) faalt bij **meerdere** kandidaten binnen de
winnende herkomst — geen stille keuze.

| Situatie | Aanbevolen actie auteur |
| -------- | ------------------------ |
| `AmbiguousError` | `catalogus zoek --lijst`; verfijn `zoek=` of `default.*`; of `@include-vsa id=` / `lokaal=` |
| `has_ook_in_bron` | Controleren of parochie-lokaal stuk bedoeld is; anders `@include-vsa lokaal=…` / `id=…` expliciet |
| Geen match | Manifest/index; `default.gelegenheid`; disambiguation in zoekstring |

VSA-tooling (`@include-vsa`, `vsa validate`): **`AmbiguousError`** → **fout**;
**`ook_gevonden_in_bron`** → **waarschuwing** (build mag doorgaan). Zie
[VSA — include-vsa](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/spec/include-vsa.md).

---

## Consumentencontract (VSA-tooling)

### Markdown — `:::include zoek="…"`

1. Lees `default` (+ `bronnen`) uit markdown-frontmatter → `ZoekContext`.
2. `result = zoek_met_roots(…, bestandsextensie=frozenset({".vsa"}))`.
3. Resolve-stap vervangt `zoek="…"` door `catalogus_pad`.

### VSA — `@include-vsa zoek="…"`

1. Lees `default` uit **ouder**-`.vsa`-frontmatter → `ZoekContext`.
2. `result = zoek_met_roots(…, bestandsextensie=frozenset({".vsa"}))`.
3. Expand leest `result.path`, strip frontmatter doel, splice body in-memory.

**Gedeelde stap:** `zoek` / `zoek_kandidaten`; geen aparte zoekimplementatie in VSA-tooling.

---

## Foutmodel

| Situatie                         | Exception              | `niveau` |
| -------------------------------- | ---------------------- | -------- |
| Geen match                       | `NotFoundError`        | `"zoek"` |
| Meerdere matches (`zoek` strict) | `AmbiguousError`       | `"zoek"` |
| Lege query                       | `ValueError`           | —        |
| Nog niet geïmplementeerd         | `NotImplementedError`  | —        |

`AmbiguousError.candidates`: lijst **`MatchCandidate`** — minimaal **`catalogus_pad`**
(canonical_id = pad of zangstuk-id; implementatie-PR).

---

## Implementatiestatus

| Onderdeel                                              | Status        |
| ------------------------------------------------------ | ------------- |
| Contract + datatypes + `format_catalogus_pad`          | **Fase 0**    |
| `zoek_kandidaten()` / `zoek()` body                    | **Gepland**   |
| `catalogus zoek` CLI (functioneel)                     | **Gepland**   |
| VSA `@include-vsa zoek=`                               | **Gepland**   |
| `vsa resolve-catalogus`                                | **Gepland**   |

---

## Wijzigingshistorie

| Datum   | Wijziging |
| ------- | --------- |
| 2026-07 | Fase 0: normatief API-contract; stub `zoek()`; `@include-vsa` als consument |
| 2026-07 | Abstract zoekgedrag; `bestandsextensie`; `zoek_kandidaten` / `--lijst`; NL metadata |
| 2026-07 | Parochie-context; lokaal vóór bron; `ook_gevonden_in_bron`; twee contextlagen; ambiguïteit |
