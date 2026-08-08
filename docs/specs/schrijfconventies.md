# Schrijfconventies

Richtlijnen voor documentatie in de `bron`-repository en verwante tool-repo's
(VSA-tooling). Doel: een lezer **zonder technische scholing** kan met een
concrete vraag het antwoord vinden — in begrijpelijk Nederlands.

**Compleet en begrijpelijk gaat boven compact** — maar *op de juiste plek*.
Tekst inkorten is geen doel; informatie mag verhuizen, niet verdwijnen.

---

## Lezerstest

Per sectie:

1. Welke vraag beantwoordt dit?
2. Staat het antwoord eerst in gewone taal, daarna pas formele tabellen?
3. Zou iemand zonder programmeerachtergrond dit kunnen volgen?

---

## Documentrollen

| Rol                    | Vraag van de lezer                                      | Canonieke plek                                                                 |
| ---------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Org-referentie**     | Wat betekent dit? Wanneer? Wat mag wel/niet?            | `bron/docs/reference/`, `bron/docs/specs/`                                     |
| **Handleiding**        | Hoe doe ik dit, stap voor stap?                         | `bron/docs/manuals/` of tool-guides — waar de handeling thuishoort             |
| **CLI man-page**       | Wat doet dit commando precies? Welke argumenten? I/O?   | Tool-repo (bijv. VSA-tooling `docs/reference/cli/`)                            |
| **Workflow-guide**     | Hoe hangt een keten van stappen samen?                  | Tool-repo guides; verwijst naar CLI man-pages i.p.v. flags te dupliceren       |

Zie [documentatie-eigendom](documentatie-eigendom.md): org-contracten in bron;
tool-CLI en Hugo-build in de tool-repo. **Geen tweede volledige CLI-handleiding
in bron-referentie** — link naar de man-page.

---

## Taal en terminologie

- Schrijf in begrijpelijk Nederlands; vermijd onnodig jargon.
- Gebruik alleen termen die in de glossary staan
  ([terminologie.md](terminologie.md), [glossary](../glossary.md), curated texts in
  `docs/terms/`).
- Bij elke gedefinieerde term: **TermRef** `[term](@)` (in tool-docs voor
  org-termen: `[term](@bron)`) zodat de definitie op de site zichtbaar is.
- Geen synoniemen die verwarring geven (R1–R5).
- **Compact via TermRefs:** als een term in de glossary staat, herhaal de
  definitie niet in de lopende tekst; één TermRef volstaat voor de lezer
  (hover / termpagina).

| Term / frase              | Gebruik                                                                                                                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Conversie**             | Tool met vaste I/O ([`vsa svg`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/svg/), [`vsa musicxml`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/musicxml/)) |
| **Export**                | Hoe een afgeleide in een samenstelling verschijnt (`:::include …`)                                                                                                                                |
| **Kanaal**                | Verouderd — gebruik *conversie* of *exporttype*                                                                                                                                                   |
| **geldige VSA-notatie**   | Voorkeur boven “VSA klopt” / “kloppende VSA” (tool-docs, VSA-tooling)                                                                                                                             |

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

## Handleidingen

- Genummerde stappen; concrete voorbeelden (wat typ je, wat zie je).
- Geen verborgen aannames over mappen of tools.
- Diepe toolcommando’s: korte stap + link naar de CLI man-page; geen tweede
  volledige flag-catalogus.

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

1. Naam / korte samenvatting
2. Synopsis (volledige syntax, optionele delen gemarkeerd)
3. Beschrijving (precies gedrag: input, verwerking, volgorde)
4. Argumenten en opties (naam, verplicht?, type, betekenis, standaard, restricties)
5. Uitvoer (scherm / bestand / directory; waar komt het terecht?)
6. Exitstatus
7. Voorbeelden — goed pad (concrete input + commando + output + bestemmingen)
8. Voorbeelden — foutpad (input + commando + fouttekst + korte oorzaak/oplossing)
9. Zie ook (org-contract, verwante subcommando’s, workflow-guides)

Workflow-guides vatten ketens samen en **verwijzen** naar deze man-pages.

Canonieke `vsa`-CLI: [VSA-tooling CLI-referentie](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/).

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
| Fouten                | Concrete melding, oorzaak, oplossing (op CLI-pagina) |
| TBD                   | Open punten expliciet — geen stilzwijgende aannames  |

Korte alinea’s; genummerde stappen in workflows; admonitions (`!!! note`,
`!!! warning`) voor uitzonderingen.

---

## MkDocs

- Nederlandse prose; code en paden in monospace
- Mermaid-diagrammen voor ketens en pipeline-fases
- `mkdocs build --strict` moet slagen vóór merge
