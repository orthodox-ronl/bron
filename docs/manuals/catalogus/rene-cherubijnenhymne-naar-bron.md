# Verhaal 3 — Rene en Nana maken de Cherubijnenhymne org-breed beschikbaar

*Het lokale stuk uit [verhaal 2](rene-cherubijnenhymne-lokaal.md) bevalt;
andere parochies zouden het ook moeten kunnen gebruiken. Rene en Nana besluiten
een **pull request** op **bron** te openen — met dezelfde canonieke ids als
lokaal, zodat bestaande samenstellingen blijven werken.*

---

## Situatie

| Lokaal (parochie)                              | Doel in bron                                      |
| ---------------------------------------------- | ------------------------------------------------- |
| `lokaal/cherubijnenhymne/kastorski/groningen/` | `zangstukken/cherubijnenhymne/` + nested manifest |
| PDF (+ later VSA) onder `repr/`                | `sources/scan/` en `sources/vsa/`                 |
| Aliassen in yaml                               | Zelfde aliassen in org-brede manifesten           |

Promotie-procedure:
[parochie-lokaal § Promotie](../parochie-lokaal-zangstukken.md#promotie-naar-bron-repository).

---

## Beoogde interface (GUI)

Rene opent in de catalogus het lokale stuk *cherubijnenhymne / kastorski /
groningen* en kiest **Delen → Voorstel voor bron**.

1. **Diff-voorbeeld:** links lokaal, rechts voorgestelde bron-structuur.
2. **Id-check:** groen als `zangstuk-id`, `variant-id`, `uitvoeringsvorm-id`
   en `representatie-id` voldoen aan `[a-z0-9_-]+` en uniek zijn in bron.
3. **Bestanden:** selectie welke representaties meegaan (PDF, VSA).
4. **Metadata:** formulier voor `zangstuk.yaml` (`title`, `occasion`, copyright).
5. **PR-assistent:** genereert branch-naam, commit-bericht (Conventional Commits)
   en checklist voor `vsa validate` / `catalogus index validate`.
6. **Na merge:** hint om samenstellingen van `lokaal:` naar `bron:` om te zetten
   (optioneel; lokaal mag blijven staan).

!!! todo "GUI + promotie-workflow"
    Automatische PR-generatie en bron-yaml is **gepland**. Rene voert de stappen
    hieronder handmatig uit volgens bestaande handleidingen.

---

## Wat Rene vandaag doet

### 1. Voorbereiden in bron (fork / branch)

```cmd
cd /d C:\Git\orthodox-groningen\bron
git checkout -b feat/cherubijnenhymne-kastorski-groningen
```

### 2. Zangstuk-map (als cherubijnenhymne nog niet in bron staat)

Volg [zangstuk toevoegen](../zangstuk-toevoegen.md) of
[bronvariant toevoegen](../bronvariant-toevoegen.md) als het zangstuk al bestaat
met andere varianten.

Voorbeeldstructuur (geneste manifesten — org-spec, in uitwerking):

```text
zangstukken/cherubijnenhymne/
├── zangstuk.yaml
├── kastorski/
│   ├── variant.yaml          # zelfde aliassen als lokaal
│   └── groningen/
│       ├── uitvoeringsvorm.yaml
│       └── repr/
│           └── groningen.vsa
└── sources/
    └── scan/
        └── nana-partituur.pdf
```

**Belangrijk:** behoud `variant-id: kastorski`, `uitvoeringsvorm-id: groningen`.

### 3. `zangstuk.yaml` (minimaal)

```yaml
id: cherubijnenhymne
title: "Cherubijnenhymne"

sources:
  - id: kastorski-groningen-scan
    file: sources/scan/nana-partituur.pdf
    author: "Nana (parochie Groningen)"
    based_on: kastorski
    copyright_status: vrij
    note: "Oorspronkelijk parochie-lokaal; bewerking Kastorski-traditie"
```

Wanneer VSA klaar is: extra source-entry of representatie onder geneste yaml
(zie [zangstuk-formaat](../../specs/zangstuk-formaat.md)).

### 4. Validatie vóór PR

```cmd
python -m catalogus.cli index validate --bron-root .
vsa validate zangstukken
```

Beide moeten groen zijn.

### 5. Pull request

Rene opent een PR op `orthodox-groningen/bron` met:

- **Summary:** nieuwe uitvoeringsvorm `groningen` onder variant `kastorski`.
- **Testplan:** catalogus-index OK, VSA-validatie OK.
- **Links:** verwijzing naar parochie-lokaal herkomst (optioneel in PR-body).

Nana reviewt de muziek; een maintainer merge.

### 6. Na merge — sjabloon bijwerken

Rene past het liturgie-sjabloon aan (verhaal 1). De zoekregel kan gelijk blijven;
de catalogus wijst dan naar **bron** i.p.v. **lokaal**. Of expliciet:

```markdown
:::include svg bron:cherubijnenhymne/kastorski/groningen alt="Cherubijnenhymne":::
```

Of de zoekregel `zoek="Cherubijnenhymne (Kastorski)"` laten staan tot resolve naar **bron** wijst.

```cmd
python -m catalogus.cli resolve uitvoeringsvorm --zangstuk cherubijnenhymne --variant kastorski Groningen --bron-root C:\Git\orthodox-groningen\bron
```

Uitvoer blijft: `groningen`.

---

## Wat Rene en Nana bereiken

- Eén **canonical** exemplaar in bron; andere parochies hoeven niet Rene's repo
  te klonen.
- **Ids blijven stabiel** — geen brekende wijziging in Groningen-lokaal tot Rene
  sync't.
- Org-brede **alias-index** dekt “Groningen” zowel lokaal als in bron (scope
  afhankelijk van `--content-root` / `--bron-root`).

## Verder lezen

- [Verhaal 4 — MusicXML](rene-cherubijnenhymne-musicxml.md)
- [Inhoudslevenscyclus § bron vs afgeleid](../../specs/inhoudslevenscyclus.md)
