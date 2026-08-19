---
doc_type: normative-spec
audience: "P2 — Bron-contentbeheerder; P6 — Spec-/PR-reviewer"
---
# Repo-structuur

Status: specificatie (juni 2026).

## Doel en scope

De [bron-repository](@) bevat de muzikale inhoud voor `orthodox-ronl`.
Parochie-sites consumeren deze repository; ze bewerken hem niet rechtstreeks.

De repository bevat **bronnen** en metadata. Geen [afgeleide](@) bestanden (SVG, MXL
uit [VSA](vsa@)) in git, en geen parochie-specifiek gebruik.

## Top-level structuur

```
bron/
├── README.md
├── LICENSE-CONTENT
├── LICENSE-CODE
├── mkdocs.yml                  # documentatiesite (GitHub Pages)
├── requirements-docs.txt
├── pyproject.toml              # catalogus Python-pakket + CLI
├── src/
│   └── catalogus/              # alias-index en resolver
├── tests/
├── docs/                       # → orthodox-ronl.github.io/bron/
│   ├── specs/
│   ├── manuals/
│   ├── reference/
│   └── plans/
├── zangstukken/                # inhoud — niet de docs-site
│   └── <zangstuk-id>/
├── composities/                # toekomst — YAML-lijsten zangstukken
└── derived/                    # .gitignore — lokale/CI afgeleide
```

## Documentatie vs. inhoud

| Pad            | GitHub Pages     | Doel                                      |
| -------------- | ---------------- | ----------------------------------------- |
| `docs/`        | ja               | Specs, handleidingen, referentie, plannen |
| `zangstukken/` | nee              | Brondocumenten + `zangstuk.yaml`          |
| `composities/` | nee              | Volgorde/referenties (toekomst)           |
| `derived/`     | nee, niet in git | Build-output                              |

## Het zangstuk

### Definitie

Mapnaam van een [zangstuk](@) = stabiele `id` onder `zangstukken/`.

### Bron versus afgeleid

- **Bron:** geen geautomatiseerd generatiepad vanuit een ander bestand *in deze repo*
  ([VSA-notatie](@), scan, MusicXML uit MuseScore, …) — een [bronbestand](@).
- **[Afgeleide](@):** geautomatiseerd uit bron (SVG/MXL via [VSA-tooling](@)). Niet in git.

### Naamgeving `zangstuk-id`

- Lowercase, koppeltekens, geen diakritische tekens
- Vast feest: `<type>-<gelegenheid-slug>` — `troparion-nicolaas-van-myra`
- Zondagscyclus: `<type>-zondag-toon-<n>` — `troparion-zondag-toon-1`
- Geen gelegenheid: algemene naam — `trisagion`
- **Stabiel:** niet hernoemen zodra externe referenties bestaan

## Eén bronbestand, meerdere zangstukken

- **VSA/tekst:** splitsen — één `.vsa` per [zangstuk](@) in de juiste map
- **Scan/PDF:** niet splitsen; tweede [zangstuk](@) verwijst met relatief `file:` naar scan
  bij het eerste zangstuk

## Composities en sjablonen

| Concept                   | Locatie                                 | Status                                                               |
| ------------------------- | --------------------------------------- | -------------------------------------------------------------------- |
| **[Compositie](@)** (org) | `composities/*.yaml` in **bron**        | Toekomst — geordende yaml-lijst                                      |
| **Sjabloon** (parochie)   | markdown in parochie **content-source** | **Geïmplementeerd** — `default.gelegenheidstype`, `:::include zoek=` |
| **[Samenstelling](@)**    | markdown publicatie parochie            | §18 terminologie                                                     |

Compositie-yaml in bron: [Plannen: samenvatting project](../plans/samenvatting-project.md).
Sjabloon-contract: [catalogus-samenstelling-zangstuk.md](catalogus-samenstelling-zangstuk.md).

## Nog te ontwerpen

- Build-stap voor [afgeleide](@) + publieke index (JSON) voor parochie-builds
- Filter: `file:` wel meenemen, `access:` niet in gepubliceerde index

Zie [Inhoudslevenscyclus](inhoudslevenscyclus.md).
