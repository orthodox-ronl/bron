---
term: samenstelling
formPhrases:
  - samenstellingen
  - samenstelling
glossaryTerm: Samenstelling
glossaryText: "Een markdown-document (met VSA-directives) dat [representaties](@) ordent voor een lezersdoel, zonder zelf [representatie](@) te zijn."
glossaryNotes:
  - "Voorbeelden: `zondag-toon-1.md`, `antifonen-hemelum.md`."
  - "Een samenstelling is het ingevulde (opgeloste) resultaat van een sjabloon."
  - "Niet verwarren met [compositie](@) (org-brede ordered list van [zangstukken](@) in yaml) of sjabloon (markdown met `:::include zoek=`)."
---

# Samenstelling

Een **samenstelling** is een markdown-document met VSA-directives (`:::include`) dat [representaties](@) ordent voor een lezersdoel (bijv. een koormap of dienst-overzicht), zonder zelf een [representatie](@) te zijn.

Een samenstelling is het ingevulde resultaat van een **sjabloon** — nadat `:::include zoek="…"`-directives zijn opgelost naar een catalogus-pad.

| Status | Voorbeeld                                   |
| ------ | ------------------------------------------- |
| Ja     | `zondag-toon-1.md`, `antifonen-hemelum.md`  |
| Nee    | `groningen.vsa` ([representatie](@) / [bronbestand](@)) |
| Nee    | `zangstuk.yaml` ([source-entry](@)-model)   |

Niet verwarren met [compositie](@) (org-brede YAML-lijst van [zangstukken](@)) of sjabloon (markdown met `default.gelegenheidstype` en `:::include zoek=`).

## Motivatie

Koren en parochies hebben praktische documenten nodig: een koormap voor de zondagse liturgie, een verzameling voor een specifieke feestdag. Die documenten zijn geen muzikale bronnen — ze ordenen bestaande [representaties](@) voor een specifiek lezersdoel.

Door samenstelling als aparte term te definiëren, is duidelijk dat een samenstelling zelf geen nieuwe muzikale informatie bevat en niet als [bronbestand](@) of [representatie](@) telt. De relatie tot sjabloon maakt ook het onderscheid tussen het *patroon* (herbruikbaar) en het *ingevulde document* (concreet) expliciet.

Zie ook: [Terminologie, paragraaf 18](../specs/terminologie.md#18-samenstelling), [catalogus-samenstelling-zangstuk.md](../specs/catalogus-samenstelling-zangstuk.md).
