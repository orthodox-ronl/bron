# TEv2 H6 — docs-toolchain

| Veld        | Waarde                                      |
| ----------- | ------------------------------------------- |
| **Status**  | afgerond                                    |
| **Repo**    | bron + VSA-tooling                          |
| **Scope**   | Hoofdonderwerp 6 (toolchain-parity)         |

## Doel

Lokale docs-ervaring ≈ CI: TEv2-pipeline, TermRef-check, scriptnamen en
contributor-docs gelijk tussen bron en VSA-tooling; versie-pins vastgelegd.

## Leveringen

| Item                         | Toelichting                                              |
| ---------------------------- | -------------------------------------------------------- |
| `docs-tev2-run.cmd`          | Gedeelde preprocess (beide repo’s)                       |
| `docs-serve-tev2.cmd`        | Serve op `generated/` met opgeloste TermRefs             |
| `docs-build.cmd` (VSA)       | Parity met bron: snelle MkDocs zonder TEv2               |
| `docs-bijdragen.md` (bron)   | Contributor-handleiding scripts / TermRefs / pins        |
| Checks                       | `check-tev2-termrefs.py` al in CI; lokaal via `*-tev2`   |
| Pins                         | Material `<10`, TEv2 npm `1.2.0` — gedocumenteerd        |

## Succes

- Contributor weet welk script voor snelle vs CI-parity preview
- `docs-serve-tev2` toont glossary-hover zoals op Pages
- Scriptmatrix in AGENTS/handleidingen synchroon

## Vervolg (niet H6)

Bredere TermRef-campagne: [tev2-termref-campagne.md](tev2-termref-campagne.md).
