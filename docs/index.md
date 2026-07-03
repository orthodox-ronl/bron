# Documentatie — bron repository

Welkom bij de documentatie van de **bron**-repository: de centrale bron van
waarheid voor zangstukken binnen [orthodox-groningen](https://github.com/orthodox-groningen).

## Wat vind je hier

| Sectie            | Inhoud                                                                                  |
| ----------------- | --------------------------------------------------------------------------------------- |
| **Specificaties** | Normatieve org-docs: terminologie, catalogus-sjablonen, repo-structuur, `zangstuk.yaml` |
| **Handleidingen** | Stap-voor-stap workflows (incl. parochie-lokaal, catalogus-gebruikersverhalen)          |
| **Referentie**    | Lookup-tabellen: conversiemechanismen, exportcontracten, brontype-validatie             |
| **Plannen**       | Ontwikkelplannen — *niet normatief*; specs en handleidingen zijn leidend                |

## Wat staat *niet* op deze site

De **zangstukken zelf** (`zangstukken/`, `composities/`) staan in git maar worden
niet als webpagina's gepubliceerd. Parochie-sites en build-pipelines consumeren
die inhoud rechtstreeks uit de repository.

**Afgeleide** bestanden (SVG, MXL, …) horen niet in git; zie
[Inhoudslevenscyclus](specs/inhoudslevenscyclus.md).

## Lokaal bekijken

```cmd
cd /d C:\Git\orthodox-groningen\bron
scripts\docs-serve.cmd
```

## Externe tools

Conversie en validatie van VSA-bestanden gebeurt met
[VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling) (`vsa validate`,
`vsa svg`, `vsa musicxml`).
