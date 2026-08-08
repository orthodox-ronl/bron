# Conversie: vsa musicxml

Contract voor het conversiemechanisme
[`vsa musicxml`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/musicxml/):
een [vsa-bestand](@) omzetten naar MusicXML (`.mxl` of `.musicxml`).

Dit document beschrijft **wat** de conversie doet en **wanneer** je die gebruikt.
Hoe je het commando aanroept: zie de
[CLI man-page `vsa musicxml`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/musicxml/)
en de workflow-guide
[MusicXML exporteren](https://orthodox-groningen.github.io/VSA-tooling/guides/musicxml-export/).

---

## Samenvatting

De conversie zet [VSA-notatie](@) om naar MusicXML voor MuseScore, Coria
(`play_from_url`) en de exporttypes [mxl-download](exporttype-mxl.md) en
[coria](exporttype-coria.md) (MXL-modus). De uitvoer is een [afgeleide](@) en
hoort **niet** in de [bron-repository](@).

Muziek-metadata in de frontmatter van het [vsa-bestand](@) (titel, toonsoort,
tempo) wordt aanbevolen zodat de MXL bruikbaar is in spelers en editors.

---

## Wanneer gebruiken

| Situatie                         | Wat je wilt                                                  |
| -------------------------------- | ------------------------------------------------------------ |
| Bewerken in MuseScore            | `.mxl` of `.musicxml` genereren                              |
| Oefenen in Coria zonder HTML     | MXL publiceren + Coria in MXL- of auto-modus                 |
| Download voor musici             | Bestand klaarzetten voor exporttype [mxl](exporttype-mxl.md) |

Gebruik **niet** deze conversie als enige weg naar leesbare notatie op papier —
daarvoor is [vsa svg](conversie-vsa-svg.md).

---

## Eisen aan de invoer

| Eis            | Toelichting                                                                                                          |
| -------------- | -------------------------------------------------------------------------------------------------------------------- |
| Bestand        | `.vsa`, UTF-8                                                                                                        |
| Validatie      | [`vsa validate`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/validate/) aanbevolen vóór conversie |
| Frontmatter    | Aanbevolen: titel, toon, tempo                                                                                       |
| Notatie-inhoud | Moet structuren bevatten die naar MusicXML te exporteren zijn                                                        |

---

## Uitvoerformaten (betekenis)

| Formaat     | Betekenis                                              | Typisch gebruik                |
| ----------- | ------------------------------------------------------ | ------------------------------ |
| `.mxl`      | Gecomprimeerd MusicXML (standaard voor distributie)    | Coria, download, archief       |
| `.musicxml` | Platte XML                                             | Debugging, sommige editors     |

### Exportprofielen (betekenis)

| Profiel     | Bedoeling                         | Wanneer                                      |
| ----------- | --------------------------------- | -------------------------------------------- |
| `playback`  | Afspelen en oefenen               | Coria, online (standaard in tooling)         |
| `engraving` | Notatie-layout / typografie       | Bewerken in MuseScore wanneer ondersteund    |

Welke vlag je daarvoor zet: zie de CLI man-page.

---

## Wat er uit komt

| Veld     | Waarde                                                                |
| -------- | --------------------------------------------------------------------- |
| Default  | `.mxl`                                                                |
| Locatie  | Door jou gekozen map of site-static                                   |
| Op site  | Typisch onder een URL-prefix zoals `/vsa/mxl/…` (tooling/site-config) |

---

## Validatie vóór conversie

| Check                                                                                      | Blokkeert?                                              |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| [`vsa validate`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/validate/) | Aanbevolen; ongeldige `.vsa` geeft slechte of geen MXL  |
| Ontbrekend inputbestand                                                                    | Ja                                                      |

Export-resolve controleert de MXL-inhoud **niet** opnieuw op build-time.

---

## Na de conversie (export)

| Exporttype                   | Gebruik                                           |
| ---------------------------- | ------------------------------------------------- |
| [mxl](exporttype-mxl.md)     | Downloadlink in de samenstelling                  |
| [coria](exporttype-coria.md) | `mode=mxl` of `auto` zonder `.coria.html`-sibling |

---

## Veelvoorkomende problemen (betekenis)

| Probleem                   | Typische oorzaak            | Richting oplossing                    |
| -------------------------- | --------------------------- | ------------------------------------- |
| Lege of minimale MXL       | Weinig muziek in `.vsa`     | Notatie uitbreiden                    |
| Verkeerde toon in speler   | Metadata ontbreekt          | Frontmatter / `zangstuk.yaml`         |
| Layout in MuseScore vreemd | playback-profiel            | engraving-profiel proberen (CLI)      |
| Coria laadt niet           | MXL niet op de server       | Genereren + static publiceren         |

---

## Open punten (TBD)

- Automatisch MXL kopiëren in alle parochie-builds
- Validatie well-formed XML in CI

---

## Gerelateerd

- [Exporttype mxl](exporttype-mxl.md)
- [Exporttype coria](exporttype-coria.md)
- [Conversiemechanismen — overzicht](conversiemechanismen.md)
- [CLI: `vsa musicxml`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/musicxml/)
- [Guide: MusicXML exporteren](https://orthodox-groningen.github.io/VSA-tooling/guides/musicxml-export/)
