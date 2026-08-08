# TEv2 — bredere TermRef-campagne

| Veld        | Waarde                                                         |
| ----------- | -------------------------------------------------------------- |
| **Status**  | eerste golf gedaan (fase E.2); rest backlog                    |
| **Repo**    | bron (+ VSA-tooling later waar nodig)                          |
| **Scope**   | Follow-up na H4–H6 en contentplan fasen A–D                    |

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
| E.2  | Steekproef: 1× spec, 1× reference, 1× task guide, 1× hub (onder)  |

H5 parkeerde expliciet: *geen* volledige campagne op alle history/spec-pagina’s.

## Eerste golf (fase E.2) — gedaan

| Type        | Pad                                                      | Notitie                                        |
| ----------- | -------------------------------------------------------- | ---------------------------------------------- |
| Spec        | `docs/specs/inhoudslevenscyclus.md`                      | TermRefs op lagen + workflow                   |
| Reference   | `docs/reference/exportcontracten.md`                     | Was 0 TermRefs; nu export/conversie-keten      |
| Task guide  | `docs/manuals/parochie-lokaal-zangstukken.md`            | parochie-lokaal, promotie, bron-repository     |
| Hub         | `docs/manuals/catalogus/index.md`                        | samenstelling, bron, promotie, uitvoeringsvorm |

Geen nieuwe glossary-termen in deze golf (sjabloon, content-source, frontmatter
blijven uncured jargon tot eigen PR).

## Backlog (later)

1. Inventaris: overige specs/reference met bare termen die al in `terms/` staan
2. Dunne manuals / long catalogus-API / `rene-*` stories (selectief)
3. TermRefs plaatsen (bron `@`, tool-docs `@` / `@bron` volgens eigendom)
4. Alleen inkorten waar hover de definitie al dekt (schrijfconventies)
5. `docs-build-tev2` / TermRef-check groen houden
6. Geen normatieve betekenis wijzigen zonder glossary-PR

## Niet in scope

Nieuwe termen bedenken zonder glossary-PR; synoniembeleid opnieuw openbreken;
dark mode / IA.

Eigen PR(s); niet mengen met ongerelateerde docs-wijzigingen.
