---
term: vsa-tooling
termType: concept
glossaryTerm: "VSA-tooling"
glossaryText: "De Python-toolchain (`vsa` CLI) waarmee [vsa-notatie](@)-bestanden worden geparseerd, gevalideerd en omgezet naar [afgeleiden](@) zoals SVG en MusicXML."
glossaryNotes:
  - "De `vsa`-CLI biedt subcommando's voor validatie (`vsa validate`), rendering (`vsa svg`) en export (`vsa musicxml`)."
  - "VSA-tooling genereert [afgeleiden](@) uit [bronbestanden](@); de [afgeleiden](@) zelf worden niet in de [bron-repository](@) opgeslagen."
  - "De tooling bevindt zich in de repo [orthodox-groningen/VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling)."
formPhrases:
  - vsa-tooling
  - vsa-tool
  - vsa-tools
---

# VSA-tooling

**VSA-tooling** is de Python-toolchain voor het verwerken van [VSA-notatie](@)-bestanden. De kern is de `vsa` CLI, die subcommando's biedt voor parseren, valideren en omzetten naar publicatievormen.

## Subcommando's

| Commando             | Wat het doet                                                            |
| -------------------- | ----------------------------------------------------------------------- |
| `vsa validate`       | Valideert een [vsa-bestand](@) of map op syntaxfouten                   |
| `vsa svg`            | Genereert een SVG-[afgeleide](@) (notenbalken) uit een [vsa-bestand](@) |
| `vsa musicxml`       | Genereert een MusicXML-[afgeleide](@) (`.mxl`) uit een [vsa-bestand](@) |
| `vsa parse`          | Toont de parse-tree van een [vsa-bestand](@)                            |
| `vsa blocks`         | Toont de blokstructuur van een [vsa-bestand](@)                         |
| `vsa process`        | Verwerkt VSA-directives in markdown                                     |
| `vsa build-markdown` | Bouwt markdown met ingebedde VSA naar publicatievorm                    |

VSA-tooling is een [conversiemechanisme](@): het zet [vsa-bestanden](@) om naar [afgeleiden](@) (`.svg`, `.mxl`). Die [afgeleiden](@) worden niet opgeslagen in de [bron-repository](@) maar gegenereerd tijdens de build.

## Installatie

```cmd
cd /d C:\Git\orthodox-groningen\VSA-tooling
scripts\bootstrap.cmd
```

Na installatie is de `vsa`-CLI beschikbaar. Valideer zangstukken in de [bron-repository](@):

```cmd
cd /d C:\Git\orthodox-groningen\bron
vsa validate zangstukken
```

## Motivatie

[VSA-notatie](@)-bestanden zijn tekstbestanden die door mensen worden geschreven. Zonder tooling zijn er geen garanties dat bestanden syntactisch correct zijn, en is het omzetten naar weergaveformaten (SVG, MusicXML) handmatig en foutgevoelig. VSA-tooling maakt dat proces automatisch en reproduceerbaar: elke build genereert de [afgeleiden](@) opnieuw uit de getrackte [bronbestanden](@), zodat de gepubliceerde site altijd consistent is met de bronrepository.

De tooling ondersteunt ook CI: in de [bron-repository](@) valideert `vsa validate zangstukken` bij elke push of PR alle zangstukken automatisch.

## Zie ook:

- [VSA-tooling demosite](https://orthodox-groningen.github.io/VSA-tooling/)
- [GitHub orthodox-groningen/VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling)
