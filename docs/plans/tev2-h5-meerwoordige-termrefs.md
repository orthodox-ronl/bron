---
doc_type: plan
audience: "P5 — Docs-/tool-contributor; P6 — Spec-/PR-reviewer"
---
# TEv2 H5 — meerwoordige terms + vereenvoudiging

| Veld        | Waarde                                                                            |
| ----------- | --------------------------------------------------------------------------------- |
| **Status**  | afgerond (H5-golf); vervolg: [bredere TermRef-campagne](tev2-termref-campagne.md) |
| **Repo**    | VSA-tooling (primair); bron (conventies)                                          |
| **Scope**   | Hoofdonderwerp 5                                                                  |

## Doel

Meerwoordige / vaste frasen als curated terms; teksten inkorten waar TermRefs
de betekenis dragen; synoniembeleid (o.a. “klopt” → “geldig”).

## Terms (VSA-tooling)

| Term                      | Status                                      |
| ------------------------- | ------------------------------------------- |
| `vsa-blokken` / VSA-blok  | Bestond al; TermRefs + tekstinkorting       |
| `vsa-tekst` / VSA-tekst   | Nieuw                                       |
| `geldige-vsa-notatie`     | Nieuw — voorkeur boven “VSA klopt”          |

## Pagina’s (deze golf)

- Gebruikershandleiding §1–2 en verdere VSA-blok-/validatie-passages
- `guides/validation.md`, CLI man-pages (`validate`, `blocks`, `process`, `svg`, index)
- [schrijfconventies](../specs/schrijfconventies.md) in bron

## Niet in deze golf

Volledige TermRef-campagne op alle history/spec-pagina’s — gepland later:
[tev2-termref-campagne.md](tev2-termref-campagne.md).

Toolchain (afgerond): [tev2-h6-toolchain.md](tev2-h6-toolchain.md).
