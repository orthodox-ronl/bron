---
term: exportmechanisme
formPhrases:
  - exportmechanismen
  - exportmechanisme
glossaryTerm: Exportmechanisme
glossaryText: "De manier waarop een [samenstelling](@) een [bronbestand](@) of [afgeleide](@) ontsluit voor een lezersdoel, via een `:::include`-directive met een [exporttype](@)."
---

# Exportmechanisme

Een **exportmechanisme** beschrijft hoe een [samenstelling](@) een [bronbestand](@) of [afgeleide](@) ontsluit voor een lezersdoel. Het exportmechanisme wordt in een [samenstelling](@) aangeroepen via een `:::include`-directive met een [exporttype](@).

```markdown
:::include svg zoek="antifoon-1 / weekdagen / liturgikon" :::
```

## Motivatie

Een [representatie](@) (bijv. een `.vsa`-bestand) kan voor verschillende doelen worden ontsloten: als notenbalken voor een koormap, als oefenmateriaal in Coria, als MusicXML voor een muziekprogramma. Het exportmechanisme maakt die keuze expliciet en configureerbaar via de `:::include`-directive in de [samenstelling](@), zodat dezelfde [representatie](@) in meerdere contexten bruikbaar is zonder het [bronbestand](@) te kopiëren of aan te passen.

Zie ook: [Terminologie, paragraaf 20](../specs/terminologie.md#20-conversiemechanisme-exportmechanisme-exporttype), [conversiemechanisme](@), [exporttype](@).
