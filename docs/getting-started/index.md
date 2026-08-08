# Starten — lokaal ontwikkelen

Deze pagina helpt je om de [bron-repository](@) en de documentatie **lokaal**
bruikbaar te maken (repo openen, docs bekijken, valideren). Uitgebreide
procedures staan onder [Handleidingen](../manuals/index.md).

!!! note "Voor wie"
    Voor beheerders en bijdragers die de bron-repo of docs op hun machine
    willen draaien — niet voor koorzangers die een dienst willen oefenen
    (dat is de parochie-site; zie [Home](../index.md)).

## Wie ben je? (kort)

| Ik wil …                         | Ga naar                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------- |
| Alleen lokaal opstarten          | Stappen 1–3 hieronder                                                           |
| Nieuw zangstuk / copyright       | [Handleidingen](../manuals/index.md)                                            |
| Catalogus / sjablonen            | [Catalogus](../manuals/catalogus/index.md)                                      |
| VSA schrijven of CLI             | [VSA-tooling](https://orthodox-groningen.github.io/VSA-tooling/)                |

## 1. Repository openen

```cmd
cd /d C:\Git\orthodox-groningen\bron
```

## 2. Documentatie lokaal bekijken

```cmd
cd /d C:\Git\orthodox-groningen\bron
scripts\docs-serve.cmd
```

De site opent typisch op `http://127.0.0.1:8000/`. Voor glossary en TermRef-hover
(zoals in CI): `scripts\docs-serve-tev2.cmd` (eerst `npm install`). Zie
[Documentatie bijdragen](../manuals/docs-bijdragen.md).

## 3. Zangstukken valideren

Validatie van [VSA-notatie](@) in deze repo gebeurt met de CLI uit
[VSA-tooling](@)
([documentatiesite](https://orthodox-groningen.github.io/VSA-tooling/)):

```cmd
cd /d C:\Git\orthodox-groningen\VSA-tooling
scripts\bootstrap.cmd
cd /d C:\Git\orthodox-groningen\bron
vsa validate zangstukken
```

## Volgende stappen

| Doel                                      | Pagina                                                                          |
| ----------------------------------------- | ------------------------------------------------------------------------------- |
| Nieuw [zangstuk](@) toevoegen             | [Zangstuk toevoegen](../manuals/zangstuk-toevoegen.md)                          |
| Copyright zonder bestand in de repo       | [Copyright en access](../manuals/copyright-access.md)                           |
| Begrijpen wat waar mag staan              | [Documentatie-eigendom](../specs/documentatie-eigendom.md)                      |
| Tool-docs (parser, CLI, export)           | [VSA-tooling — documentatie](https://orthodox-groningen.github.io/VSA-tooling/) |
