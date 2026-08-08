---
term: source-entry
formPhrases:
  - source-entries
  - source-entry
glossaryTerm: Source-entry
glossaryText: "Een element in de `sources:`-lijst van `zangstuk.yaml` in de [bron-repository](@), met een uniek `id` binnen dat [zangstuk](@); registreert een [representatie](@) of placeholder op het huidige platte model."
glossaryNotes:
  - "Het `id`-veld van een source-entry correspondeert met het `representatie-id`."
  - "Meerdere source-entries kunnen meerdere [representaties](@) registreren, of (legacy) nog niet onderscheiden [variant](@)/[uitvoeringsvorm](@)-structuur bevatten — bij nieuw werk gebruik het vier-niveaumodel."
---

# Source-entry

Een **source-entry** is een element in de `sources:`-lijst van `zangstuk.yaml` in de [bron-repository](@). Elke entry heeft een uniek `id` binnen dat [zangstuk](@) en registreert een [representatie](@) (of een placeholder daarvoor) op het huidige platte model.

```yaml
# voorbeelden van source-entries
sources:
  - id: groningen
    file: sources/vsa/groningen.vsa
    based_on: liturgikon
  - id: liturgikon
    status: nog-niet-getranscribeerd
```

Het `id`-veld van een source-entry correspondeert met het `representatie-id`. Bij nieuw werk is het vier-niveaumodel leidend; [source-entries](@) kunnen legacy-structuur bevatten die niet altijd [variant](@) en [uitvoeringsvorm](@) onderscheidt.

| Status | Voorbeeld                                                                   |
| ------ | --------------------------------------------------------------------------- |
| Ja     | `{ id: groningen, file: sources/vsa/groningen.vsa, based_on: liturgikon }`  |
| Ja     | `{ id: liturgikon, status: nog-niet-getranscribeerd }`                      |
| Nee    | Alleen een `.vsa` op schijf zonder yaml-entry                               |

## Motivatie

De [bron-repository](@) gebruikt een plat model (`sources:` in `zangstuk.yaml`) als brug naar het vier-niveaumodel. Een source-entry is de schakel: hij registreert een [representatie](@) (of placeholder) en maakt het mogelijk voor tooling en CI om te weten welke [bronbestanden](@) bij een [zangstuk](@) horen, wat hun status is, en of ze toegankelijk zijn.

Zonder source-entries zou een `.vsa`-bestand in de repository onzichtbaar zijn voor de catalogus: er is geen registratie, geen vindbare koppeling aan een [zangstuk](@), [variant](@) of [uitvoeringsvorm](@).

Zie ook: [Terminologie, paragraaf 13](../specs/terminologie.md#13-source-entry).
