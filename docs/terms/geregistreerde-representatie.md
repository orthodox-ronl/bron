---
term: geregistreerde-representatie
formPhrases:
  - geregistreerde representaties
  - geregistreerde representatie
  - geregistreerd
glossaryTerm: Geregistreerde representatie
glossaryText: "Een [representatie](@) waarvoor een [source-entry](@) bestaat in de [bron-repository](@) die haar koppelt via `file:`, `access:` of `status:`."
glossaryNotes:
  - "Het tegenovergestelde van een [parochie-lokale representatie](@)."
  - "Registratie vindt plaats via [promotie](@): een PR naar de [bron-repository](@) met [source-entry](@) en [bronbestand](@)."
---

# Geregistreerde representatie

Een [representatie](@) is **geregistreerd** als er een [source-entry](@) in de [bron-repository](@) bestaat die haar koppelt via `file:`, `access:` of `status:`.

| Status | Voorbeeld                                         |
| ------ | ------------------------------------------------- |
| Ja     | `groningen` met `file: sources/vsa/groningen.vsa` |
| Nee    | `lokaal/.../hemelum.vsa` vóór PR                  |
| Nee    | Inline VSA zonder entry                           |

Het tegenovergestelde is een [parochie-lokale representatie](@). De overgang van parochie-lokaal naar geregistreerd noemen we [promotie](@).

## Motivatie

Parochies kunnen lokaal materiaal ontwikkelen zonder het direct in de [bron-repository](@) te plaatsen. Door het onderscheid geregistreerd/niet-geregistreerd formeel te maken, weten parochies op welk materiaal ze kunnen bouwen: geregistreerde [representaties](@) zijn stabiel, vindbaar via de catalogus en beschikbaar voor alle parochies. [Parochie-lokale representaties](@) zijn dat niet.

Het onderscheid maakt ook duidelijk *wanneer* lokaal werk klaar is om te delen: op het moment van [promotie](@) wordt het geregistreerd en daarmee deel van de gemeenschappelijke basis.

Zie ook: [Terminologie, paragraaf 14](../specs/terminologie.md#14-geregistreerde-representatie).
