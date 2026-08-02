# Exporttype: embed SVG

Contract voor het **svg**-exporttype: [VSA-notatie](@) als schaalbare
vectorafbeelding in een samenstelling (HTML, afdruk).

Technische build-stappen (shortcodes, asset-mappen): zie
[SVG exporteren](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/guides/svg-export.md)
en [CLI `vsa build-markdown`](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/reference/cli/build-markdown.md).

---

## Samenvatting

Met exporttype **svg** toon je de muzieknotatie van een [vsa-bestand](@) als SVG
in de pagina. De lezer ziet dezelfde glyphs en omringende tekst als in VSA,
geschikt voor scherm en papier. De SVG ontstaat via conversie
([conversie-vsa-svg](conversie-vsa-svg.md)); export bepaalt alleen *hoe* die SVG
in de samenstelling wordt ingebed.

---

## Beoogde doelen

- Notatie **lezen** in de browser (online uitgave)
- Notatie **afdrukken** op A4 (zelfde HTML, `@media print`)
- Visuele consistentie met VSA-weergave elders
- **Niet:** bewerken in MuseScore (→ [mxl](exporttype-mxl.md))
- **Niet:** audio oefenen (→ [coria](exporttype-coria.md))

---

## Authoring

### Doelsyntax

```markdown
:::include svg "praktijk/zondagen/tropaar-zondag-toon-3.vsa" alt="Tropaar van de zondag, Toon 3" scale="85%":::
```

### Equivalent zonder expliciet type (ook geldig)

```markdown
:::include "praktijk/zondagen/tropaar-zondag-toon-3.vsa" alt="Tropaar van de zondag, Toon 3" scale="85%":::
```

Zonder het woord `svg` wordt een `.vsa`-include als VSA-blok behandeld en bij
document-build naar SVG gerenderd. Functioneel komt dat overeen met exporttype
svg.

### Pad naar de bron

| Regel                           | Toelichting                                                   |
| ------------------------------- | ------------------------------------------------------------- |
| Relatief aan includerende `.md` | `praktijk/page.md` + `"melodie.vsa"` → `praktijk/melodie.vsa` |
| Spaties in pad                  | Alleen met quotes: `"mijn map/melodie.vsa"`                   |
| Absolute paden                  | Niet ondersteund                                              |
| Symlinks                        | Vermijd                                                       |

---

## Parameters

### `pad` (eerste argument)

| Veld                   | Waarde                                                    |
| ---------------------- | --------------------------------------------------------- |
| **Verplicht?**         | Ja                                                        |
| **Type**               | Relatief pad naar `.vsa`                                  |
| **Doel**               | Welke bronnotatie wordt getoond                           |
| **Toegestane waarden** | Pad dat eindigt op `.vsa`, bestand bestaat                |
| **Verboden**           | Ontbrekend bestand, verkeerde extensie, pad buiten bereik |
| **Effect**             | Bepaalt welke VSA wordt gevalideerd en gerenderd          |
| **Voorbeeld geldig**   | `"tropaar-zondag-toon-3.vsa"`                             |
| **Voorbeeld ongeldig** | `"ontbreekt.vsa"` → bestand-niet-gevonden-fout            |

### `alt`

| Veld                   | Waarde                                                                                   |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| **Verplicht?**         | Nee (sterk aanbevolen voor toegankelijkheid)                                             |
| **Type**               | String tussen dubbele quotes: `alt="…"`                                                  |
| **Standaard**          | Lege `alt` bij directe `.svg`-include; bij `.vsa` vaak `"VSA notatie"`                   |
| **Doel**               | Tekst voor screenreaders en wanneer de afbeelding niet laadt                             |
| **Toegestane waarden** | Willekeurige UTF-8-tekst; geen nested quotes zonder escape                               |
| **Verboden**           | `alt=Tropaar` zonder quotes (wordt niet herkend)                                         |
| **Effect**             | Wordt de alternatieve tekst bij de afbeelding in HTML                                    |
| **Interactie**         | Onafhankelijk van `scale`                                                                |
| **Voorbeeld**          | `alt="Kondak van de zondag, Toon 5"`                                                     |

### `scale`

| Veld                   | Waarde                                                                           |
| ---------------------- | -------------------------------------------------------------------------------- |
| **Verplicht?**         | Nee                                                                              |
| **Type**               | Percentage-string: `scale="85%"`                                                 |
| **Standaard**          | Geen schaling (100% van natuurlijke SVG-breedte)                                 |
| **Doel**               | Notatie smaller op de pagina (meer op één scherm/A4)                             |
| **Toegestane waarden** | Positief getal + `%`, bijv. `"60%"`, `"85%"`, `"100%"`                           |
| **Verboden**           | Lege string; niet-numeriek percentage valt terug op ruwe CSS-waarde              |
| **Effect**             | Breedte = natuurlijke SVG-breedte × percentage; hoogte schaalt mee via `viewBox` |
| **Interactie**         | Combineert met `:::keep-together scale="…"` op blokniveau                        |
| **Voorbeeld**          | `scale="85%"` op tropaar/kondak                                                  |

!!! note "Typische waarden"
    In demos wordt vaak `scale="85%"` voor `.vsa` gebruikt en `scale="100%"` voor
    een JPG-scan.

---

## Inputs

| Input                      | Vereist?    | Bron                                                         |
| -------------------------- | ----------- | ------------------------------------------------------------ |
| `.vsa`-bestand             | Ja          | content-source of gekopieerd uit `bron/zangstukken/`         |
| `.svg` afgeleide           | Impliciet   | Wordt bij build of via `vsa svg` gegenereerd                 |
| Vooraf gegenereerde `.svg` | Alternatief | `:::include "bestand.svg"` — geen VSA-validatie op dat moment |

Sibling-conventie: `{stem}.svg` hoort bij `{stem}.vsa`.

---

## Validatie (bedoeling)

| Check                  | Blokkeert publicatie? | Toelichting                          |
| ---------------------- | --------------------- | ------------------------------------ |
| `.vsa` parseerbaar     | Ja                    | Kwaliteit van de bron                |
| Semantische VSA-regels | Ja                    | Idem                                 |
| Include-pad bestaat    | Ja                    | Geen gebroken verwijzing             |
| Geen kring-include     | Ja                    | A → B → A is verboden                |
| Directe `.svg`-include | Alleen bestand bestaat | Geen VSA-validate op dat moment     |

---

## Wat de eindgebruiker ziet

| Uitgaveprofiel | Resultaat                                           |
| -------------- | --------------------------------------------------- |
| Online         | Schaalbare notatie in de pagina                     |
| Afdruk         | Zelfde SVG; site-chrome wordt bij print verborgen   |
| Bewerking      | Meestal niet het primaire doel van svg              |

---

## Geschikt / niet geschikt

| Geschikt                                  | Niet geschikt                                            |
| ----------------------------------------- | -------------------------------------------------------- |
| Liturgische tekst + notatie op één pagina | Audio afspelen                                           |
| Afdrukbaar boek/deel                      | Bewerken in MuseScore                                    |
| Consistente VSA-weergave                  | Partij kiezen / oefenen (→ [coria](exporttype-coria.md)) |

---

## Veelvoorkomende problemen (betekenis)

| Situatie                | Typische oorzaak              | Richting oplossing                    |
| ----------------------- | ----------------------------- | ------------------------------------- |
| Bestand niet gevonden   | Pad-typo of ontbrekend bestand | Pad t.o.v. `.md` controleren         |
| Kringverwijzing         | A include B include A         | Include-structuur herzien             |
| Onbekend bestandstype   | Verkeerde extensie            | Alleen ondersteunde types             |
| VSA-validatiefout       | Ongeldige syntax              | `vsa validate` (zie CLI)              |
| Lege of gebroken SVG    | Renderfout                    | Bron `.vsa` en [VSA-tooling](@) check |

---

## Open punten (TBD)

- Alt-tekst automatisch uit `zangstuk.yaml` / VSA-frontmatter
- Expliciete conversiestap in CI vóór export
- Validatie dat `.svg` niet verouderd is t.o.v. `.vsa`

---

## Gerelateerd

- [Conversie vsa svg](conversie-vsa-svg.md)
- [Exportcontracten — overzicht](exportcontracten.md)
- [Guide: SVG exporteren](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/guides/svg-export.md)
