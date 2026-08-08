# Documentatie — bron repository

Welkom bij de documentatie van de **bron**-repository: de centrale bron van
waarheid voor [zangstukken](@) binnen [orthodox-groningen](https://github.com/orthodox-groningen).

## Wat vind je hier

| Sectie                                         | Wat je er vindt                                                                                          |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [Starten](getting-started/index.md)            | Eerste stappen: repo openen, docs lokaal bekijken, zangstukken valideren.                                |
| [Terminologie](glossary.md)                    | Gegenereerde glossary van org-brede begrippen (na TEv2-build).                                           |
| [Specificaties](specs/index.md)                | Normatieve regels: terminologie, repo-structuur, `zangstuk.yaml`, catalogus-contracten.                  |
| [Handleidingen](manuals/index.md)              | Stap-voor-stap procedures voor beheerders (zangstuk toevoegen, copyright, catalogus-voorbeelden).        |
| [Referentie](reference/index.md)               | Contractpagina’s voor conversie, exporttypes en brontype-validatie — ter naslag naast de specificaties.  |
| [Plannen](plans/README.md)                     | Ontwikkelplannen en ideeën. Die zijn niet normatief; bij twijfel gelden specificaties en handleidingen.  |

## Waar hoort wat?

| Vraag                                              | Ga naar                                                                                         |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Wat betekent een term, en wat mag wel/niet?        | [Specificaties](specs/index.md) en [Terminologie](glossary.md) in **deze** site                 |
| Hoe voer ik een taak uit in de bron-repo?          | [Handleidingen](manuals/index.md)                                                               |
| Hoe werkt de VSA-CLI (validate, svg, MusicXML)?    | [VSA-tooling — documentatie](https://orthodox-groningen.github.io/VSA-tooling/)                 |

Zie ook [Documentatie-eigendom](specs/documentatie-eigendom.md): normatieve
org-specs horen alleen in bron; tool-docs horen in [VSA-tooling](@).

## Wat staat *niet* op deze site

De [zangstukken](@) zelf (`zangstukken/`, `composities/`) staan in git maar worden
niet als webpagina's gepubliceerd. Parochie-sites en build-pipelines consumeren
die inhoud rechtstreeks uit de repository.

[Afgeleide](@) bestanden (SVG, MXL, …) horen niet in git; zie
[Inhoudslevenscyclus](specs/inhoudslevenscyclus.md).

## Lokaal bekijken

```cmd
cd /d C:\Git\orthodox-groningen\bron
scripts\docs-serve.cmd
```

## Externe tools

Conversie en validatie van [vsa-bestanden](@) gebeurt met
[VSA-tooling](@)
([documentatiesite](https://orthodox-groningen.github.io/VSA-tooling/))
([`vsa validate`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/validate/),
[`vsa svg`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/svg/),
[`vsa musicxml`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/musicxml/)).
