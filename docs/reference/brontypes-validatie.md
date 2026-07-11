# Brontypes en validatie

Overzicht van validatieregels per brontype in `zangstukken/`.

## `.vsa`

Validatie van [vsa-bestanden](@) — bestanden met [vsa-notatie](@).

Installatie: [VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling).

| Check                            | Tool                     | Wanneer                          |
| -------------------------------- | ------------------------ | -------------------------------- |
| Parse + semantiek                | `vsa validate <pad>`     | Lokaal, CI (gepland)             |
| Frontmatter YAML                 | handmatig / CI (gepland) | Bij aanwezigheid van `---`       |
| Consistentie met `zangstuk.yaml` | CI (gepland)             | Geen tegenstrijdige `title`/tone |

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

Alleen wanneer MusicXML **zelfstandige bron** is, niet wanneer het afgeleide van [vsa-notatie](@) is.

## `zangstuk.yaml`

| Check                      | Tool                          | Wanneer        |
| -------------------------- | ----------------------------- | -------------- |
| Schema / verplichte velden | handmatig; yamllint (gepland) | Elke wijziging |
| `file:` bestaat            | script                        | CI (gepland)   |
| Eén status per source      | script                        | CI (gepland)   |
| `based_on` geldig          | script                        | CI (gepland)   |

Validatie-workflow in `.github/workflows/` volgt in een later increment.
