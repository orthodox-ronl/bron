# Overzicht

Deze pagina helpt je om de [bron-repository](@) en de documentatie lokaal
bruikbaar te maken. Uitgebreide procedures staan onder
[Handleidingen](../manuals/index.md).

## 1. Repository openen

```cmd
cd /d C:\Git\orthodox-groningen\bron
```

## 2. Documentatie lokaal bekijken

```cmd
cd /d C:\Git\orthodox-groningen\bron
scripts\docs-serve.cmd
```

De site opent typisch op `http://127.0.0.1:8000/`. Voor de volledige TEv2-pipeline
(glossary en TermRefs) gebruik je later `scripts\docs-build-tev2.cmd`; dat hoort
niet bij deze eerste stappen.

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
