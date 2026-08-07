# TEv2 H4 — eenvoudige TermRefs (inventaris)

| Veld               | Waarde                |
| ------------------ | --------------------- |
| **Status**         | in-uitvoering         |
| **Repo**           | bron + VSA-tooling    |
| **Scope**          | Hoofdonderwerp 4      |

## Doel

Enkelvoudige begrippen (bestaande curated texts) als TermRef in prioritaire
pagina’s plaatsen. Geen meerwoordige concepten, geen synoniempass, geen
tekstinkorting (dat is H5).

## Set H4 — bron (`docs/terms/`)

Kernset voor hubs/handleidingen:

`zangstuk`, `variant`, `uitvoeringsvorm`, `representatie`, `bronbestand`,
`afgeleide`, `bron-repository`, `source-entry`, `samenstelling`,
`conversiemechanisme`, `exporttype`, `vsa-notatie`, `vsa-bestand`, `vsa-tooling`

Overige bron-terms blijven beschikbaar; TermRefs volgen waar ze in tekst
voorkomen.

## Set H4 — VSA-tooling (`docs/terminologie/`)

Tool-set:

`parser`, `validator`, `renderer`, `diagnostic`, `severity`, `modifier`,
`pitch-marker`, `hoogte-modifier`, `lengte-modifier`, `vsa-toml`, `ast`

Org-termen in tool-docs: via `@bron` (bijv. `[zangstuk](@bron)`,
`[VSA-notatie](@bron)`, `[vsa-bestand](@bron)`).

## Parkeren tot H5

`VSA-tekst`, `VSA-blok`, *geldige VSA(-notatie)*, synoniem “klopt” → “geldig”.

## Prioritaire pagina’s (deze golf)

| Repo        | Pagina’s                                                                     |
| ----------- | ---------------------------------------------------------------------------- |
| bron        | home, Starten, specs/manuals/reference-hubs, zangstuk-/bronvariant-toevoegen |
| VSA-tooling | home, Starten, manuals-hub, user-guide (§1–2), validation-guide              |
