---
doc_type: wayfinding-hub
audience: "P1 — Parochie-docs-maintainer; P2 — Bron-contentbeheerder; P5 — Docs-/tool-contributor"
---
# Documentatie — bron repository

Welkom bij de documentatie van de **bron**-repository: de centrale bron van
waarheid voor [zangstukken](@) binnen [orthodox-groningen](https://github.com/orthodox-groningen).

Deze site is voor **wie zangstukken of documentatie beheert** — niet voor het
koor dat een dienst oefent of een partituur volgt. Daarvoor: de parochie-site
(bijv. [VSA-demo](https://github.com/orthodox-groningen/VSA-demo)).

## Wie ben je? (kies je route)

| Ik wil …                                               | Persona | Start hier                                                                                          |
| ------------------------------------------------------ | ------- | --------------------------------------------------------------------------------------------------- |
| Sjablonen / `zoek=` / catalogus voor de parochie       | P1      | [Catalogus-handleidingen](manuals/catalogus/index.md)                                               |
| Een [zangstuk](@) of bronvariant toevoegen / `access:` | P2      | [Zangstuk toevoegen](manuals/zangstuk-toevoegen.md) · [Handleidingen](manuals/index.md)             |
| Begrijpen wat wel/niet mag (afgeleide, ids, …)         | P6      | [Specificaties](specs/index.md) · [Terminologie](glossary.md)                                       |
| Docs of TEv2 bijdragen                                 | P5      | [Documentatie bijdragen](manuals/docs-bijdragen.md)                                                 |
| VSA schrijven / CLI / SVG / MusicXML                   | P3/P4   | [VSA-tooling — documentatie](https://orthodox-groningen.github.io/VSA-tooling/)                     |
| Partituur oefenen / liturgie volgen                    | P7      | **Niet hier** — parochie-site / demo                                                                |

Persona’s en toon: [Schrijfconventies](specs/schrijfconventies.md).

## Wat vind je hier

| Sectie                                         | Wat je er vindt                                                                                          |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [Starten](getting-started/index.md)            | Lokaal ontwikkelen: repo openen, docs bekijken, zangstukken valideren.                                   |
| [Handleidingen](manuals/index.md)              | Stap-voor-stap procedures (zangstuk toevoegen, copyright, catalogus-voorbeelden).                        |
| [Specificaties](specs/index.md)                | Normatieve regels: terminologie, repo-structuur, `zangstuk.yaml`, catalogus-contracten.                  |
| [Referentie](reference/index.md)               | Contractpagina’s voor conversie, exporttypes en brontype-validatie — ter naslag naast de specificaties.  |
| [Terminologie](glossary.md)                    | Gegenereerde glossary van org-brede begrippen (na TEv2-build).                                           |
| [Plannen](plans/README.md)                     | Ontwikkelplannen en ideeën. Die zijn niet normatief; bij twijfel gelden specificaties en handleidingen.  |

## Waar hoort wat?

| Vraag                                              | Ga naar                                                                                         |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Hoe voer ik een taak uit in de bron-repo?          | [Handleidingen](manuals/index.md)                                                               |
| Wat betekent een term, en wat mag wel/niet?        | [Specificaties](specs/index.md) en [Terminologie](glossary.md) in **deze** site                 |
| Hoe werkt de VSA-CLI (validate, svg, MusicXML)?    | [VSA-tooling — documentatie](https://orthodox-groningen.github.io/VSA-tooling/)                 |

Zie ook [Documentatie-eigendom](specs/documentatie-eigendom.md): normatieve
org-specs horen alleen in bron; tool-docs horen in [VSA-tooling](@).

## Wat staat *niet* op deze site

De [zangstukken](@) zelf (`zangstukken/`, `composities/`) staan in git maar worden
niet als webpagina's gepubliceerd. Parochie-sites en build-pipelines consumeren
die inhoud rechtstreeks uit de repository.

[Afgeleide](@) bestanden (SVG, MXL, …) — zie
[Inhoudslevenscyclus](specs/inhoudslevenscyclus.md).

## Lokaal bekijken

```cmd
cd /d C:\Git\orthodox-groningen\bron
scripts\docs-serve.cmd
```

Met TermRefs (na `npm install`): `scripts\docs-serve-tev2.cmd`.

## Externe tools

Conversie en validatie van [vsa-bestanden](@) gebeurt met
[VSA-tooling](@)
([documentatiesite](https://orthodox-groningen.github.io/VSA-tooling/))
([`vsa validate`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/validate/),
[`vsa svg`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/svg/),
[`vsa musicxml`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/musicxml/)).
