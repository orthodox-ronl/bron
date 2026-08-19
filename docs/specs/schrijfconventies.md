---
doc_type: normative-spec
audience: "P5 — Docs-/tool-contributor; P6 — Spec-/PR-reviewer"
---

# Schrijfconventies

Richtlijnen voor documentatie in de `bron`-repository en verwante tool-repo's
(VSA-tooling).

**Doeltoon:** schrijf voor **welwillende volwassenen** — geen techneut aannemen
tenzij de pagina expliciet voor contributors of reviewers is. Compleet en
begrijpelijk gaat boven compact, maar *op de juiste plek*: tekst inkorten is
geen doel; informatie mag verhuizen, niet verdwijnen.

Dit document is de **canonieke** plek voor schrijfregels (persona’s, paginatypen,
jargon, foutpaden, term-sjabloon). Uitvoeringsplannen mogen ernaar verwijzen;
bij conflict geldt dit document boven plannen.

---

## Publieken (persona’s)

| Id     | Persona                       | Typische vraag                                         | Primaire plek                                      |
| ------ | ----------------------------- | ------------------------------------------------------ | -------------------------------------------------- |
| **P1** | Parochie-docs-maintainer      | Hoe schrijf ik een sjabloon / `zoek=` / build?         | Catalogus-handleidingen; VSA consumer/CLI          |
| **P2** | Bron-contentbeheerder         | Hoe voeg ik een zangstuk / variant / `access:` toe?    | bron `manuals/`                                    |
| **P3** | Notatie-auteur                | Hoe schrijf/valideer ik VSA? Wat betekent deze marker? | VSA Starten, guides, syntax, lokale terms          |
| **P4** | Consumer-site builder         | Hoe hang ik Hugo + SVG/CI aan VSA-tooling?             | VSA reuse, svg-export, CLI `build-markdown`        |
| **P5** | Docs-/tool-contributor        | Hoe draait TEv2? Wat is normatief waar?                | docs-bijdragen, tev2-docs, specs                   |
| **P6** | Spec-/PR-reviewer             | Wat mag wel/niet? Wanneer is iets een afgeleide?       | bron specs + terms + glossary                      |
| **P7** | Eindgebruiker koor / liturgie | Partituur oefenen, dienst volgen                       | **Niet** deze docs (parochie-site / VSA-demo)      |

Op Home/Starten: hard zeggen dat **koor / liturgie** hier niet bediend wordt
(doorverwijzen).

### Persona’s in lezerstekst

Ids `P1`–`P7` zijn **interne labels** (frontmatter, plannen, review). Op
pagina’s die lezers zien (hubs, “Voor wie”, route-tabellen, admonitions):

- Gebruik de **persona-naam** (`Notatie-auteur`, `Bron-contentbeheerder`, …).
- **Niet** alleen `P3`, `P4`, … — dat zegt een lezer niets.
- Optioneel in contributor-docs: `Notatie-auteur (P3)` of frontmatter
  `P3 — Notatie-auteur`.
- Kolomkop op route-tabellen: **Voor wie** (niet “Persona” met alleen een code).

---

## Paginatypen

Mappen (`manuals/`, `specs/`, …) volgen [documentatie-eigendom](documentatie-eigendom.md).
Onderstaande typen sturen **toon en inhoud**. Eén bestand = één type; mengvormen
expliciet markeren.

| Type                         | Lezersvraag                                      | Taal / diepte                                                                                         | Canonieke plek (voorbeeld)                          |
| ---------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Wayfinding hub**           | Waar moet ik zijn?                               | Kort; persona-routes; “wanneer”; wat *niet* hier                                                      | `index.md`, sectie-indexen                          |
| **Onboarding**               | Hoe begin ik *hier*?                             | Eenvoudige taal; stappen; “klaar als…”                                                                | `getting-started/`                                  |
| **Task guide**               | Hoe doe ik taak X?                               | Stappen + voorbeeld + checklist + **foutpad** + link naar norm                                        | `manuals/zangstuk-toevoegen.md` e.d.                |
| **User story / walkthrough** | Hoe doet persona Y dit end-to-end?               | Narratief, volwassen, zonder nodeloos moeilijke woorden; doelbeeld vs “werkt nu”                      | `manuals/catalogus/`                                |
| **Normative spec**           | Wat is de regel?                                 | Formeel mag; optioneel “snelle uitleg”-box bovenaan                                                   | `specs/`                                            |
| **Org-contract**             | Wat/wanneer mag deze export/conversie?           | Waartoe → wel/niet → parameters → problemen → CLI-brug                                                | `reference/exporttype-*`, `conversie-*`             |
| **CLI man-page**             | Waartoe dient het commando, en wat doet het?     | Precies; synopsis; I/O; exit; goed+**fout** voorbeeld                                                 | VSA `reference/cli/`; bron `catalogus-cli`          |
| **Workflow-guide**           | Waartoe de workflow? Hoe hangt de keten samen?   | Wanneer wel/niet; 2–3 paden; diagnose; **geen** flag-catalogus (link man-pages)                       | VSA guides (bijv. svg-export)                       |
| **Term entry (curated)**     | Wat betekent dit? Waartoe? Gerelateerd? Verder?  | Zie [Term-entry-sjabloon](term-entry-sjabloon.md)                                                     | `docs/terms/`, VSA `terminologie/`                  |
| **Generated glossary**       | Overzicht + hover                                | Shelltekst; verschil glossary / termpagina / terminologie-spec                                        | `glossary.md`                                       |
| **Integratie / ownership**   | Waar hoort welke repo?                           | Rollen, minimale keten                                                                                | documentatie-eigendom; consumer-site                |
| **Non-normative plan**       | Wat overwegen we?                                | Statusbanner; wijkt nooit af van specs                                                                | `docs/plans/`                                       |

Oudere rollen “Org-referentie / Handleiding / CLI / Workflow” vallen onder
org-contract + normative spec, task guide, CLI man-page en workflow-guide.

Zie [documentatie-eigendom](documentatie-eigendom.md): org-contracten in bron;
tool-CLI en Hugo-build in de tool-repo. **Geen tweede volledige CLI-handleiding
in bron-referentie** — link naar de man-page.

---

## Pagina-kopnorm

Elke gepubliceerde pagina (behalve puur gegenereerde shelltekst) begint met:

1. **Voor wie** (één zin of admonition; **persona-naam**, geen kale `P`-code).
2. **Wanneer lees je dit** (en wanneer *niet* — link naar het juiste type).
3. **Antwoord eerst** (1–3 zinnen), daarna diepte.
4. Onderaan: **Zie ook** (how-to ↔ spec ↔ CLI ↔ term).

Expertpagina’s (docs-/tool-contributor, spec-/PR-reviewer) mogen dichter zijn,
mits 1–2 duidelijk zijn.

### Frontmatter `doc_type` / `audience`

Gebruik YAML-frontmatter op gepubliceerde pagina’s (behalve puur gegenereerde
HRG-cellen). Niet verplicht voor MkDocs-nav; wél voor review en later tooling.

| Veld        | Waarde                                                                                                                                                                                                                                  |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `doc_type`  | Paginatype uit de tabel hierboven, kebab-case: `task-guide`, `normative-spec`, `wayfinding-hub`, `cli-man-page`, `org-contract`, `workflow-guide`, `user-story`, `onboarding`, `term-entry`, `generated-glossary`, `integratie`, `plan` |
| `audience`  | Primaire lezer(s) als **herkenbare tekst**: `P3 — Notatie-auteur` (niet alleen `P3`). Meerdere: scheiden met `; `                                                                                                                       |

Voorbeeld:

```yaml
---
doc_type: task-guide
audience: "P2 — Bron-contentbeheerder"
---
```

---

## Lezerstest

**Staande regel:** na schrijven of herschrijven **nalezen alsof je de bedoelde
lezer bent**. Begrijp je zonder voorkennis van dit project wat de schrijver
bedoelde? Zo nee: herschrijf tot dat wel zo is. Codes, afkortingen en
interne ids (`P3`, `E.3`, …) horen niet in lezerstekst tenzij de pagina
expliciet uitlegt wat ze betekenen.

Per sectie (en bij PR-review):

1. Welke vraag beantwoordt dit?
2. Staat het antwoord eerst in gewone taal, daarna pas formele tabellen?
3. Past de toon bij het paginatype en de primaire persona (welwillende volwassene
   tenzij docs-/tool-contributor of spec-/PR-reviewer)?
4. Bij task guide / CLI / workflow: is er een **foutpad** (melding → oorzaak → fix)?
5. Zou een lezer zonder dit document te kennen de labels en tabellen begrijpen
   (geen kale `P3` / jargon zonder TermRef of uitleg)?

---

## Taal en terminologie

- Schrijf in begrijpelijk Nederlands; vermijd onnodig jargon.
- **Jargon-regel:** gebruik alleen termen die in de glossary staan
  ([terminologie.md](terminologie.md), [glossary](../glossary.md), curated texts).
  Is jargon nodig of nuttig en ontbreekt de term → **eerst** curated text
  (`docs/terms/` of in VSA `terminologie/`) + glossary-entry, **daarna** TermRef
  bij gebruik. Geen ad-hoc jargon in lopende tekst.
- Bij elke gedefinieerde term: **TermRef** `[term](@)` (in tool-docs voor
  org-termen: `[term](@bron)`).
- Geen synoniemen die verwarring geven (R1–R5).
- **Compact via TermRefs:** als een term in de glossary staat, herhaal de
  definitie niet in de lopende tekst; één TermRef volstaat (hover / termpagina).
- Termpagina’s volgen het [Term-entry-sjabloon](term-entry-sjabloon.md).

| Term / frase            | Gebruik                                                                                                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Conversie**           | Tool met vaste I/O ([`vsa svg`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/svg/), [`vsa musicxml`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/musicxml/)) |
| **Export**              | Hoe een afgeleide in een samenstelling verschijnt (`:::include …`)                                                                                                                                |
| **Kanaal**              | Verouderd — gebruik *conversie* of *exporttype*                                                                                                                                                   |
| **geldige VSA-notatie** | Voorkeur boven “VSA klopt” / “kloppende VSA” (tool-docs, VSA-tooling)                                                                                                                             |

---

## Org-referentie (contractpagina’s)

Twee families met vaste structuur:

| Familie       | Overzicht                                                    | Per type                                                                                                                                                 |
| ------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Export**    | [Exportcontracten](../reference/exportcontracten.md)         | [exporttype-svg](../reference/exporttype-svg.md), [exporttype-coria](../reference/exporttype-coria.md), [exporttype-mxl](../reference/exporttype-mxl.md) |
| **Conversie** | [Conversiemechanismen](../reference/conversiemechanismen.md) | [conversie-vsa-svg](../reference/conversie-vsa-svg.md), [conversie-vsa-musicxml](../reference/conversie-vsa-musicxml.md)                                 |

Opbouw (lezersgericht): waartoe → wanneer wel/niet → wat mag → parameters
(betekenis voor de auteur) → fouten op betekenisniveau → brug “technisch
uitvoeren” met link naar CLI man-page of workflow-guide.

### Parameters (org-contract)

Elke parameter minimaal: naam, verplicht?, type, standaard, **betekenis voor de
lezer**, toegestane/verboden waarden, effect per waarde, interactie, voorbeeld.
CLI-flags, build-paden en shortcodes horen in de tool-repo, niet hier herhaald.

---

## Handleidingen (task guides)

- Genummerde stappen; concrete voorbeelden (wat typ je, wat zie je); verwacht resultaat.
- Geen verborgen aannames over mappen of tools.
- Diepe toolcommando’s: korte stap + link naar de CLI man-page; geen tweede
  volledige flag-catalogus.
- **Foutpad verplicht:** typische fout(en) met melding, korte oorzaak en fix
  (of link naar CLI-foutvoorbeeld).

---

## Workflow-guides

- Begin met **waartoe** / wanneer wel en niet.
- Toon 2–3 commandopaden; diagnose bij falen; verwijs naar man-pages en
  org-contracten.
- Geen volledige flag-catalogus dupliceren.

---

## CLI man-pages (org-brede norm voor tool-CLI’s)

Voor elke CLI (bijv. `vsa`, later ook `catalogus`):

### Overzichtspagina

- Waartoe de tool dient (helder NL + TermRefs).
- Aanroepcontext (bijv. Windows `cmd`, werkmap).
- Algemene syntax: `tool <subcommando> [opties] …`.
- Gemeenschappelijke conventies: exitcodes, globale opties (`--version`, `--help`).
- Index van subcommando’s met één-regel doel + link naar de man-page.
- Geen volledige argumentenlijst per subcommando (dat hoort op de deelpagina’s).

### Eén pagina per subcommando (man-page-niveau)

1. Naam / korte samenvatting (**waartoe**)
2. Synopsis (volledige syntax, optionele delen gemarkeerd)
3. Beschrijving (precies gedrag: input, verwerking, volgorde)
4. Argumenten en opties (naam, verplicht?, type, betekenis, standaard, restricties)
5. Uitvoer (scherm / bestand / directory; waar komt het terecht?)
6. Exitstatus
7. Voorbeelden — goed pad (concrete input + commando + output + bestemmingen)
8. Voorbeelden — foutpad (input + commando + fouttekst + korte oorzaak/oplossing)
9. Zie ook (org-contract, verwante subcommando’s, workflow-guides)

Workflow-guides vatten ketens samen en **verwijzen** naar deze man-pages.

Canonieke `vsa`-CLI: [VSA-tooling CLI-referentie](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/).

---

## Geen informatieverlies

- Verplaats inhoud naar de rol/repo waar die nuttigst is; wis niet zonder bestemming.
- Bij herschrijven: checklist wat blijft / wat verhuist / link terug.

---

## Markdown-tabellen

Kolommen **aligneren in de bron**: cellen in dezelfde kolom even breed (spatiëring
met spaties). Separator-regel per cel: spatie + `---` + alignment + spatie.

Voorbeeld:

```markdown
| Parameter | Verplicht? | Standaard       |
| --------- | ---------- | --------------- |
| `alt`     | Nee        | `"VSA notatie"` |
| `scale`   | Nee        | geen schaling   |
```

Cursor-agents: `.cursor/rules/markdown-table-layout.mdc`. Bulk:
`python scripts/align_markdown_tables.py docs/` (VSA-tooling).

---

## Algemene checklist (per concept)

| Vraag                 | Wat de lezer moet kunnen vinden                      |
| --------------------- | ---------------------------------------------------- |
| Waarvoor?             | Doel, gebruikersscenario, uitgaveprofiel             |
| Wat gebeurt er?       | Op de juiste rolpagina: contract, stappen of CLI     |
| Effect van waarden    | Wat verandert bij keuze A vs. B                      |
| Toegestaan / verboden | Lijsten, voorbeelden fout vs. goed                   |
| Standaard             | Gedrag als een parameter ontbreekt                   |
| Fouten                | Concrete melding, oorzaak, oplossing                 |
| TBD                   | Open punten expliciet — geen stilzwijgende aannames  |

Korte alinea’s; genummerde stappen in workflows; admonitions (`!!! note`,
`!!! warning`) voor uitzonderingen.

---

## MkDocs

- Nederlandse prose; code en paden in monospace
- Mermaid-diagrammen voor ketens en pipeline-fases
- Lokaal: `docs-serve.cmd` (snel) of `docs-serve-tev2.cmd` (TermRefs zoals CI)
- `scripts\docs-build-tev2.cmd` / CI moet slagen vóór merge (`check-tev2-termrefs.py`)
- Contributor-checklist: [Documentatie bijdragen](../manuals/docs-bijdragen.md)
