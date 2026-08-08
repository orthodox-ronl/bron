---
doc_type: org-contract
audience: "P6 — Spec-/PR-reviewer; P4 — Consumer-site builder"
---
# Exportcontracten

Referentie voor **[exportmechanismen](@)** (incl. handmatige siblings) in een
**[samenstelling](@)**.

Export is **geen** [conversie](conversiemechanismen.md): export verwijst naar
reeds gemaakte [afgeleiden](@) (bijv. `.svg`, `.mxl`) of naar handmatige siblings
(`.coria.html`). Conversie staat in [Conversiemechanismen](conversiemechanismen.md).

Authoring-directives worden uitgevoerd door
[VSA-tooling](@);
**normatieve contracten** (wat/wanneer) staan op deze pagina’s.

---

## Export vs. conversie

| Begrip                       | Vraag die het beantwoordt                                  | Voorbeeld                                           |
| ---------------------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| **[Conversiemechanisme](@)** | Hoe maak ik [afgeleide](@) uit `.vsa`?                     | Zie [conversiemechanismen](conversiemechanismen.md) |
| **[Exportmechanisme](@)**    | Hoe verschijnt [afgeleide](@) in de [samenstelling](@)?    | `:::include svg "lied.vsa" alt="…":::`              |

Eén `.vsa`-bron ([vsa-bestand](@)) kan meerdere [exporttypes](@) tegelijk hebben
(SVG embed + Coria-link + MXL-download).

---

## Geregistreerde exporttypes

| Exporttype | Contract                                | Beoogd gebruik                           |
| ---------- | --------------------------------------- | ---------------------------------------- |
| **svg**    | [exporttype-svg](exporttype-svg.md)     | Notatie leesbaar in browser en op papier |
| **coria**  | [exporttype-coria](exporttype-coria.md) | Online oefenen, partij kiezen            |
| **mxl**    | [exporttype-mxl](exporttype-mxl.md)     | Download voor MuseScore / bewerking      |

---

## Authoring-syntax (doel)

Pad is **relatief aan het includerende `.md`-bestand** (niet aan de projectroot).

```markdown
:::include svg "pad/melodie.vsa" alt="Tropaar, toon 3" scale="85%":::
:::include coria "pad/melodie.vsa" label="Oefenen in Coria" mode="auto":::
:::include mxl "pad/melodie.vsa" label="Download MusicXML":::
```

**Catalogus-zoek (sjabloon/sessie)** — `zoek=` tot resolve is gedraaid; daarna
catalogus-pad:

```markdown
:::include svg zoek="Troparion" alt="Troparion" scale="85%":::
:::include coria zoek="Troparion" label="Oefenen in Coria" mode="auto":::
```

Zie [catalogus-samenstelling-zangstuk.md](../specs/catalogus-samenstelling-zangstuk.md)
en
[parochie-lokaal VSA (`zoek=`)](https://orthodox-groningen.github.io/VSA-tooling/guides/parochie-lokaal-vsa/#include-met-zoek-catalogus).
Resolve-commando:
[CLI `vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/).

**Beperking:** `coria` / `mxl` op een **`bron:`** catalogus-pad — het `.vsa` ligt
vaak buiten de content-root; **svg** op `bron:` werkt wel.

### Status van de syntax

| Syntax                                          | Status              | Opmerking                                      |
| ----------------------------------------------- | ------------------- | ---------------------------------------------- |
| `:::include "melodie.vsa"` (zonder exporttype)  | **Geïmplementeerd** | Wordt als VSA-blok naar SVG gerenderd          |
| `:::coria "melodie.vsa"`                        | **Geïmplementeerd** | Alias voor [exporttype](@) `coria`             |
| `:::include svg\|coria\|mxl "…"`                | **Geïmplementeerd** | Pad of catalogus-pad                           |
| `:::include <type> zoek="…"`                    | **Geïmplementeerd** | Resolve vóór build                             |
| `coria` / `mxl` op `bron:` catalogus-pad        | **Beperkt**         | `.vsa` buiten content-root                     |
| `:::include mp3-player`                         | **Gepland**         | [Exporttype](@) nog niet in [VSA-tooling](@)   |

---

## Uitgaveprofielen

Profielen zijn **geen** aparte pipelines. Eén [samenstelling](@); export en CSS
bepalen wat zichtbaar is.

| Profiel       | Typische [exporttypes](@)            | Conversie nodig         |
| ------------- | ------------------------------------ | ----------------------- |
| **Afdruk**    | svg, `keep-together`, `@media print` | svg                     |
| **Online**    | svg, coria, `web-only`               | svg, eventueel musicxml |
| **Bewerking** | mxl-download                         | musicxml                |

Zie [Inhoudslevenscyclus](../specs/inhoudslevenscyclus.md) Deel 3.

---

## Handmatige siblings

| Bestand             | Rol                                                                          |
| ------------------- | ---------------------------------------------------------------------------- |
| `{stem}.coria.html` | Coria-export met vooraf gekozen partij; naast `{stem}.vsa` in content-source |

In de [bron-repository](@) primair VSA + scans; Coria-HTML kan in parochie-content voorkomen.

---

## Gerelateerd

- [Conversiemechanismen](conversiemechanismen.md)
- [Schrijfconventies](../specs/schrijfconventies.md)
- [VSA — directives](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/specification/directives.md)
- [VSA CLI-overzicht](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/)
