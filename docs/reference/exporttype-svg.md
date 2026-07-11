# Exporttype: embed SVG

Contract voor het **svg**-exporttype: [VSA-notatie](@) als schaalbare vectorafbeelding
in een samenstelling (HTML, afdruk).

---

## Samenvatting

Met exporttype **svg** toon je de muzieknotatie van een [vsa-bestand](@) als SVG in
de pagina. De lezer ziet dezelfde glyphs en omringende tekst als in VSA, geschikt
voor scherm en papier. De SVG wordt gegenereerd via conversie
([conversie-vsa-svg](conversie-vsa-svg.md)); export bepaalt alleen *hoe* die SVG
in de samenstelling wordt ingebed.

---

## Beoogde doelen

- Notatie **lezen** in browser (online uitgave)
- Notatie **afdrukken** op A4 (zelfde HTML, `@media print`)
- Visuele consistentie met VSA-rendering elders in het project
- **Niet:** bewerken in MuseScore (gebruik exporttype [mxl](exporttype-mxl.md))

---

## Authoring

### Doelsyntax (gepland)

```markdown
:::include svg "praktijk/zondagen/tropaar-zondag-toon-3.vsa" alt="Tropaar van de zondag, Toon 3" scale="85%":::
```

### Huidige equivalent (geïmplementeerd)

```markdown
:::include "praktijk/zondagen/tropaar-zondag-toon-3.vsa" alt="Tropaar van de zondag, Toon 3" scale="85%":::
```

Zonder exporttype `svg` wordt een `.vsa`-include omgezet naar een
`::: vsa-notatie`-blok; `build-markdown` rendert dat naar SVG. Gedrag is functioneel
gelijk aan exporttype svg zodra de kanaal-alias is geïmplementeerd.

### Pad naar bron

| Regel                           | Toelichting                                                   |
| ------------------------------- | ------------------------------------------------------------- |
| Relatief aan includerende `.md` | `praktijk/page.md` + `"melodie.vsa"` → `praktijk/melodie.vsa` |
| Spaties in pad                  | Alleen met quotes: `"mijn map/melodie.vsa"`                   |
| Absolute paden                  | Niet ondersteund                                              |
| Symlinks                        | Niet gedocumenteerd; vermijd                                  |

---

## Parameters

### `pad` (positie: eerste argument)

| Veld                   | Waarde                                                    |
| ---------------------- | --------------------------------------------------------- |
| **Verplicht?**         | Ja                                                        |
| **Type**               | Relatief pad naar `.vsa`                                  |
| **Doel**               | Welke bronnotatie wordt getoond                           |
| **Toegestane waarden** | Pad dat eindigt op `.vsa`, bestand bestaat                |
| **Verboden**           | Ontbrekend bestand, verkeerde extensie, pad buiten bereik |
| **Effect**             | Bepaalt welke VSA wordt gevalideerd en gerenderd          |
| **Voorbeeld geldig**   | `"tropaar-zondag-toon-3.vsa"`                             |
| **Voorbeeld ongeldig** | `"ontbreekt.vsa"` → `IncludeError: Bestand niet gevonden` |

### `alt`

| Veld                   | Waarde                                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------------------ |
| **Verplicht?**         | Nee (sterk aanbevolen voor toegankelijkheid)                                                           |
| **Type**               | String tussen dubbele quotes: `alt="…"`                                                                |
| **Standaard**          | Lege `alt` bij directe `.svg`-include; bij `.vsa`-include via shortcode: `"VSA notatie"`               |
| **Doel**               | Tekst voor screenreaders en wanneer afbeelding niet laadt                                              |
| **Toegestane waarden** | Willekeurige UTF-8-tekst; geen nested quotes zonder escape                                             |
| **Verboden**           | Geen apart attribuutformaat (`alt=Tropaar` zonder quotes wordt niet herkend)                           |
| **Effect**             | Bij `.vsa`: wordt `# alt: …` metadata in het VSA-blok; in HTML: `alt`-attribuut op `<img>` / shortcode |
| **Interactie**         | Onafhankelijk van `scale`                                                                              |
| **Voorbeeld**          | `alt="Kondak van de zondag, Toon 5"`                                                                   |

### `scale`

| Veld                   | Waarde                                                                           |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Verplicht?**         | Nee                                                                              |
| **Type**               | Percentage-string: `scale="85%"`                                                 |
| **Standaard**          | Geen schaling (100% van natuurlijke SVG-breedte)                                 |
| **Doel**               | Notatie smaller op pagina (meer regels op één scherm/A4)                         |
| **Toegestane waarden** | Positief getal + `%`, bijv. `"60%"`, `"85%"`, `"100%"`                           |
| **Verboden**           | Lege string; niet-numeriek percentage valt terug op ruwe CSS-waarde              |
| **Effect**             | Breedte = natuurlijke SVG-breedte × percentage; hoogte schaalt mee via `viewBox` |
| **Interactie**         | Combineert met `:::keep-together scale="…"` op blokniveau                        |
| **Voorbeeld**          | `scale="85%"` op tropaar/kondak in zondags-pagina’s                              |

!!! note "Typische waarden in demo"
    Zondags-pagina’s in VSA-tooling hugo-demo gebruiken vaak `scale="85%"` voor
    `.vsa` en `scale="100%"` voor JPG-scan van tropaarmelodie.

---

## Inputs

| Input                      | Vereist?    | Bron                                                                                    |
| -------------------------- | ----------- | --------------------------------------------------------------------------------------- |
| `.vsa`-bestand             | Ja          | content-source of gekopieerd uit `bron/zangstukken/`                                    |
| `.svg` afgeleide           | Impliciet   | Wordt bij build gegenereerd uit `.vsa` (nu inline)                                      |
| Vooraf gegenereerde `.svg` | Alternatief | `:::include "bestand.svg"` — kopieert SVG naar static, geen VSA-validatie op dat moment |

Sibling-conventie: `{stem}.svg` hoort bij `{stem}.vsa`; in CI doel expliciete
conversiestap vóór export (zie [CI-architectuur](../plans/ci-architectuur.md)).

---

## Validatie vóór export

| Check                      | Tool / moment                   | Blokkeert export?                    |
| -------------------------- | ------------------------------- | ------------------------------------ |
| `.vsa` parseerbaar         | `vsa validate` / build-markdown | Ja — build faalt                     |
| Semantische VSA-regels     | Zelfde                          | Ja                                   |
| Include-pad bestaat        | `resolve_includes`              | Ja — `IncludeError`                  |
| Geen kring-include         | include-stack                   | Ja — `IncludeError: Kringverwijzing` |
| `.svg` als directe include | Geen VSA-validate               | Nee — alleen bestand moet bestaan    |

Validatie dient **kwaliteit van bron** vóór publicatie, niet het exporttype zelf.

---

## Build-gedrag

**Volgorde in pipeline** (`build-markdown`):

1. Include-resolutie (`.vsa` → `::: vsa-notatie`)
2. Coria-directives (niet van toepassing op svg)
3. Blok-directives (`web-only`, `keep-together`, …)
4. VSA → SVG rendering

**Huidige stand:** conversie en export lopen deels in één stap (SVG ontstaat tijdens
build-markdown).

**Doel:** expliciete conversiestap (`vsa svg`) vóór samenstelling; export leest
dan `.svg` of valideert dat afgeleide aanwezig is.

**Output in HTML:** Hugo shortcode `{{< vsa … >}}` of `<img class="vsa-notation">`
met URL onder `/vsa/…` (configureerbaar via `svg_assets_url_prefix`).

---

## Output

| Uitgaveprofiel | Wat de eindgebruiker ziet                       |
| -------------- | ----------------------------------------------- |
| Online         | Schaalbare notatie in pagina                    |
| Afdruk         | Zelfde SVG; `@media print` verbergt site-chrome |
| Bewerking      | Meestal niet het primaire doel van svg          |

---

## Geschikt / niet geschikt

| Geschikt                                  | Niet geschikt                                            |
| ----------------------------------------- | -------------------------------------------------------- |
| Liturgische tekst + notatie op één pagina | Audio afspelen                                           |
| Afdrukbaar boek/deel                      | Bewerken in MuseScore                                    |
| Consistente VSA-weergave                  | Partij kiezen / oefenen (→ [coria](exporttype-coria.md)) |

---

## Fouten en oplossingen

| Melding (fragment)             | Oorzaak                                    | Oplossing                                           |
| ------------------------------ | ------------------------------------------ | --------------------------------------------------- |
| `Bestand niet gevonden`        | Pad typo of bestand niet in content-source | Pad controleren t.o.v. `.md`; bestand toevoegen     |
| `Kringverwijzing gedetecteerd` | A include B include A                      | Include-structuur herzien                           |
| `Onbekend bestandstype`        | Include van `.csv`, `.pdf`, …              | Alleen ondersteunde extensies                       |
| VSA-validatiefout              | Ongeldige `.vsa`-syntax                    | `vsa validate pad/melodie.vsa` lokaal               |
| Lege of gebroken SVG           | Zeldzaam renderfout                        | Issue [VSA-tooling](@); bron `.vsa` controleren     |

---

## Open punten (TBD)

- Implementatie `:::include svg` als expliciet exporttype (Spoor B)
- Alt-tekst automatisch uit `zangstuk.yaml` / VSA-frontmatter
- Expliciete conversiestap in CI vóór export
- Validatie dat `.svg` afgeleide niet verouderd is t.o.v. `.vsa`

---

## Gerelateerd

- [Conversie vsa svg](conversie-vsa-svg.md)
- [Exportcontracten — overzicht](exportcontracten.md)
