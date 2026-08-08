# Docs-content: publiek, paginatypen en werkplan


| Veld       | Waarde                                                                 |
| ---------- | ---------------------------------------------------------------------- |
| **Status** | voorstel (uitvoering na akkoord)                                       |
| **Repo**   | bron (canoniek) + parallelle taken in VSA-tooling                      |
| **Scope**  | Inhoudelijke geschiktheid van documentatie per publiek en paginatype   |
| **Niet**   | Dark mode, grote IA-herbouw, nieuwe glossary-termen (tenzij drift-fix) |


Dit plan volgt op de docs-professionalisering (H4–H6) en de HRG-TermRef-verbeteringen
op dezelfde feature branch. Het is **niet normatief**. Bij conflict gelden
[schrijfconventies](../specs/schrijfconventies.md), [documentatie-eigendom](../specs/documentatie-eigendom.md)
en de overige specs.

Gerelateerd: [TEv2 TermRef-campagne](tev2-termref-campagne.md) (mechanisch hoverbaar
maken) — dit plan gaat over **wat er geschreven moet staan** en **voor wie**.

---



## 1. Doel

Voor **elke** gepubliceerde pagina (en voor term-entries die via glossary/TermRef
bereikbaar zijn) expliciet maken:

1. **Welk paginatype** het is (niet alleen in welke map het staat).
2. **Welk publiek** primair komt kijken.
3. Welke **taal**, **diepte** en **bouwstenen** (voorbeelden, checklists, links) dat
  publiek nodig heeft.
4. Wat er **nu** schort, en in welke **werkpakketten** we dat verbeteren.

Succes: na uitvoering voldoet een steekproef pagina’s aan de lezerstest uit
schrijfconventies **per type**, zonder de belofte “iedereen zonder technische
scholing” te pretenderen voor contributor-only pagina’s.

---



## 2. Publieken (persona’s)

De sites zijn **geen** koormap of oefensite voor zangers. Dat hard uitspreken
voorkomt teleurstelling op Home/Starten.


| Id     | Persona                       | Typische vraag                                         | Primaire site / sectie                         | Taalbehoefte                                                         |
| ------ | ----------------------------- | ------------------------------------------------------ | ---------------------------------------------- | -------------------------------------------------------------------- |
| **P1** | Parochie-docs-maintainer      | Hoe schrijf ik een sjabloon / `zoek=` / build?         | bron catalogus-handleidingen; VSA consumer/CLI | Volwassen NL, gecontroleerd jargon + TermRefs                        |
| **P2** | Bron-contentbeheerder         | Hoe voeg ik een zangstuk / variant / `access:` toe?    | bron manuals                                   | Stappen + yaml-voorbeeld; weinig aannames                            |
| **P3** | Notatie-auteur                | Hoe schrijf/valideer ik VSA? Wat betekent deze marker? | VSA Starten, guides, syntax, lokale terms      | Eenvoudige taal; Concrete voorbeelden; foutpaden en hoe die te fixen |
| **P4** | Consumer-site builder         | Hoe hang ik Hugo + SVG/CI aan VSA-tooling?             | VSA reuse, svg-export, CLI build-markdown      | Workflow + links naar man-pages; geen flag-dump                      |
| **P5** | Docs-/tool-contributor        | Hoe draait TEv2? Wat is normatief waar?                | docs-bijdragen, tev2-docs, specs               | Expert OK; “alleen voor bijdragers”-label                            |
| **P6** | Spec-/PR-reviewer             | Wat mag wel/niet? Wanneer is iets een afgeleide?       | bron specs + terms + glossary                  | Formeel waar nodig; snelle entry via glossary                        |
| **P7** | Eindgebruiker koor / liturgie | Partituur oefenen, dienst volgen                       | **Niet** deze docs (parochie-site / VSA-demo)  | Doorverwijzen, niet bedienen                                         |


Catalogus-verhalen (Rene/Nana) dekken P1/P2 al relatief goed. P2-how-to’s buiten
catalogus en P3’s eerste uur in VSA zijn de zwakste plekken.

---



## 3. Paginatypen (taxonomy)

Mappen (`manuals/`, `specs/`, …) volgen **eigendom en nav**. Onderstaande typen
sturen **toon en inhoud**. Eén bestand = één type; mengvormen expliciet markeren.


| Type                         | Lezersvraag                                                                                                                                                                                       | Taal                                                        | Jargon                        | Diepte / bouwstenen                                                                                                     | Voorbeelden van plekken                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Wayfinding hub**           | Waar moet ik zijn?                                                                                                                                                                                | Kort, volwassen                                             | TermRefs spaarzaam            | Persona-routes; “wanneer”; wat *niet* hier staat                                                                        | `index.md`, sectie-indexen                                     |
| **Onboarding**               | Hoe begin ik *hier*?                                                                                                                                                                              | Volwassen; minimale jargonbrug                              | Uitleg bij eerste jargon      | Genummerde stappen; succescriterium; “klaar als…”                                                                       | `getting-started/`                                             |
| **Task guide**               | Hoe doe ik taak X?                                                                                                                                                                                | Stappen-NL                                                  | TermRefs i.p.v. herdefiniëren | Voorbeeldinput; verwacht resultaat; checklist; link naar norm; foutidentificatie en oplossen                            | `zangstuk-toevoegen`, copyright, bronvariant                   |
| **User story / walkthrough** | Hoe doet persona Y dit end-to-end?                                                                                                                                                                | Narratief, volwassen taal zonder nodeloos moeilijke woorden | Gecontroleerd                 | Doelbeeld vs “werkt nu”; concrete ids/paden; statusbadge                                                                | `manuals/catalogus/`*                                          |
| **Normative spec**           | Wat is de regel?                                                                                                                                                                                  | Formeel mag                                                 | Canonieke termen              | Criteria; R-regels; optioneel “snelle uitleg”-box bovenaan                                                              | `specs/terminologie.md`, `zangstuk-formaat.md`                 |
| **Org-contract**             | Wat/wanneer mag deze export/conversie?                                                                                                                                                            | Volwassen + tabellen                                        | TermRefs                      | Waartoe → wel/niet → parameters → problemen → CLI-brug (schrijfconventies)                                              | `reference/exporttype-`*, `conversie-*`                        |
| **CLI man-page**             | Waartoe dient het commando, en wat doet het dan precies?                                                                                                                                          | Precies, beknopt                                            | Tooljargon OK                 | Synopsis, I/O, exit, goed+fout voorbeeld (schrijfconventies), oplossen van fouten                                       | VSA `reference/cli/`*; bron `catalogus-cli` (splitsbaar)       |
| **Workflow-guide**           | Hoe hangt een keten samen? Waarvoor gebruik je de workflow? Waartoe dient hij?                                                                                                                    | Volwassen                                                   | Links, geen flag-catalogus    | Wanneer wel/niet; 2–3 commandopaden; diagnose; zie man-pages + org-contract                                             | VSA `svg-export.md` (sjabloon); validation inkorten/verbeteren |
| **Term entry (curated)**     | Wat betekent dit begrip? Waartoe bestaat het begrip (wat kun je ermee wat je zonder niet kan?) Wat zijn gerelateerde onderwerpen? Waar kan ik er verder over lezen (liefst in de body natuurlijk) | Definitie kort; body motiverend                             | Alleen glossary-termen        | `glossaryText` + Notes + Ja/Nee + Motivatie (**waartoe**) + gerelateerd + verder lezen + link §N; **geen herdefinitie** | `docs/terms/`*, VSA `terminologie/*`                           |
| **Generated glossary**       | Overzicht + hover                                                                                                                                                                                 | Shelltekst volwassen                                        | —                             | Verschil glossary / termpagina / terminologie-spec uitleggen                                                            | `glossary.md`                                                  |
| **Integratie / ownership**   | Waar hoort welke repo?                                                                                                                                                                            | Volwassen                                                   | Licht                         | Rollen, minimale keten, geen tweede handleiding                                                                         | `consumer-site`, documentatie-eigendom                         |
| **Non-normative plan**       | Wat overwegen we?                                                                                                                                                                                 | Vrij                                                        | —                             | Statusbanner; geen conflict met specs                                                                                   | `docs/plans/`*                                                 |




### Taalrichtlijnen per type (samenvatting)

- **Geen Jip-en-Janneke** op specs/CLI — wel op hubs, task guides, onboarding en
  P3-gerichte workflow-guides: eerst de vraag in gewone (eenvoudige) taal, daarna
  formele details. Doeltoon: **welwillende volwassenen**, geen techneuten aannemen
  tenzij het type expert is (P5/P6).
- **Jargon**: alleen glossary-termen; altijd TermRef waar de term al bestaat. Is
  jargon nodig of nuttig en ontbreekt de term nog → eerst curated text
  (`docs/terms/` of VSA `terminologie/`) + glossary-entry, daarna TermRef bij gebruik.
  Geen ad-hoc jargon in lopende tekst.
- **Fouten**: task guides, CLI man-pages en workflow-guides tonen niet alleen het
  goedepad, maar **fout herkennen én oplossen** (concrete melding → oorzaak → fix).
- **Term entries**: beantwoorden ook *waartoe* het begrip bestaat, *gerelateerde*
  begrippen, en *waar verder te lezen* (bij voorkeur in de body).
- **Expertpagina’s (P5/P6)**: mogen dicht zijn, mits bovenaan staat *voor wie* en
  *wanneer niet lezen*.

---



## 4. Evaluatie huidige documentatie (kernbevindingen)

Gebaseerd op een steekproef van volledige pagina’s in bron en VSA-tooling (augustus 2026).

### Wat al goed werkt

- **Catalogus-verhalen** (P1): persona’s, “wanneer”, eerlijk over GUI vs CLI.
- **Org-contracten** export/conversie: volgen schrijfconventies-opbouw.
- **VSA CLI man-pages** en **svg-export**-guide: referentiekwaliteit; geen flag-dump.
- **Indexen** met “wanneer”-kolom (bron manuals): herbruikbaar patroon.
- **Scheiding bron ↔ tool** op Home’s grotendeels helder.



### Spanningsveld

`schrijfconventies` belooft een lezer **zonder technische scholing**. De sites zijn
in de praktijk vooral **bijdragers-/beheerdersdocumentatie**. Oplossing: belofte
**per type/publiek** aanscherpen in schrijfconventies (fase A), niet alles infantiliseren, maar wel rekening houden met gebruikers die doorgaans geen techneut zijn, en dus wel bij de hand genomen moeten worden (welwillende volwassenen).

### Prioritaire inhoudelijke gaten


| Prio | Bevinding                                                                                                   | Publiek | Type                |
| ---- | ----------------------------------------------------------------------------------------------------------- | ------- | ------------------- |
| P0   | VSA: `050_svg_demo.vsa` als **succes**-voorbeeld voor `vsa validate` terwijl validate faalt                 | P3      | Onboarding / guides |
| P1   | `terms/representatie.md`: spreektaal, typo, spanning met `terminologie` §8 (SVG als representatie?)         | P6/P2   | Term entry          |
| P1   | Korte how-to’s (`zangstuk-toevoegen`, `copyright-access`) te cryptisch: geen yaml-voorbeeld, “workflow 9.1” | P2      | Task guide          |
| P1   | Home/Starten: geen persona-router; geen “geen koorzanger-site”                                              | allen   | Hub / onboarding    |
| P2   | Nav-verwarring “Terminologie” (glossary) vs “Terminologie” (spec)                                           | allen   | Hub                 |
| P2   | Driedubbele definities terms / glossary / `terminologie.md` → drift-risico                                  | P6      | Term + spec         |
| P2   | Twee authoring-werelden (`:::include` pad vs `zoek=`) zonder brug                                           | P1/P4   | Hub / contract      |
| P2   | VSA: duale hubs (`manuals/index` vs `guides/README` vs brede user-guide)                                    | P3/P4   | Hub                 |
| P2   | Spec-overview VSA: eigen termtabel naast glossary; “Export”-woordgebruik                                    | P5      | Spec hub            |
| P3   | Dunne term-bodies (`zangstuk.md`); contributor-pages zonder “minimaal pad”                                  | P2/P5   | Term / task         |
| P3   | TermRef-dekking op specs/reference (zie apart plan)                                                         | allen   | Cross-cutting       |




### Illustratie toonprobleem

Slechte entry (`representatie.md`): lange MuseScore/Coria-monoloog zonder Ja/Nee-tabel,
terwijl glossaryText kort en formeel is — lezer krijgt twee werelden.

Goede entry (`afgeleide.md` / exportcontracten): korte definitie, Notes, Ja/Nee,
Motivatie, link naar canonieke § — dat is het sjabloon.

---



## 5. Norm: wat elke pagina bovenaan moet hebben

Voorstel (fase A vastleggen in schrijfconventies; daarna pagina’s bijwerken):

1. **Voor wie** (één zin of admonition).
2. **Wanneer lees je dit** (en wanneer *niet* — link naar het juiste type).
3. **Antwoord eerst** (1–3 zinnen), daarna diepte.
4. **Zie ook** onderaan (gerelateerde types: how-to ↔ spec ↔ CLI ↔ term).

Optioneel later: YAML-frontmatter `doc_type` / `audience` voor review-checklists
(niet verplicht voor MkDocs-nav).

---

## 5a. Landingsgarantie (plan → canonieke plek)

Dit plan is **niet** de blijvende bron van schrijfregels. Eisen die elders horen,
moeten daar **landen** voordat de bijbehorende content-PR’s “klaar” mogen heten.
Zonder landingsbewijs blijft de eis open — ook als hij al in dit plan staat.

### Regel

1. Elke eis heeft precies één **canonieke bestemming** (tabel hieronder).
2. De fase-PR die die bestemming wijzigt, vermeldt in de PR-body:
   `Landing: <pad> ← <eis-id of korte naam>`.
3. Fase A (of de eerste PR die een norm wijzigt) is **niet mergebaar** zolang een
   rij in de landingsmatrix met status “moet in A” nog ontbreekt in de diff.
4. Latere fasen (B–E) toetsen tegen de **gelande** tekst in schrijfconventies /
   checklist — niet tegen dit plan alleen.
5. Als een eis bewust uitgesteld wordt: rij status `uitgesteld` + issue/PR-link;
   geen stille weglating.

### Landingsmatrix


| Eis (uit dit plan)                                          | Canonieke bestemming                                                                        | Landt in fase                 | Bewijs in PR                                    | Status        |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----------------------------- | ----------------------------------------------- | ------------- |
| Persona’s P1–P7 + paginatypen + toon welwillende volwassene | `bron/docs/specs/schrijfconventies.md`                                                      | **A.1**                       | Diff + sectiekop in schrijfconventies           | gedaan        |
| Jargon → curated text + TermRef                             | idem (+ korte vermelding in `documentatie-eigendom` of terms-index indien nodig)            | **A.1**                       | Diff schrijfconventies                          | gedaan        |
| Foutpad-eis (task / CLI / workflow)                         | `schrijfconventies.md` (rollen CLI/workflow/handleiding)                                    | **A.1**                       | Diff                                            | gedaan        |
| Pagina-kopnorm (voor wie / wanneer / antwoord eerst)        | `schrijfconventies.md`                                                                      | **A.1**                       | Diff; dekt §5 van dit plan                      | gedaan        |
| Term-entry-sjabloon (waartoe / gerelateerd / verder lezen)  | `schrijfconventies.md` **of** `bron/docs/terms/README.md` (nieuw)                           | **A.2**                       | Bestand bestaat + link vanuit schrijfconventies | gedaan        |
| Review-checklist voor contributors                          | `bron/docs/manuals/docs-bijdragen.md` (+ VSA `guides/tev2-docs.md` of manuals indien nodig) | **E.1** (mag met A meeliften) | Checklist-sectie in diff                        | gedaan (bron) |
| Nav “Begrippenlijst” (indien akkoord §8.1)                  | `bron/mkdocs.yml` + `glossary.md` shell                                                     | **A.3**                       | Diff                                            | uitgesteld    |
| Agent/contributor-reminder (niet normatief)                 | Korte pointer in `bron/AGENTS.md` en/of VSA `AGENTS.md` → schrijfconventies                 | **A** of **E.1**              | Diff; geen tweede normtekst                     | gedaan (bron) |
| VSA-specifieke uitvoering                                   | Bestanden in VSA-tooling (fase 0 / D / B.4); pointer-plan blijft stub                       | **0 / D / B.4**               | PR in VSA-repo                                  | 0 gedaan      |

Nieuwe eisen die tijdens uitvoering opduiken: **eerst** rij toevoegen aan deze
matrix (of direct in schrijfconventies landen), **daarna** content wijzigen.

### Definition of Done per fase-PR

- [x] Landingsmatrix-rijen voor fase A: gedaan of uitgesteld (A.3 wacht §8.1).
- [x] Geen “alleen in het plan”-norm meer die al in A had moeten landen (behalve A.3).
- [ ] Content-PR’s na A citeren schrijfconventies (of term-sjabloon), niet dit plan,
      als acceptatiebron.

### Wat dit *niet* garandeert

Automatische CI die toon of “welwillende volwassene” afdwingt bestaat niet.
De garantie is **proces + review**: matrix + verplichte `Landing:`-regel in de
PR + checklist in docs-bijdragen. Optioneel later: litmus-test in review
(één vraag per type uit de lezerstest).

---



## 6. Werkplan (uitvoering na akkoord)



### Fase 0 — Juistheid (VSA-tooling, snel) — **gedaan** (2026-08-08)


| #   | Taak                                                                                                     | Acceptatie                               | Status   |
| --- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------- |
| 0.1 | Vervang succes-`validate` op Home/Starten/validation/cli-taken/user-guide door bestand dat echt OK geeft | Geen pad claimt succes op `050_svg_demo` | gedaan   |
| 0.2 | Houd `050_svg_demo` alleen bij svg/parse met bestaande waarschuwing                                      | validate.md en svg.md blijven consistent | gedaan   |

Succespad overal: `examples\minimal\001_plain_text.vsa`. `050_svg_demo.vsa` blijft
bij svg/parse/musicxml en als **faalvoorbeeld** in `reference/cli/validate.md`.




### Fase A — Kaders aanscherpen (bron) — **gedaan** (2026-08-08), A.3 uitgesteld


| #   | Taak                                                                                                                                                                               | Acceptatie                                                                                 | Status                          |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------- |
| A.1 | Schrijfconventies: persona’s P1–P7 + paginatypen-tabel + belofte “welwillende volwassenen” per type; jargon→curated+TermRef; foutpad-eis voor task/CLI/workflow; pagina-kopnorm §5 | Diff `schrijfconventies.md`; PR-body `Landing:`-regels voor matrix-rijen A.1; D1–D4 intact | gedaan                          |
| A.2 | Term-entry-sjabloon: glossaryText / Notes / Ja-Nee / Motivatie (**waartoe**) / gerelateerd / verder lezen / §-link                                                                 | Bestand of sectie bestaat; link vanuit schrijfconventies; `Landing: A.2`                   | gedaan (`docs/terms/README.md`) |
| A.3 | Nav-label glossary: bijv. “Begrippenlijst” i.p.v. tweede “Terminologie” (alleen na akkoord §8.1)                                                                                   | mkdocs.yml + glossary-shelltekst; of rij `uitgesteld`                                      | **uitgesteld** (wacht §8.1)     |

**Landing (fase A):**

- `Landing: docs/specs/schrijfconventies.md` ← persona’s, paginatypen, toon, jargon, foutpad, kopnorm
- `Landing: docs/terms/README.md` ← term-entry-sjabloon (+ link vanuit schrijfconventies)
- `Landing: docs/manuals/docs-bijdragen.md` ← review-checklist (E.1 meegelift)
- `Landing: AGENTS.md` ← pointer (geen tweede normtekst)
- A.3: uitgesteld tot akkoord open vraag §8.1




### Fase B — Term entries (bron, daarna VSA-lokaal)


| #   | Taak                                                                                                                           | Acceptatie                                                                 |
| --- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| B.1 | Herschrijf `representatie.md` naar sjabloon (incl. waartoe / gerelateerd / verder lezen); align `terminologie` §8; fix typo    | Geen drift glossaryText ↔ §8 ↔ body; A.2-sjabloon compleet                 |
| B.2 | Verrijk `zangstuk.md` (Ja/Nee + Notes + waartoe/gerelateerd)                                                                   | Zelfde structuur als `afgeleide.md` / A.2                                  |
| B.3 | Steekproef overige `docs/terms/*`: body herdefinieert niet; Notes zonder self-TermRef; ontbrekend “waartoe” aanvullen waar dun | Checklist in PR                                                            |
| B.4 | VSA curated: dunne bodies + 1 voorbeeld + “verder lezen”; expliciet `@bron` waar org-term bedoeld is                           | tev2-docs / contributor-note                                               |




### Fase C — Task guides & hubs (bron)


| #   | Taak                                                                                                                  | Acceptatie                                                         |
| --- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| C.1 | `zangstuk-toevoegen`: yaml-voorbeeld, mapboom, “wanneer”, verwacht resultaat; “9.1” weg/uitleg; typische fouten + fix | P2 kan zonder spec-diepte starten; foutpad aanwezig                |
| C.2 | `copyright-access` + `bronvariant-toevoegen`: yaml-voorbeeld + checklist + foutpad                                    | Idem                                                               |
| C.3 | Home + Starten: persona-router; “geen P7”; subtitel Starten = lokaal ontwikkelen; toon welwillende volwassene         | Eerste scherm beantwoordt “wie ben ik?”                            |
| C.4 | Brugtekst pad-`:::include` vs catalogus-`zoek=` op exporttype-svg én catalogus-index                                  | Beide werelden genoemd met links                                   |




### Fase D — VSA leesbaarheid & hubs


| #   | Taak                                                                                           | Acceptatie                                                                 |
| --- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| D.1 | Eén hub: `manuals/index`; `guides/README` → stub/exclude                                       | Geen tweede startpunt                                                      |
| D.2 | User-guide inkorten tot tour + links (geen tweede CLI); eenvoudige taal waar P3 meekijkt       | Flags alleen in `reference/cli/`                                           |
| D.3 | Validatie-guide naar niveau svg-export: waartoe/wanneer, validate≠svg, diagnose + fix          | Zelfde sectiestructuur; foutpad concreet                                   |
| D.4 | Spec `overview.md`: termtabel → glossary; Export/conversie-woordgebruik; sectienummers         | Geen parallelle glossary                                                   |
| D.5 | Consumer-site: “pointer-only” of minimale end-to-end                                           | Titel dekt lading                                                          |
| D.6 | Nav-titels NL waar nu Engels (`Conformance`, …)                                                | Consistente NL-nav                                                         |
| D.7 | CLI man-pages steekproef: “waartoe” bovenaan + foutvoorbeeld met oplossing (schrijfconventies) | Min. validate + svg voldoen; overige in backlog noteren                    |




### Fase E — Cross-cutting (na of parallel met TermRef-campagne)


| #   | Taak                                                                                                          | Acceptatie                                            |
| --- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| E.1 | Review-checklist in docs-bijdragen: type, publiek, lezerstest, jargon→TermRef/curated, foutpad waar verplicht | Contributors weten waarop te toetsen                  |
| E.2 | TermRef-campagne op specs/reference/dunne manuals; bij ontbrekend jargon: term eerst curaten                  | Zie [tev2-termref-campagne](tev2-termref-campagne.md) |
| E.3 | Optioneel: `catalogus-cli` splitsen gebruikers-CLI vs library                                                 | Schrijfconventies man-page-vorm                       |




### Voorgestelde volgorde

```text
0 (VSA juistheid) → A (kaders) → B1–B2 (representatie/zangstuk)
  → C (how-to’s + hubs bron) → D (VSA hubs) → B3–B4 + E
```

Elke fase = eigen PR(s); geen mengeling met ongerelateerde features.

---



## 7. Acceptatiecriteria (programma)

- [x] Schrijfconventies noemen persona’s en paginatypen; toon **welwillende
      volwassenen** (geen techneut aannemen) op hubs/task guides/onboarding/P3-workflows;
      expertpagina’s mogen dichter met duidelijk “voor wie”.
- [x] Jargon-regel staat in schrijfconventies: nodig jargon → curated text + TermRef.
- [x] P0-demo-bug in VSA is weg.
- [ ] `representatie` en `zangstuk` term-entries volgen sjabloon (incl. waartoe /
      gerelateerd / verder lezen) en matchen de spec.
- [ ] Kern-task-guides P2 hebben voorbeeld + checklist + “wanneer” + foutpad.
- [ ] Home (bron + VSA) routeren op persona en benoemen P7-niet-hier.
- [ ] Geen tweede docs-hub in VSA-guides-README.
- [ ] Steekproef (min. 1 pagina per type) doorstaat de lezerstest voor dat type.
- [ ] Landingsmatrix §5a: alle “moet in A”-rijen geland of expliciet uitgesteld;
      latere fasen toetsen tegen schrijfconventies, niet alleen tegen dit plan.

---



## 8. Open vragen voor akkoord

1. **Nav-hernoaming** glossary → “Begrippenlijst”: akkoord, of liever “Glossary” houden?
2. **Schrijfconventies aanscherpen** (fase A) vóór pagina-rewrites, of parallel met B1?
   → **Beslist door uitvoering:** A eerst (nu gedaan); B volgt.
3. **User-guide VSA**: inkorten (D.2) of tijdelijk `not_in_nav` / archief?
4. **Frontmatter `doc_type` / `audience`**: nu meenemen, of alleen checklist in prose?
5. Scope **alleen bron** eerst, of bron+VSA in één programma met gescheiden PR’s
  (aanbevolen: gescheiden PR’s, één programmaplan = dit document)?

---



## 9. Wijzigingslog


| Datum      | Wijziging                                                                                                                          |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 2026-08-08 | Eerste voorstel na content-audit bron + VSA                                                                                        |
| 2026-08-08 | Aanvullingen (P3-taal, waartoe, foutpaden, jargon→curated, welwillende volwassenen) doorgewerkt in §3-richtlijnen, fasen A–E en §7 |
| 2026-08-08 | §5a Landingsgarantie: matrix plan→canonieke plek + PR DoD `Landing:`                                                               |
| 2026-08-08 | Fase 0 gedaan (VSA): succes-`validate` → `001_plain_text.vsa`                                                                      |
| 2026-08-08 | Fase A gedaan: schrijfconventies + `terms/README.md` + checklist/AGENTS; A.3 uitgesteld (§8.1)                                     |


