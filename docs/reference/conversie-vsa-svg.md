---
doc_type: org-contract
audience: "P6 — Spec-/PR-reviewer; P4 — Consumer-site builder"
---
# Conversie: vsa svg

Contract voor het [conversiemechanisme](@)
[`vsa svg`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/svg/):
een [vsa-bestand](@) omzetten naar een schaalbare vectorafbeelding (`.svg`).

Dit document beschrijft **wat** de conversie doet en **wanneer** je die gebruikt.
Hoe je het commando precies aanroept (syntax, opties, voorbeelden): zie de
[CLI man-page `vsa svg`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/svg/)
en de workflow-guide
[SVG exporteren](https://orthodox-ronl.github.io/VSA-tooling/guides/svg-export/).

---

## Samenvatting

De conversie leest een [vsa-bestand](@) en schrijft een SVG met VSA-glyphs,
omringende tekst en layout volgens de rendering van [VSA-tooling](@). Die SVG is
een [afgeleide](@). Je gebruikt hem daarna via [exporttype](@)
[embed svg](exporttype-svg.md) of als static asset op een parochiesite.

---

## Wanneer gebruiken

| Situatie                         | Wat je wilt                                                                                                                 |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Notatie bekijken of afdrukken    | SVG als plaatje in de pagina of op papier                                                                                   |
| Site-build / CI                  | SVG’s klaarzetten vóór of tijdens publicatie                                                                                |
| Inline tijdens document-build    | Zelfde resultaat via [`vsa build-markdown`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/build-markdown/) |

Gebruik **niet** deze conversie als je wilt bewerken in MuseScore of oefenen in
Coria — daarvoor is [vsa musicxml](conversie-vsa-musicxml.md).

---

## Eisen aan de invoer

| Eis              | Toelichting                                                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Bestand          | `.vsa`, UTF-8 — een geldig [vsa-bestand](@)                                                                                         |
| Validatie        | Moet slagen met [`vsa validate`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/validate/) vóór een betrouwbare SVG |
| Frontmatter      | Optioneel; metadata kan de weergave beïnvloeden                                                                                     |
| Omringende tekst | Maakt deel uit van de body van het [vsa-bestand](@)                                                                                 |

---

## Wat er uit komt

| Veld         | Waarde                                                    |
| ------------ | --------------------------------------------------------- |
| Formaat      | SVG met `width` / `viewBox` zodat schalen mogelijk is     |
| Inhoud       | [VSA-notatie](@) + tekst; geen geluid                     |
| Bestandsnaam | Meestal `{stem}.svg` bij `{stem}.vsa`                     |
| Bewaarplaats | Afgeleide map of site-static — **niet** in `bron`         |

---

## Validatie vóór conversie

| Check              | Blokkeert betrouwbare SVG?                                                                            |
| ------------------ | ----------------------------------------------------------------------------------------------------- |
| Parse / semantiek  | Ja — eerst [`vsa validate`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/validate/) |
| Ontbrekend bestand | Ja                                                                                                    |

Bij document-build faalt de hele build als een `.vsa` ongeldig is.

---

## Na de conversie (export)

| Exporttype               | Gebruik                                |
| ------------------------ | -------------------------------------- |
| [svg](exporttype-svg.md) | Notatie inbedden in een samenstelling  |
| Directe `.svg`-include   | Kopie naar static zonder VSA-blok      |

---

## Veelvoorkomende problemen (betekenis)

| Probleem         | Typische oorzaak        | Richting oplossing                                      |
| ---------------- | ----------------------- | ------------------------------------------------------- |
| Validatiefout    | Syntax in `.vsa`        | Valideren; [vsa-notatie](@) raadplegen                  |
| Lege SVG         | Lege body               | Inhoud toevoegen                                        |
| Verkeerde glyphs | Font of toolversie      | [VSA-tooling](@) gelijk trekken met CI                  |
| Te breed op A4   | Brede layout            | `scale` bij export of regelbreedte in tooling           |

Concrete foutteksten en commandovoorbeelden: CLI man-pages
[`vsa svg`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/svg/) /
[`vsa validate`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/validate/).

---

## Open punten (TBD)

- Expliciete CI-job alleen voor conversie (los van Hugo)
- Cache: alleen opnieuw converteren bij gewijzigde `.vsa`

---

## Gerelateerd

- [Exporttype svg](exporttype-svg.md)
- [Conversiemechanismen — overzicht](conversiemechanismen.md)
- [CLI: `vsa svg`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/svg/)
- [Guide: SVG exporteren](https://orthodox-ronl.github.io/VSA-tooling/guides/svg-export/)
