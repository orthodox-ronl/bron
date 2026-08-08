---
term: exporttype
formPhrases:
  - exporttypen
  - exporttypes
  - exporttype
glossaryTerm: Exporttype
glossaryText: "De naam die in een `:::include <exporttype>`-directive aangeeft welk [exportmechanisme](@) wordt gebruikt, zoals `svg`, `coria` of `mxl`."
glossaryNotes:
  - "Huidige exporttypen: `svg`, `coria`, `mxl`."
---

# Exporttype

Het **exporttype** is de naam in een `:::include <exporttype>`-directive die aangeeft welk [exportmechanisme](@) wordt gebruikt om een [representatie](@) te ontsluiten in een [samenstelling](@).

| Exporttype | Wat het doet                                                                                                                                      |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `svg`      | Rendert een VSA-[representatie](@) naar een SVG (plaatje), met daarin de te zingen tekst en strepen onder en boven lettergrepen in de tekst (SVG) |
| `coria`    | Ontsluit een VSA-[representatie](@) voor gebruik in de Coria-oefentool                                                                            |
| `mxl`      | Exporteert een VSA-[representatie](@) als MXL (gecomprimeerde MusicXML)                                                                           |

## Motivatie

Bij het embedden van een [representatie](@) in een [samenstelling](@) moet worden aangegeven *hoe* die [representatie](@) gepresenteerd wordt. Het exporttype is de naam daarvoor in de directive-syntax. Door exporttypen expliciet te benoemen, is de interface tussen [samenstelling](@) en tooling gedocumenteerd en uitbreidbaar: een nieuw exporttype kan worden toegevoegd zonder de syntaxis van bestaande [samenstellingen](@) te breken.

Zie ook: [Terminologie, paragraaf 20](../specs/terminologie.md#20-conversiemechanisme-exportmechanisme-exporttype), [exportmechanisme](@), [conversiemechanisme](@).
