---
doc_type: task-guide
audience: "P5 — Docs-/tool-contributor"
---
# Documentatie bijdragen

Handleiding voor wie **docs** in de [bron-repository](@) (of parallel in
[VSA-tooling](@)) wijzigt: TermRefs, tabellen, lokale builds en wat CI controleert.

## Scripts (bron)

| Script                         | Wanneer                                                                       |
| ------------------------------ | ----------------------------------------------------------------------------- |
| `scripts\docs-serve.cmd`       | Snelle lokale preview **zonder** glossary/TermRef-hover                       |
| `scripts\docs-serve-tev2.cmd`  | Preview **met** TEv2 (zoals CI) — herhaal na term-/TermRef-wijzigingen        |
| `scripts\docs-build.cmd`       | Alleen `mkdocs build --strict` (geen TEv2)                                    |
| `scripts\docs-build-tev2.cmd`  | Volledige keten: TEv2 + TermRef-check + `mkdocs build --strict` (= CI-parity) |

```cmd
cd /d C:\Git\orthodox-groningen\bron
npm install
scripts\docs-serve-tev2.cmd
```

TEv2-tools: pins in root-`package.json` (`@tno-terminology-design/*` **1.2.0**).
Voorkeur: `npm install` (lokaal `node_modules`), niet alleen globale installs.

`docs-serve.cmd` / plain `docs-build.cmd` tonen **geen** opgeloste TermRefs;
gebruik `*-tev2` als je hover of glossary wilt controleren.

## TermRefs

- Org-termen: `[zangstuk](@)` in bron; in [VSA-tooling](@) bij voorkeur `[zangstuk](@bron)`
  tenzij de tool-repo een bewuste lokale herdefinitie heeft.
- Na TRRT mogen geen `[…](@…)`-vormen meer in `generated/docs` staan —
  CI draait `python scripts/check-tev2-termrefs.py generated/docs`.
- Beleid: [schrijfconventies](../specs/schrijfconventies.md) (TermRefs + synoniemen).

## Markdown-tabellen

Kolommen in de bron aligneren (spaties). Bulk:

```cmd
cd /d C:\Git\orthodox-groningen\VSA-tooling
python scripts\align_markdown_tables.py ..\bron\docs\
```

Cursor-regel: `.cursor/rules/markdown-table-layout.mdc`.

## Versie-pins (docs-stack)

| Onderdeel                              | Pin / range              | Bestand                 |
| -------------------------------------- | ------------------------ | ----------------------- |
| MkDocs Material                        | `>=9.5,<10`              | `requirements-docs.txt` |
| git-revision-date plugin               | `>=1.2`                  | `requirements-docs.txt` |
| TEv2 CLI’s (trrt/hrgt/mrgt/mrg-import) | `1.2.0`                  | `package.json`          |

Houd pins gelijk tussen bron en [VSA-tooling](@) tenzij er een bewuste drift-PR is.

## [VSA-tooling](@)

Zelfde scriptnamen; mrg-import is daar standaard (bron-MRG voor `*@bron`).
Zie [TEv2 in tool-docs](https://orthodox-groningen.github.io/VSA-tooling/guides/tev2-docs/).

## Checklist vóór PR

- [ ] `scripts\docs-build-tev2.cmd` groen (of CI `docs-pages` / docs-build)
- [ ] **Type + publiek** benoemd (of evident uit hub/pad): zie
      [schrijfconventies](../specs/schrijfconventies.md) — paginatypen / persona’s
- [ ] **Lezerstest** voor dat type: kan de beoogde lezer in één scan antwoorden op
      *voor wie / wanneer / wat moet ik doen of weten?* (hub = route; task =
      stappen + voorbeeld; term = waartoe; CLI = SYNOPSIS-achtig + foutpad)
- [ ] Nieuwe/gewijzigde termen: curated text + TermRefs waar de term voorkomt
      ([term-sjabloon](../specs/term-entry-sjabloon.md); jargon alleen via glossary)
- [ ] Jargon op de pagina → TermRef of expliciet “niet in glossary” (geen ad-hoc term)
- [ ] Pagina voldoet aan [schrijfconventies](../specs/schrijfconventies.md):
      kopnorm (voor wie / wanneer / antwoord eerst), toon welwillende volwassene
      tenzij docs-/tool-contributor of spec-/PR-reviewer; task/CLI/workflow hebben
      **foutpad**; lezerstekst gebruikt persona-**namen** (geen kale `P3`)
- [ ] Frontmatter waar van toepassing: `doc_type` + `audience` als
      `P3 — Notatie-auteur` (niet alleen `P3`)
- [ ] Nagelezen als de bedoelde lezer: zou iemand zonder voorkennis begrijpen
      wat je bedoelde?- [ ] Tabellen uitgelijnd
- [ ] Geen [afgeleide](@) SVG/MXL in bron committen
