# Exportcontracten

Referentie voor **exportmechanismen**: hoe afgeleide (of handmatige siblings) in een
**samenstelling** (Markdown-bundel voor parochie-uitgave) worden ontsloten.

Export is **geen** conversie: export verwijst naar reeds gegenereerde afgeleide
(bijv. `.svg`, `.mxl`) of naar handmatige siblings (`.coria.html`). Conversie
(`vsa svg`, `vsa musicxml`) staat beschreven in
[Conversiemechanismen](conversiemechanismen.md).

Authoring-syntax wordt geïmplementeerd in
[VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/spec-vsa-document-samenstellen.md);
**normatieve contracten** staan op deze pagina’s.

---

## Export vs. conversie

| Begrip        | Vraag die het beantwoordt                     | Voorbeeld                              |
| ------------- | --------------------------------------------- | -------------------------------------- |
| **Conversie** | Hoe maak ik afgeleide uit `.vsa`?             | `vsa svg lied.vsa lied.svg`            |
| **Export**    | Hoe verschijnt afgeleide in de samenstelling? | `:::include svg "lied.vsa" alt="…":::` |

Eén `.vsa`-bron kan meerdere exporttypes tegelijk hebben (SVG embed + Coria-link +
MXL-download).

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

**Catalogus-zoek (sjabloon/sessie)** — `zoek=` tot **`vsa resolve-catalogus`** is gedraaid;
daarna catalogus-pad:

```markdown
:::include svg zoek="Troparion" alt="Troparion" scale="85%":::
:::include coria zoek="Troparion" label="Oefenen in Coria" mode="auto":::
```

Zie [catalogus-samenstelling-zangstuk.md](../specs/catalogus-samenstelling-zangstuk.md),
[VSA — `:::include` met `zoek=`](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/parochie-lokaal-vsa.md#include-met-zoek-catalogus).

**Beperking:** `coria` / `mxl` op **`bron:`** catalogus-pad — `.vsa` ligt vaak buiten
content-root; **svg** op `bron:` werkt wel.

### Huidige implementatie

| Syntax                                         | Status              | Opmerking                                         |
| ---------------------------------------------- | ------------------- | ------------------------------------------------- |
| `:::include "melodie.vsa"` (zonder exporttype) | **Geïmplementeerd** | Wrapt als `::: vsa-notatie`; SVG inline bij build |
| `:::coria "melodie.vsa"`                       | **Geïmplementeerd** | Alias voor exporttype `coria`                     |
| `:::include svg\|coria\|mxl "…"`               | **Geïmplementeerd** | Pad of catalogus-pad                              |
| `:::include <type> zoek="…"`                    | **Geïmplementeerd** | Resolve via `vsa resolve-catalogus` vóór build    |
| `coria` / `mxl` op `bron:` catalogus-pad         | **Beperkt**         | `.vsa` buiten content-root                        |
| `:::include mp3-player`                         | **Gepland**         | Exporttype nog niet in VSA-tooling                |

Voor open `zoek=`: **`vsa resolve-catalogus`** of handmatig **`bron:…`** / **`lokaal:…`**.
Zie [exporttype-coria](exporttype-coria.md) voor Coria-details.

---

## Uitgaveprofielen

Profielen zijn **geen** aparte pipelines. Eén samenstelling; export en CSS bepalen
wat zichtbaar is.

| Profiel       | Typische exporttypes                 | Conversie nodig                |
| ------------- | ------------------------------------ | ------------------------------ |
| **Afdruk**    | svg, `keep-together`, `@media print` | `vsa svg`                      |
| **Online**    | svg, coria, `web-only`               | `vsa svg`, evt. `vsa musicxml` |
| **Bewerking** | mxl-download                         | `vsa musicxml`                 |

Zie [Inhoudslevenscyclus](../specs/inhoudslevenscyclus.md) Deel 3.

---

## Handmatige siblings

| Bestand             | Rol                                                                          |
| ------------------- | ---------------------------------------------------------------------------- |
| `{stem}.coria.html` | Coria-export met vooraf gekozen partij; naast `{stem}.vsa` in content-source |

In de bron-repo primair VSA + scans; Coria-HTML kan in parochie-build content voorkomen.

---

## Gerelateerd

- [Conversiemechanismen](conversiemechanismen.md)
- [Schrijfconventies](../specs/schrijfconventies.md)
- [VSA — document samenstellen](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/spec-vsa-document-samenstellen.md)
