---
doc_type: org-contract
audience: "P6 — Spec-/PR-reviewer; P2 — Bron-contentbeheerder"
---
# Brontypes en validatie

Overzicht van validatieregels per type [bronbestand](@) in `zangstukken/`
([bron-repository](@)).

## `.vsa`

Validatie van [vsa-bestanden](@) — bestanden met [vsa-notatie](@).

Installatie: [VSA-tooling](@)
([GitHub](https://github.com/orthodox-ronl/VSA-tooling)).

| Check                            | Tool                                                                                             | Wanneer                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------- |
| Parse + semantiek                | [`vsa validate <pad>`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/validate/) | Lokaal, CI (gepland)             |
| Frontmatter YAML                 | handmatig / CI (gepland)                                                                         | Bij aanwezigheid van `---`       |
| Consistentie met `zangstuk.yaml` | CI (gepland)                                                                                     | Geen tegenstrijdige `title`/tone |

## `.pdf` (scan)

| Check             | Tool                 | Wanneer      |
| ----------------- | -------------------- | ------------ |
| Geldig PDF        | magic bytes / `file` | CI (gepland) |
| Minstens 1 pagina | PDF-library          | CI (gepland) |
| Leesbaarheid      | mens                 | Opname scan  |

Padconventie: `zangstukken/<id>/sources/scan/*.pdf` — zie `.gitignore` uitzondering.

## Raster (`.png`, `.jpg`, …)

| Check               | Tool     | Wanneer      |
| ------------------- | -------- | ------------ |
| Geldig beeldbestand | PIL/file | CI (gepland) |

## `.musicxml` / `.mxl` als bron

| Check           | Tool             | Wanneer      |
| --------------- | ---------------- | ------------ |
| Well-formed XML | xmllint / parser | CI (gepland) |

Alleen wanneer MusicXML **zelfstandig [bronbestand](@)** is, niet wanneer het
[afgeleide](@) van [vsa-notatie](@) is.

## `zangstuk.yaml`

| Check                            | Tool                          | Wanneer        |
| -------------------------------- | ----------------------------- | -------------- |
| Schema / verplichte velden       | handmatig; yamllint (gepland) | Elke wijziging |
| `file:` bestaat                  | script                        | CI (gepland)   |
| Eén status per [source-entry](@) | script                        | CI (gepland)   |
| `based_on` geldig                | script                        | CI (gepland)   |

Validatie-workflow in `.github/workflows/` volgt in een later increment.
