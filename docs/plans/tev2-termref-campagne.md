# TEv2 — bredere TermRef-campagne

| Veld        | Waarde                                                         |
| ----------- | -------------------------------------------------------------- |
| **Status**  | tweede golf gedaan; rest backlog                               |
| **Repo**    | bron (+ VSA-tooling later waar nodig)                          |
| **Scope**   | Follow-up na H4–H6 en contentplan fasen A–E                    |

## Doel

TermRefs systematisch uitbreiden voorbij de prioritaire hubs/handleidingen van
H4/H5: specificaties, referentiepagina’s, plannen en (waar gepubliceerd)
history — zodat gedefinieerde begrippen consequent hoverbaar zijn.

## Context

| Golf | Wat al gedaan is                                                  |
| ---- | ----------------------------------------------------------------- |
| H4   | [Eenvoudige TermRefs](tev2-h4-eenvoudige-termrefs.md)             |
| H5   | [Meerwoordige terms + inkorten](tev2-h5-meerwoordige-termrefs.md) |
| H6   | [Toolchain](tev2-h6-toolchain.md) (serve≈CI, checks, pins)        |
| E.2  | Steekproef: 1× spec, 1× reference, 1× task guide, 1× hub          |
| E.2b | Tweede golf: specs + exporttypes + eigendom (onder)               |

H5 parkeerde expliciet: *geen* volledige campagne op alle history/spec-pagina’s.

## Eerste golf (fase E.2) — gedaan

| Type        | Pad                                                      | Notitie                                        |
| ----------- | -------------------------------------------------------- | ---------------------------------------------- |
| Spec        | `docs/specs/inhoudslevenscyclus.md`                      | TermRefs op lagen + workflow                   |
| Reference   | `docs/reference/exportcontracten.md`                     | Was 0 TermRefs; nu export/conversie-keten      |
| Task guide  | `docs/manuals/parochie-lokaal-zangstukken.md`            | parochie-lokaal, promotie, bron-repository     |
| Hub         | `docs/manuals/catalogus/index.md`                        | samenstelling, bron, promotie, uitvoeringsvorm |

## Tweede golf — gedaan

| Type        | Pad                                                         | Notitie                                      |
| ----------- | ----------------------------------------------------------- | -------------------------------------------- |
| Spec        | `docs/specs/repo-structuur.md`                              | bron vs afgeleide, compositie, samenstelling |
| Spec        | `docs/specs/zangstuk-identificatie.md`                      | vier niveaus + manifest                      |
| Spec        | `docs/specs/catalogus-samenstelling-zangstuk.md`            | intro + mixed session                        |
| Spec        | `docs/specs/documentatie-eigendom.md`                       | VSA-tooling, export/conversie                |
| Reference   | `docs/reference/conversiemechanismen.md`                    | densify conversie/export                     |
| Reference   | `docs/reference/exporttype-mxl.md`                          | was 0 TermRefs                               |
| Reference   | `docs/reference/exporttype-coria.md`                        | exporttype + samenstelling                   |

Geen nieuwe glossary-termen in deze golven (sjabloon, content-source, frontmatter,
catalogus-pad blijven uncured jargon tot eigen PR).

## Backlog (later)

1. `catalogus-architectuur.md`, `catalogus-zoek-api.md`, `catalogus-cli.md` (selectief)
2. `zangstuk-formaat.md` / overige reference densify
3. Dunne manuals / `rene-*` stories (selectief)
4. VSA-tooling tool-docs waar org-termen bare blijven (`@bron`)
5. Alleen inkorten waar hover de definitie al dekt (schrijfconventies)
6. `docs-build-tev2` / TermRef-check groen houden
7. Geen normatieve betekenis wijzigen zonder glossary-PR

## Niet in scope

Nieuwe termen bedenken zonder glossary-PR; synoniembeleid opnieuw openbreken;
dark mode / IA; volledige `terminologie.md`-herhaling (is zelf de glossary).

Eigen PR(s); niet mengen met ongerelateerde docs-wijzigingen.
