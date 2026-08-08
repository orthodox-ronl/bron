---
term: zangstuk
formPhrases:
  - zangstuk
  - zangstukken
glossaryTerm: Zangstuk
glossaryText: "Een liturgisch-muzikaal geheel met een stabiele `zangstuk-id`, waaronder nul of meer [varianten](@) bestaan."
glossaryNotes:
  - "Beantwoordt de vraag: *welk stuk in de liturgie?* (bijv. Cherubijnenhymne, 1e antifoon weekdagen)."
  - "Een `.vsa`-bestand of een samenstelling is geen zangstuk — dat zijn [representatie](@) / [samenstelling](@)."
---

# Zangstuk

Een **zangstuk** is een liturgisch-muzikaal geheel met een stabiele
`zangstuk-id`, waaronder nul of meer [varianten](@) bestaan.

| Status    | Voorbeeld                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Ja        | `antifoon-1-weekdagen`, `cherubijnenhymne`, `troparion-zondag-toon-1`                                                           |
| Nee       | `groningen.vsa` ([bronbestand](@) / [representatie](@)); `zondag-toon-1.md` ([samenstelling](@)); SVG na build ([afgeleide](@)) |
| Randgeval | Werknamen vóór registratie → afstemmen bij [promotie](@); daarna canoniek `zangstuk-id`                                         |

## Motivatie

Zonder stabiel zangstuk-id kun je niet eenduidig zoeken, verwijzen of
samenstellen: dezelfde liturgische “slot” (bijv. Cherubijnenhymne) zou
anders uit elkaar vallen over losse bestanden. Het begrip maakt ruimte voor
meerdere [varianten](@) onder één liturgische identiteit.

## Gerelateerd

- [variant](@), [uitvoeringsvorm](@), [representatie](@) — lagere niveaus
- [source-entry](@), [bron-repository](@) — registratie
- [Terminologie, paragraaf 5](../specs/terminologie.md#5-zangstuk)
