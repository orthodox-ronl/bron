---
term: alias
formPhrases:
  - alias
  - aliassen
glossaryTerm: Alias
glossaryText: "Een voor mensen leesbare naam of werknaam voor een entiteit ([zangstuk](@), [variant](@), [uitvoeringsvorm](@) of [representatie](@)), die op de invoergrens mag worden gebruikt en door een resolver wordt omgezet naar het [canonieke id](@) in opslag."
glossaryNotes:
  - "Aliassen mogen spaties, hoofdletters, diacritica en andere talen bevatten; het [canonieke id](@) blijft `^[a-z0-9_-]+$`."
  - "Binnen één scope mag een alias niet op twee verschillende entiteiten wijzen; bij meerdere matches is er een ambiguïteitsfout."
  - "Niet verwarren met het [canonieke id](@) zelf, noch met [herkomst](@) (waar iets vandaan komt)."
---

# Alias

Een **alias** is een voor mensen leesbare naam of werknaam voor een entiteit in het
vier-niveaumodel — [zangstuk](@), [variant](@), [uitvoeringsvorm](@) of
[representatie](@). Op de **invoergrens** (zoeken, UI, CLI, soms yaml-invoer) mag
een alias gebruikt worden; vóór opslag, paden of `bron:…`-referenties zet een
**resolver** die om naar het **[canonieke id](@)** (`^[a-z0-9_-]+$`).

| Status | Voorbeeld                                                                                  |
| ------ | ------------------------------------------------------------------------------------------ |
| Ja     | `"Groningen"` → `uitvoeringsvorm-id` `groningen`                                           |
| Ja     | `"1e antifoon weekdagen"` → `zangstuk-id` `antifoon-1-weekdagen`                           |
| Ja     | `"Касторский"` / `"koormap 15c"` → `variant-id` `kastorski`                                |
| Nee    | Het [canonieke id](@) zelf in opslag (`groningen` in pad of yaml) — dat is geen alias-laag |
| Nee    | Twee verschillende entiteiten in dezelfde scope met dezelfde alias-tekst                   |

## Motivatie

Zangers en beheerders denken in herkenbare namen (“Hemelum”, “eerste antifoon”),
niet in machine-ids. Zonder [aliassen](@) zou iedereen overal lowercase ids moeten
typen — foutgevoelig en onvriendelijk. Met [aliassen](@) blijft de **technische laag**
stabiel ([canonieke ids](@) in git en builds) terwijl de **menselijke laag** natuurlijk
Nederlands, Engels of Cyrillisch mag gebruiken.

De scheiding opslag ↔ invoer (en de eis van eenduidigheid binnen scope) voorkomt
dat “Groningen” stilzwijgend naar de verkeerde [uitvoeringsvorm](@) wijst.

## Gerelateerd

- [canoniek id](@) — wat de alias resolve’t (opslagvorm)
- Id-velden van [zangstuk](@), [variant](@), [uitvoeringsvorm](@),
  [representatie](@)
- [herkomst](@) — *niet* hetzelfde: herkomst is metadata over oorsprong, geen
  zoeknaam
- Catalogus-resolver / `zoek=` — praktijkinvoer die aliases gebruikt
- [Zangstukmodel §2](../specs/terminologie.md#2-canonieke-ids-en-aliassen)
  (vorm, scope, matching); gangbaar gebruik in
  [§3](../specs/terminologie.md#3-gangbare-taal-vs-precieze-termen)
