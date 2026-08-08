---
doc_type: wayfinding-hub
audience: "P6 — Spec-/PR-reviewer; P4 — Consumer-site builder"
---
# Overzicht

Deze sectie bevat **contractpagina’s ter naslag**: wat conversie en export
betekenen voor auteurs en tooling, en hoe brontypes worden gevalideerd. Het zijn
geen stap-voor-stap handleidingen; die staan onder
[Handleidingen](../manuals/index.md). CLI-details van `vsa` staan in de
[VSA-tooling](@)-documentatie
([site](https://orthodox-groningen.github.io/VSA-tooling/)).

## Conversie

Conversie is de vaste toolstap van [bronbestand](@) naar [afgeleide](@)
(bijvoorbeeld [VSA-notatie](@) naar SVG). Zie ook
[conversiemechanismen](@).

| Pagina                                                      | Wat je er vindt                                      |
| ----------------------------------------------------------- | ---------------------------------------------------- |
| [Conversiemechanismen — overzicht](conversiemechanismen.md) | Welke conversies er zijn en hoe ze samenhangen.      |
| [Conversie vsa → svg](conversie-vsa-svg.md)                 | Contract voor VSA naar SVG.                          |
| [Conversie vsa → musicxml](conversie-vsa-musicxml.md)       | Contract voor VSA naar MusicXML / MXL.               |

## Export

Export beschrijft hoe een [afgeleide](@) of bron in een [samenstelling](@)
verschijnt (bijvoorbeeld via `:::include`). Elk [exporttype](@) heeft een eigen
contractpagina.

| Pagina                                              | Wat je er vindt                         |
| --------------------------------------------------- | --------------------------------------- |
| [Exportcontracten — overzicht](exportcontracten.md) | Overzicht van exporttypes en regels.    |
| [Exporttype svg](exporttype-svg.md)                 | Contract voor exporttype `svg`.         |
| [Exporttype coria](exporttype-coria.md)             | Contract voor exporttype `coria`.       |
| [Exporttype mxl](exporttype-mxl.md)                 | Contract voor exporttype `mxl`.         |

## Overig

| Pagina                                           | Wat je er vindt                                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| [Brontypes en validatie](brontypes-validatie.md) | Welke brontypes er zijn en wat validatie daarop controleert.                                                 |
| [Catalogus CLI](catalogus-cli.md)                | Commando’s rond de catalogus; zie ook het [sjabloon-contract](../specs/catalogus-samenstelling-zangstuk.md). |
