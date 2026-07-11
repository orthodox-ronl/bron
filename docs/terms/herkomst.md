---
term: herkomst
formPhrases:
  - herkomst
glossaryTerm: Herkomst
glossaryText: "Metadata die beschrijft *waar* een [zangstuk](@), [variant](@), [uitvoeringsvorm](@) of [representatie](@) vandaan komt — mens, traditie, publicatie of parochie — maar niet zijnde een [bronbestand](@) of de [bron-repository](@) zelf."
glossaryNotes:
  - "Herkomst mag onbekend zijn: de entiteit bestaat desondanks."
  - "Herkomst is geen bestand; het is metadata (zoals `reference:` in `zangstuk.yaml`)."
---

# Herkomst

**Herkomst** beschrijft *waar* een entiteit vandaan komt: de mens, traditie, publicatie of parochie die aan de basis staat van een [zangstuk](@), [variant](@), [uitvoeringsvorm](@) of [representatie](@).

Herkomst is uitsluitend metadata — geen [bronbestand](@) en geen verwijzing naar de [bron-repository](@).

| Niveau          | Voorbeeld                                           |
| --------------- | --------------------------------------------------- |
| Zangstuk        | `reference: "Liturgikon, weekdagen"`                |
| Variant         | `"Obikhod-traditie"`; `"A. Kastorski, koormap 15c"` |
| Uitvoeringsvorm | `"Parochie Groningen, refreinpraktijk"`             |
| Representatie   | transcribent, `based_on` scan                       |

Herkomst mag **onbekend** zijn; de entiteit bestaat desondanks.

## Motivatie

Muzikaal erfgoed heeft geen bestaansrecht los van zijn oorsprong. Weten wie een [variant](@) componeerde, uit welke traditie een [uitvoeringsvorm](@) stamt, of via welke publicatie materiaal is overgeleverd, is onmisbaar voor verantwoording (attribution), historische context en het beoordelen van authenticiteit.

Herkomst is bewust los gehouden van [bronbestand](@) en [bron-repository](@): het gaat niet om *waar iets staat opgeslagen*, maar om *waar het inhoudelijk vandaan komt*. Die scheiding voorkomt verwarring tussen logistieke en inhoudelijke afkomst.

Zie ook: [Terminologie, paragraaf 9](../specs/terminologie.md#9-herkomst).
