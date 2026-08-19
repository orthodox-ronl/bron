---
term: canoniek-id
formPhrases:
  - canoniek id
  - canonieke id
  - canonieke ids
  - canoniek ids
  - canonieke id's
glossaryTerm: Canonieke id
glossaryText: "De stabiele, machine-leesbare identifier van een entiteit ([zangstuk](@), [variant](@), [uitvoeringsvorm](@) of [representatie](@)) in opslag: lowercase ASCII volgens `^[a-z0-9_-]+$`, zonder spaties, diacritica of Cyrillisch."
glossaryNotes:
  - "Voorbeelden: `zangstuk-id` `antifoon-1-weekdagen`, `uitvoeringsvorm-id` `groningen`."
  - "Op de invoergrens mag een [alias](@) gebruikt worden; de resolver levert altijd het [canonieke id](@) voor paden, yaml, git en `bron:…`-referenties."
  - "Niet verwarren met [alias](@) (menselijke werknaam) of met [herkomst](@) (waar iets vandaan komt)."
---

# Canonieke id

Een **canoniek id** (ook: **canonieke id**) is de stabiele identifier van een
entiteit in het vier-niveaumodel die in **opslag en techniek** wordt gebruikt:
paden, yaml, git, `bron:…`-referenties, build-artefacten.

Vorm (normatief): `^[a-z0-9_-]+$` — lowercase ASCII, cijfers, `-` en `_`. Geen
spaties, hoofdletters, diacritica of Cyrillisch in het **opgeslagen** id.

| Niveau               | Id-veld              | Voorbeeld canoniek id        |
| -------------------- | -------------------- | ---------------------------- |
| [Zangstuk](@)        | `zangstuk-id`        | `antifoon-1-weekdagen`       |
| [Variant](@)         | `variant-id`         | `kastorski`                  |
| [Uitvoeringsvorm](@) | `uitvoeringsvorm-id` | `groningen`                  |
| [Representatie](@)   | `representatie-id`   | `hemelum`                    |

| Status | Voorbeeld                                              |
| ------ | ------------------------------------------------------ |
| Ja     | `groningen`, `troparion-zondag-toon-1`, `liturgikon`   |
| Nee    | `Groningen`, `1e antifoon weekdagen`, `Касторский`     |
| Nee    | Spaties of diacritica in het **opgeslagen** id         |

Invoer zoals `Groningen` mag als [alias](@) (of case-variatie); na resolve is het
[canonieke id](@) in opslag altijd `groningen`.

## Motivatie

Builds, catalogus-paden en git moeten **stabiel en eenduidig** zijn. Menselijke
spelling wisselt (`Hemelum` / `hemelum` / Cyrillisch); machine-ids niet. Het
[canonieke id](@) is die vaste kern: alles wat in de repository of in
machine-leesbare referenties terechtkomt, gebruikt precies die vorm (R5).

Zonder dit begrip zouden [aliassen](@) en ids door elkaar lopen — of elke UI
zou rechtstreeks fragile strings in paden schrijven.

## Gerelateerd

- [alias](@) — invoernaam die naar dit id resolve’t
- Id-velden van [zangstuk](@), [variant](@), [uitvoeringsvorm](@),
  [representatie](@)
- [promotie](@) — behoudt [canonieke ids](@) bij overgang naar de [bron-repository](@)
- [Zangstukmodel §2](../specs/terminologie.md#2-canonieke-ids-en-aliassen);
  R5 in [§0](../specs/terminologie.md#0-gebruiksregels-alle-repos-orthodox-ronl);
  contrast in [§3](../specs/terminologie.md#3-gangbare-taal-vs-precieze-termen)
