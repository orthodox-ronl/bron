---
term: exportmechanisme
formPhrases:
  - exportmechanismen
  - exportmechanisme
glossaryTerm: Exportmechanisme
glossaryText: "De manier waarop een [samenstelling](@) een [bronbestand](@) of [afgeleide](@) ontsluit voor een lezersdoel, via een `:::include`-directive met een [exporttype](@)."
glossaryNotes:
  - "Niet verwarren met [conversiemechanisme](@) (bestand → afgeleide in de toolketen)."
  - "Voorbeeld: `:::include svg zoek=\"…\" :::` kiest exporttype `svg`."
---

# Exportmechanisme

Een **exportmechanisme** beschrijft hoe een [samenstelling](@) een [bronbestand](@)
of [afgeleide](@) ontsluit voor een lezersdoel, via een `:::include`-directive
met een [exporttype](@).

```markdown
:::include svg zoek="antifoon-1 / weekdagen / liturgikon" :::
```

| Status | Voorbeeld                                                                    |
| ------ | ---------------------------------------------------------------------------- |
| Ja     | SVG in een koormap; Coria-oefenlink; MXL-download in een samenstelling       |
| Nee    | `vsa svg` als losse conversie zonder `:::include` ([conversiemechanisme](@)) |
| Nee    | Het [bronbestand](@) zelf kopiëren in plaats van includen                    |

## Motivatie

Een [representatie](@) kan voor verschillende lezersdoelen nodig zijn
(notenbalken, oefentool, MusicXML). Het exportmechanisme maakt die keuze
expliciet in de [samenstelling](@), zonder het [bronbestand](@) te kopiëren.

## Gerelateerd

- [exporttype](@), [conversiemechanisme](@), [samenstelling](@)
- [Terminologie, paragraaf 20](../specs/terminologie.md#20-conversiemechanisme-exportmechanisme-exporttype)
