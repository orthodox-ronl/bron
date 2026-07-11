---
term: compositie
formPhrases:
  - composities
  - compositie
glossaryTerm: Compositie
glossaryText: "Een YAML-bestand onder `composities/` in de [bron-repository](@) met geordende verwijzingen naar [zangstukken](@) (toekomstig: via `zangstuk-id`, `variant-id`, `uitvoeringsvorm-id`). Nog niet geïmplementeerd."
glossaryNotes:
  - "Nog niet geïmplementeerd in de [bron-repository](@)."
  - "Niet verwarren met [samenstelling](@) (parochie-markdown met `:::include`) of sjabloon (markdown met `:::include zoek=`)."
---

# Compositie

Een **compositie** is een YAML-bestand onder `composities/` in de [bron-repository](@) met geordende verwijzingen naar [zangstukken](@) — in de toekomst via het volledige pad `(zangstuk-id, variant-id, uitvoeringsvorm-id)`.

*(Nog niet geïmplementeerd in de bron-repository.)*

| Term              | Waar                              | Formaat                                                     |
| ----------------- | --------------------------------- | ----------------------------------------------------------- |
| **Compositie**    | org-brede ordered list (toekomst) | yaml in `bron/composities/`                                 |
| **Sjabloon**      | parochie                          | markdown + `default.gelegenheidstype` + `:::include zoek=`  |
| **Samenstelling** | parochie-publicatie               | markdown + `:::include` met catalogus-pad                   |

Niet verwarren met [samenstelling](@) (een ingevuld parochie-document) of sjabloon.

## Motivatie

Op organisatieniveau kan het nuttig zijn om een geordende lijst van [zangstukken](@) te hebben die bij een bepaalde dienst of gelegenheid horen — los van welke parochie die dienst viert. Dat is iets fundamenteel anders dan een parochie-specifieke [samenstelling](@): een compositie beschrijft de *structuur* van een dienst vanuit de bron-repository, niet een concrete publicatie voor een specifiek koor.

De term reserveert een plek voor dit concept, zodat het niet verward wordt met [samenstelling](@) of [variant](@), en zodat toekomstige tooling een duidelijk aanknopingspunt heeft.

Zie ook: [Terminologie, paragraaf 19](../specs/terminologie.md#19-compositie).
