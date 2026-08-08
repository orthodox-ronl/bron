---
term: afgeleide
formPhrases:
  - afgeleide
  - afgeleiden
  - afgeleide(n)
glossaryTerm: Afgeleide
glossaryText: "Een bestand dat volledig en herhaalbaar door een [conversiemechanisme](@) uit een [bronbestand](@) wordt gegenereerd, en dat (dus) niet als [bronbestand](@) in de [bron-repository](@) staat."
glossaryNotes:
  - "Voorbeelden: `.svg` via `vsa svg`; `.mxl` via `vsa musicxml`."
  - "Afgeleiden worden niet getrackt in de [bron-repository](@); ze worden gegenereerd tijdens de build."
---

# Afgeleide

Een **afgeleide van een [bronbestand](@) B** is een bestand AB waarvoor een [conversiemechanisme](@) CM bestaat zodat AB = CM(B), waarbij CM geautomatiseerd en herhaalbaar is en AB niet als [bronbestand](@) in de [bron-repository](@) is, of wordt opgenomen.

| Status | Voorbeeld                                       |
| ------ | ----------------------------------------------- |
| Ja     | `.svg` uit `vsa svg`; `.mxl` uit `vsa musicxml` |
| Nee    | `.vsa`; handbewerkt `.vsa`; scan-PDF            |

## Motivatie

Het complement van [bronbestand](@). Door expliciet te benoemen wat een afgeleide is, is duidelijk welke bestanden *niet* in git horen en bij elke build opnieuw gegenereerd worden. Dat houdt de [bron-repository](@) schoon: geen onnodige binaire bestanden, geen stale gegenereerde versies die afwijken van de actuele bronnen.

Het begrip maakt ook de build-pipeline toetsbaar: een tool kan controleren of een bestand dat claimt een afgeleide te zijn inderdaad volledig reproduceerbaar is uit de getrackte bronnen.

Zie ook: [Terminologie, paragraaf 11](../specs/terminologie.md#11-afgeleide).
