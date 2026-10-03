---
term: toonhoogte-overgang
termType: concept
glossaryTerm: Toonhoogte-overgang
glossaryAlias: Pitch-transition
glossaryText: "Een stil bracket-token in [vsa-notatie](@) van de vorm `[<oude-EHM>:<nieuwe-EHM>]` dat een bewuste sprong in relatieve toonhoogte aangeeft zonder iets op het blad te tonen."
glossaryNotes:
  - "Normatieve syntax, semantiek en rendering staan in VSA-tooling (tool-specifiek), niet in dit Zangstukmodel."
  - "Onderscheid met een hoogte-markering `[<EHM>:]`: die eindigt op `:]` en is zichtbaar op het blad; een toonhoogte-overgang heeft niet-lege inhoud na de middelste `:` vóór `]`."
  - "Voorbeeld: `[//:/]` springt van relatieve hoogte `//` naar `/` tussen opeenvolgende stukken in één bron."
formPhrases:
  - toonhoogte-overgang
  - toonhoogte-overgangen
  - pitch-transition
  - pitch-transitions
  - pitch transition
  - pitch transitions
---

# Toonhoogte-overgang

Een **toonhoogte-overgang** is een stil token in [vsa-notatie](@) waarmee je een
bewuste sprong in relatieve toonhoogte tussen opeenvolgende stukken in één
bron aangeeft, zonder de gezongen tekst te verdraaien en zonder iets op het
blad te tonen.

Vorm: `[<oude-EHM>:<nieuwe-EHM>]` — bijvoorbeeld `[//:/]` (van `//` naar `/`).

| Status | Voorbeeld                                       |
| ------ | ----------------------------------------------- |
| Wel    | `[//:/]`, `[/://]`, `[:/]`                      |
| Niet   | `[/:]` of `[//:]` (hoogte-markering, zichtbaar) |
| Niet   | Kunstmatige dalende EHM op het eerste woord     |

## Motivatie

Zonder dit begrip moeten opeenvolgende stukken met verschillende relatieve
starthoogte óf een validatiefout geven, óf de melodie verdraaien met
kunstmatige modifiers. De toonhoogte-overgang maakt de sprong expliciet voor
validatie en export, terwijl zangers op het blad alleen de gewone
hoogte-markeringen blijven zien.

## Gerelateerd / verder lezen

- [vsa-notatie](@), [vsa-tooling](@), [vsa-bestand](@)
- Normatieve tool-spec (syntax, semantiek, rendering):
  [VSA-tooling — toonhoogte-overgang](https://github.com/orthodox-ronl/VSA-tooling/blob/development/docs/terminologie/toonhoogte-overgang.md)
  en [syntax](https://github.com/orthodox-ronl/VSA-tooling/blob/development/docs/specification/syntax.md)
- Documentatie-eigendom: VSA-syntax is tool-specifiek
  ([documentatie-eigendom](../specs/documentatie-eigendom.md))
