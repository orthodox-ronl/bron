---
term: parochie-lokale-representatie
formPhrases:
  - parochie-lokale representaties
  - parochie-lokale representatie
  - parochie-lokaal
glossaryTerm: Parochie-lokale representatie
glossaryText: "Een [bronbestand](@) of inline-notatie in een parochie-repo die nog niet [geregistreerd](@) is in de [bron-repository](@)."
glossaryNotes:
  - "Na [promotie](@) (PR naar [bron-repository](@)) wordt een parochie-lokale representatie een [geregistreerde representatie](@)."
  - "Parochie-lokale representaties staan onder `content-source/lokaal/<zangstuk-id>/<variant-id>/…`."
---

# Parochie-lokale representatie

Een [representatie](@) is **parochie-lokaal** als zij een [bronbestand](@) of inline-notatie in een parochie-repo is én nog niet [geregistreerd](@) is in de [bron-repository](@).

| Status | Voorbeeld                                             |
| ------ | ----------------------------------------------------- |
| Ja     | `content-source/lokaal/.../hemelum.vsa` vóór promotie |
| Ja     | Inline VSA in een [samenstelling](@)                  |
| Nee    | Na bron-sync: canonical uit bron-repo                 |

De overgang van parochie-lokaal naar geregistreerd noemen we [promotie](@).

## Motivatie

Parochies zingen niet altijd precies wat in de [bron-repository](@) staat: ze hebben eigen adaptaties, kleine variaties in de melodie, of materiaal dat nog niet gedeeld is. Die lokale praktijk verdient een plek in het systeem — ook als het nog niet rijp is voor de centrale repository.

Door parochie-lokale [representaties](@) expliciet te benoemen, kan tooling ermee omgaan (ze includen in [samenstellingen](@)) terwijl tegelijk duidelijk is dat dit materiaal niet gegarandeerd stabiel of vindbaar is voor andere parochies. Het begrip schept ook een heldere route naar delen: via [promotie](@).

Zie ook: [Terminologie, paragraaf 15](../specs/terminologie.md#15-parochie-lokale-representatie), [parochie-lokaal zangstukken](../manuals/parochie-lokaal-zangstukken.md).
