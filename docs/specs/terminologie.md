---
doc_type: normative-spec
audience: "P6 — Spec-/PR-reviewer; P2 — Bron-contentbeheerder"
---

# Zangstukmodel — niveaus, criteria en samenhang

**Status:** normatief, goedgekeurd (juni 2026).

**Canonieke locatie:** dit bestand (`bron/docs/specs/terminologie.md`). **Niet dupliceren** in andere repo's — link ernaar (zie [documentatie-eigendom.md](documentatie-eigendom.md)).

**Rol:** dit document beschrijft het **vier-niveaumodel** en de **samenhang** tussen
begrippen (criteria, verboden paden, disambiguatie). De korte definitie per term,
plus samenhang *vanuit die term*, staat in curated texts onder `docs/terms/`
(mensleesbaar overzicht: [Begrippenlijst](../glossary.md)).

Gerelateerd: [parochie-lokaal zangstukken](../manuals/parochie-lokaal-zangstukken.md), [zangstuk-identificatie.md](zangstuk-identificatie.md) (beknopte index).

**Id-velden:** `zangstuk-id`, `variant-id`, `uitvoeringsvorm-id`, `representatie-id`.

---

## 0. Gebruiksregels (alle repo’s `orthodox-groningen`)

Deze glossary is **bindend** voor documentatie, metadata, code-commentaar, issues, PR-beschrijvingen en user-facing teksten in alle repository’s van [github.com/orthodox-groningen](https://github.com/orthodox-groningen).

| Regel                                  | Inhoud                                                                                                                                                                        |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **R1 — gedefinieerde term**            | Komt een term uit deze glossary voor in een repo, dan **moet** ze gebruikt worden in **precies** de hier gedefinieerde betekenis. Geen andere betekenis “erbij plakken”.      |
| **R2 — concept met term**              | Bedoel je inhoudelijk iets waarvoor deze glossary een term heeft, dan **moet** je die term gebruiken (niet een gangbaar synoniem dat verwarring geeft — zie § gangbare taal). |
| **R3 — geen nieuwe termen ad hoc**     | Nieuwe precieze termen of gewijzigde definities **alleen** via wijziging van dit document (PR op `bron`, daarna spiegels bijwerken).                                          |
| **R4 — gangbare taal expliciet maken** | In user-facing tekst mag gangbaar Nederlands, mits de **eerste** keer of in een gloss-link de precieze term genoemd wordt waar misverstand dreigt.                            |
| **R5 — ids canoniek**                  | In opslag, paden en machine-leesbare referenties: canonieke ids (`§ canonieke id’s`); aliassen alleen op de invoergrens.                                                      |

**Review:** bij PR's die metadata, zangstuk-structuur of docs raken: controleer R1–R2. **Implementatie** van automatische terminologie-lint: open (fase 2).

**Andere repo's:** link naar dit document; geen volledige kopieën (stubs met link zijn oké — zie [documentatie-eigendom.md](documentatie-eigendom.md)).

---

## 1. Vier niveaus (overzicht)

**[Zangstuk](@) → [variant](@) → [uitvoeringsvorm](@) → [representatie](@) (0..n)**

| Niveau | Term                     | Id                   | Uniciteit                                                   | Typisch in git  |
| ------ | ------------------------ | -------------------- | ----------------------------------------------------------- | --------------- |
| 0      | **[Zangstuk](@)**        | `zangstuk-id`        | —                                                           | metadata        |
| 1      | **[Variant](@)**         | `variant-id`         | max. 1× per `zangstuk-id`                                   | metadata        |
| 2      | **[Uitvoeringsvorm](@)** | `uitvoeringsvorm-id` | max. 1× per `(zangstuk-id, variant-id)`                     | metadata        |
| 3      | **[Representatie](@)**   | `representatie-id`   | max. 1× per `(zangstuk-id, variant-id, uitvoeringsvorm-id)` | `.vsa`, scan, … |

Volledig pad (canoniek): `(zangstuk-id, variant-id, uitvoeringsvorm-id, representatie-id)`.

- Geen default-id’s (geen `variant-id: standaard`).
- **0 representaties:** [uitvoeringsvorm](@) bestaat ([herkomst](@) bekend) zonder [bronbestand](@).

### Voorbeeldhiërarchie

**Cherubijnenhymne (meerdere varianten):**

```text
zangstuk: cherubijnenhymne
├── variant: kastorski
│   └── uitvoeringsvorm: koormap-15c
│       ├── representatie: scan-koormap-034-ru
│       └── representatie: scan-koormap-034-nl
├── variant: obikhod
│   └── uitvoeringsvorm: …
└── variant: grieks-byzantijns
    └── uitvoeringsvorm: …
```

**1e antifoon weekdagen (één variant, meerdere uitvoeringsvormen):**

```text
zangstuk: antifoon-1-weekdagen
└── variant: liturgikon-weekdagen
    ├── uitvoeringsvorm: liturgikon
    ├── uitvoeringsvorm: groningen
    │   └── representatie: groningen
    └── uitvoeringsvorm: hemelum
        └── representatie: hemelum
```

---

## 2. Canonieke id’s en aliassen

### 2.1 Canonieke id-vorm

Elk canoniek id voldoet aan: `^[a-z0-9_-]+$` (lowercase ASCII, cijfers, `-`, `_`).

- Geen spaties, hoofdletters, diacritica of Cyrillisch in het **opgeslagen** canonieke id.
- Meertalige of gemixte spelling → **aliassen**, niet in het canonieke id.
- Resolver normaliseert invoer naar lowercase; ongeldige tekens → **fout** (geen stille transliteratie tenzij later expliciet gespecificeerd).

### 2.2 Aliassen

| Concept              | Canoniek             | Aliassen (voorbeelden)                       |
| -------------------- | -------------------- | -------------------------------------------- |
| [Zangstuk](@)        | `zangstuk-id`        | “1e antifoon weekdagen”, “8a”, koormap-label |
| [Variant](@)         | `variant-id`         | “Kastorski”, “obikhod”, `greek-chant`        |
| [Uitvoeringsvorm](@) | `uitvoeringsvorm-id` | “Groningen”, “refrein-praktijk”, “Hemelum”   |
| [Representatie](@)   | `representatie-id`   | scan-bestandsnaam, parochie-label            |

### 2.3 Twee lagen: opslag vs invoer

| Laag                   | Regel                                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| **Opslag / techniek**  | Paden, yaml, git, `bron:…`-referenties, build-artefacten: **altijd canoniek id** (lowercase). |
| **Invoer / gebruiker** | Zoeken, specs, UI, CLI: **alias toegestaan** → resolver zet om vóór validate/build/opslag.    |

Gebruikers hoeven het canonieke id **niet** te kennen als hun alias geregistreerd en binnen scope **eenduidig** is.

### 2.4 Case-insensitive matching

- Vergelijking invoer ↔ canoniek id en invoer ↔ alias: **case-insensitive** (Unicode case-folding).
- Voorbeeld: `Groningen`, `groningen`, `GRONINGEN` → `uitvoeringsvorm-id` `groningen`.
- Aliassen mogen willekeurige casing hebben; **canoniek id in opslag** blijft `[a-z0-9_-]+`.

### 2.5 Meertalige aliassen

- Aliassen in elke relevante taal (NL, EN, RU, Kerk-Slavisch, …); optioneel `lang` (BCP 47).
- Geen automatische machinevertaling — elke taalvariant apart registreren.

Voorbeeld [variant](@) `kastorski` onder `cherubijnenhymne`:

```yaml
aliases:
  - { text: "Kastorski", lang: en }
  - { text: "Kastorski", lang: nl }
  - { text: "Касторский", lang: ru }
  - { text: "koormap 15c" }
  - { text: "15c" }
```

### 2.6 Scope en uniciteit aliassen

| Niveau               | Alias uniek binnen                                  |
| -------------------- | --------------------------------------------------- |
| [Zangstuk](@)        | globale catalogus (bron-index)                      |
| [Variant](@)         | één `zangstuk-id`                                   |
| [Uitvoeringsvorm](@) | één `(zangstuk-id, variant-id)`                     |
| [Representatie](@)   | één `(zangstuk-id, variant-id, uitvoeringsvorm-id)` |

Een alias mag **niet** binnen dezelfde scope op twee verschillende entiteiten wijzen.

### 2.7 Ambiguïteit

Meerdere matches na normalisatie → **fout** met kandidaten (canoniek id + context). Geen stille disambiguatie.

### 2.8 Alias-resolver (contract)

1. Normaliseer invoer (trim; case-fold voor matching).
2. Match canoniek id of alias binnen scope → **canoniek id** (lowercase `[a-z0-9_-]+`).
3. Geen match → fout; meerdere matches → ambiguïteitsfout.

| Context       | Voorbeeld invoer               | Na resolutie (opslag)  |
| ------------- | ------------------------------ | ---------------------- |
| CLI           | `--uitvoeringsvorm Groningen`  | `groningen`            |
| CLI           | `--variant касторский` (alias) | `kastorski`            |
| Yaml (invoer) | `uitvoeringsvorm-id: Hemelum`  | `hemelum`              |
| Zoek-UI       | “eerste antifoon weekdagen”    | `antifoon-1-weekdagen` |

**Implementatiestatus:** contract gedocumenteerd; resolver in **catalogus**-tool (bron-repo, fase 2 basis).

---

## 3. Gangbare taal vs precieze termen

Leesvorm: “*gangbaar* noemen wij *precieze term*, niet verwarren met *…*.”

| Gangbaar                                     | Noemen wij                                     | Niet verwarren met                                     |
| -------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------ |
| “Cherubijnenhymne” (verschillende melodieën) | **[variant](@)**                               | [uitvoeringsvorm](@), [representatie](@)               |
| “cover” / parochiepraktijk                   | **[uitvoeringsvorm](@)**                       | [variant](@), [representatie](@)                       |
| scan, `.vsa`, notatie                        | **[representatie](@)**                         | [uitvoeringsvorm](@), [variant](@)                     |
| werknaam in invoer                           | **[alias](@)** → resolver                      | canoniek id in opslag                                  |
| “bron van …” (waar vandaan)                  | **[herkomst](@)**                              | [bronbestand](@), [bron-repository](@)                 |
| “bron” (bestand)                             | **[bronbestand](@)**                           | [bron-repository](@)                                   |
| “bron” (repo)                                | **[bron-repository](@)**                       | [bronbestand](@)                                       |
| “bronvariant” (informeel)                    | **[source](@)-entry** / **[representatie](@)** | [uitvoeringsvorm](@)                                   |
| “metadata-yaml”, “config” in zangstuk-map    | **[manifest](@)**                              | npm-/package-manifest, build-manifest, `zangstuk.yaml` |

---

## 4. `based_on`

| Van                  | Naar                                         | Voorbeeld                                  |
| -------------------- | -------------------------------------------- | ------------------------------------------ |
| [Variant](@)         | andere variant, zelfde zangstuk              | zeldzaam; met onderbouwing                 |
| [Uitvoeringsvorm](@) | andere uitvoeringsvorm, zelfde variant       | `groningen` based_on `liturgikon`          |
| [Representatie](@)   | andere representatie, zelfde uitvoeringsvorm | VSA-transcriptie based_on scan             |
| [Representatie](@)   | repr. onder andere uitvoeringsvorm           | alleen mét uitvoeringsvorm `based_on` peer |

**Verboden:** [representatie](@) → [variant](@)/[zangstuk](@) (direct); [uitvoeringsvorm](@) → [representatie](@); [variant](@) → [uitvoeringsvorm](@)/[representatie](@).

---

## 5. Zangstuk

**Criterium:** Entiteit E is een [zangstuk](@) dan en slechts dan als E een liturgisch-muzikaal geheel identificeert met stabiele **`zangstuk-id`**, waarbij onder E nul of meer [varianten](@) (§6) bestaan.

**Toelichting:** Antwoord op “welk stuk in de liturgie?” (bijv. “1e antifoon weekdagen”, “Cherubijnenhymne”).

|               | Voorbeeld                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------- |
| **Ja**        | `antifoon-1-weekdagen`, `cherubijnenhymne`, `troparion-zondag-toon-1`                     |
| **Nee**       | `groningen.vsa` ([bronbestand](@)); `zondag-toon-1.md` ([samenstelling](@)); SVG na build |
| **Randgeval** | Werknamen vóór registratie → afstemmen bij [promotie](@); daarna canoniek `zangstuk-id`   |

---

## 6. Variant

**Criterium:** V is een [variant](@) onder [zangstuk](@) Z dan en slechts dan als:

1. V **dezelfde liturgische functie** vervult als andere [varianten](@) onder Z (zelfde liturgische rol/plaats), **en**
2. een correcte uitvoering (middels een bijbehorende [uitvoeringsvorm](@)/[representatie](@)) van V **wezenlijk anders klinkt** dan een correcte uitvoering van een andere variant onder Z — niet uitsluitend door uitvoerders (§7).

|               | Voorbeeld                                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------------ |
| **Ja**        | `kastorski` vs `obikhod` onder `cherubijnenhymne`; verschillende melodische lijnen, zelfde liturgische tekst |
| **Nee**       | `groningen` vs `liturgikon` als **[uitvoeringsvormen](@)** onder dezelfde [variant](@) (§7), geen varianten  |
| **Nee**       | Zelfde `.vsa`, ander koor → geen [variant](@)                                                                |
| **Randgeval** | Catalogiseer-beleid bepaalt `variant-id`-waarde; inhoudelijk criterium blijft §6                             |

---

## 7. Uitvoeringsvorm

**Criterium:** U is een [uitvoeringsvorm](@) onder [variant](@) V dan en slechts dan als er tenminste één [representatie](@) R van U bestaat die beschrijft **wat je hoort** bij correct uitvoeren van V.

**Operationele test:** Twee [representaties](@) R en R' betreffen dezelfde [uitvoeringsvorm](@) U als ze dezelfde melodielijn en tekst beschrijven (een verschil tussen de 'do context' of tempo is hierbij niet van belang). Als R en R' dus in hetzelfde tempo en met dezelfde do-context worden gehoord, klinkt dat goed. Als ze grotendeels hetzelfde klinken, maar er zitten kleine verschillen (bijvoorbeeld in loopjes, het net even anders plaatsen van lettergrepen onder noten, of het omhoog-omlaag gaan aan het eind vs. het omlaag-omhoog gaan aan het eind), dan betreffen R en R' verschillende uitvoeringsvormen.

**Toelichting (didactisch, niet-normatief voor liturgie):** een **cover** (zelfde compositie, andere invulling) of een lichter **arrangement** met herkenbare muzieklijn kan analoog zijn aan verschillende [uitvoeringsvormen](@) onder dezelfde [variant](@) — classificatie is niet altijd eenduidig; documenteer via `based_on` en [herkomst](@).

|               | Voorbeeld                                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------------------------- |
| **Ja**        | `liturgikon` vs `groningen` vs `hemelum` onder `antifoon-1-weekdagen` / `liturgikon-weekdagen`                 |
| **Nee**       | Scan en getrouwe VSA van **dezelfde** uitvoering → twee **[representaties](@)** (§8), één [uitvoeringsvorm](@) |
| **Randgeval** | 0 [representaties](@); [uitvoeringsvorm](@) bestaat met [herkomst](@) “mondeling / koorleider”                 |

---

## 8. Representatie

**Criterium:** R is een [representatie](@) onder [uitvoeringsvorm](@) U dan en slechts dan als:

1. R is een bestand waarmee [uitvoeringsvorm](@) U concreet is vastgelegd (VSA, scan, MusicXML), **en**
2. R is onderscheidbaar van andere [representaties](@) onder **dezelfde** U (`representatie-id`, [herkomst](@)).

**Toelichting:** [Representatie](@) specificeert U; U hoort bij [variant](@) V en [zangstuk](@) Z. Twee representaties onder **dezelfde** U documenteren **dezelfde** [uitvoeringsvorm](@) (bijv. scan + transcriptie). Verschillende muziek onder dezelfde U → classificatiefout of extra uitvoeringsvorm (§7).

|               | Voorbeeld                                                                                           |
| ------------- | --------------------------------------------------------------------------------------------------- |
| **Ja**        | `hemelum.vsa`; Liturgikon-scan PDF; inline VSA-blok (tot extraktie)                                 |
| **Nee**       | Abstract [zangstuk](@); `melodie.svg` ([afgeleide](@)); [manifest](@) (§16) zonder [bronbestand](@) |
| **Nee**       | Tweede melodie Cherubijnenhymne → andere **[variant](@)**, geen tweede repr. onder dezelfde U       |
| **Randgeval** | Identieke `.vsa`, twee `representatie-id`s → duplicaat; vermijden                                   |

**Legacy bron-repo:** veld `sources[].id` in `zangstuk.yaml` ≈ **`representatie-id`** (historische naam “source-id”); migreer terminologie in docs naar `representatie-id`.

---

## 9. Herkomst

**Criterium:** H is [herkomst](@) van entiteit X dan en slechts dan als H metadata beschrijft *waar X vandaan komt* (mens, traditie, publicatie, parochie), **niet** zijnde [bronbestand](@) of [bron-repository](@).

| Niveau               | Voorbeeld                                           |
| -------------------- | --------------------------------------------------- |
| [Zangstuk](@)        | `reference: "Liturgikon, weekdagen"`                |
| [Variant](@)         | `"Obikhod-traditie"`; `"A. Kastorski, koormap 15c"` |
| [Uitvoeringsvorm](@) | `"Parochie Groningen, refreinpraktijk"`             |
| [Representatie](@)   | transcribent, `based_on` scan                       |

[Herkomst](@) mag **onbekend** zijn — entiteit bestaat desondanks.

---

## 10. Bronbestand

**Criterium:** Bestand F is een [bronbestand](@) dan en slechts dan als in die repository geen geautomatiseerd, herhaalbaar [conversiemechanisme](@) F volledig uit een ander *getrackt* bestand genereert.

|               | Voorbeeld                                                                             |
| ------------- | ------------------------------------------------------------------------------------- |
| **Ja**        | handmatig `.vsa`; scan-PDF; MusicXML uit MuseScore                                    |
| **Nee**       | `.svg` na `vsa svg`; gegenereerde Hugo-pagina                                         |
| **Randgeval** | `.coria.html` naast `.vsa` → voorlopig [bronbestand](@); herbeoordelen bij Coria-spec |

---

## 11. Afgeleide

**Criterium:** G is [afgeleide](@) van [bronbestand](@) B dan en slechts dan als [conversiemechanisme](@) M met M(B)=G bestaat, M geautomatiseerd/herhaalbaar is, en G niet als bron in [bron-repository](@) staat.

|         | Voorbeeld                                       |
| ------- | ----------------------------------------------- |
| **Ja**  | `.svg` uit `vsa svg`; `.mxl` uit `vsa musicxml` |
| **Nee** | `.vsa`; handbewerkt `.vsa`; scan-PDF            |

---

## 12. Bron-repository

**Criterium:** R is de [bron-repository](@) dan en slechts dan als R de git-repo `orthodox-groningen/bron` is (of expliciet aangewezen opvolger).

|         | Voorbeeld                                             |
| ------- | ----------------------------------------------------- |
| **Ja**  | `github.com/orthodox-groningen/bron`                  |
| **Nee** | [VSA-tooling](@); parochie Hugo-repo; vendor-checkout |

---

## 13. Source-entry

**Criterium:** S is een [source-entry](@) dan en slechts dan als S een element is in `sources:` van `zangstuk.yaml` in [bron-repository](@), met uniek `id` (≈ `representatie-id`) binnen dat [zangstuk](@) **op het huidige platte model**.

**Toelichting:** Registreert een [representatie](@) (of placeholder). Meerdere entries = meerdere [representaties](@) **of** (legacy) nog niet onderscheiden [variant](@)/[uitvoeringsvorm](@) — bij nieuw werk vier-niveau-metadata gebruiken.

|         | Voorbeeld                                                                  |
| ------- | -------------------------------------------------------------------------- |
| **Ja**  | `{ id: groningen, file: sources/vsa/groningen.vsa, based_on: liturgikon }` |
| **Ja**  | `{ id: liturgikon, status: nog-niet-getranscribeerd }`                     |
| **Nee** | Alleen `.vsa` zonder yaml-entry                                            |

---

## 14. Geregistreerde representatie

**Criterium:** R is [geregistreerde representatie](geregistreerde-representatie@) dan en slechts dan als een [source-entry](@) S in [bron-repository](@) bestaat die R koppelt via `file:`, `access:`, of `status:`.

|         | Voorbeeld                                         |
| ------- | ------------------------------------------------- |
| **Ja**  | `groningen` met `file: sources/vsa/groningen.vsa` |
| **Nee** | `lokaal/.../hemelum.vsa` vóór PR                  |
| **Nee** | Inline VSA zonder entry                           |

---

## 15. Parochie-lokale representatie

**Criterium:** R is [parochie-lokaal](@) dan en slechts dan als R [bronbestand](@) of inline-notatie in een parochie-repo is **en** R niet [geregistreerd](geregistreerde-representatie@) is.

|         | Voorbeeld                                                  |
| ------- | ---------------------------------------------------------- |
| **Ja**  | `content-source/lokaal/.../hemelum.vsa` vóór [promotie](@) |
| **Ja**  | Inline VSA in [samenstelling](@)                           |
| **Nee** | Na bron-sync canonical uit bron-repo                       |

Zie [parochie-lokaal zangstukken](../manuals/parochie-lokaal-zangstukken.md).

---

## 16. Manifest

**Criterium:** Bestand M is een [manifest](@) dan en slechts dan als:

1. M is een YAML-bestand met **vaste bestandsnaam** op één van de twee niveaus [variant](@) (§6) of [uitvoeringsvorm](@) (§7) binnen het vier-niveaumodel (§1), **en**
2. M registreert precies **één** entiteit op dat niveau via het bijbehorende id-veld (`variant-id` of `uitvoeringsvorm-id`), **en**
3. M beschrijft uitsluitend **metadata** over die entiteit (titels, aliassen, [herkomst](@), `based_on`, verwijzingen naar [representaties](@)) — M is zelf **geen** [representatie](@) (§8), [bronbestand](@) (§10) of [samenstelling](@) (§18).

**Vaste bestandsnamen (canoniek):**

| Niveau               | Bestandsnaam           | Id-veld in yaml      |
| -------------------- | ---------------------- | -------------------- |
| [Variant](@)         | `variant.yaml`         | `variant-id`         |
| [Uitvoeringsvorm](@) | `uitvoeringsvorm.yaml` | `uitvoeringsvorm-id` |

Meerdere [manifesten](@) in dezelfde mappenstructuur noemen wij **manifesten** (meervoud).

**Toelichting:** Een [manifest](@) is de machine-leesbare registratie van variant- of uitvoeringsvorm-metadata. Op uitvoeringsvorm-niveau mag een manifest [representaties](@) **verwijzen** (`representaties:` met `representatie-id` en relatief `file:`), zonder zelf notatie te bevatten.

**Parochie-lokaal:** [manifesten](@) staan onder `content-source/lokaal/<zangstuk-id>/<variant-id>/…` — zie [parochie-lokaal zangstukken](../manuals/parochie-lokaal-zangstukken.md).

**Relatie tot [bron-repository](@):** `zangstuk.yaml` en `sources:` (§13 [source-entry](@)) zijn **geen** [manifest](@) — ander plat model, andere bestandsnaam.

**Implementatiestatus:** velden zijn vandaag vooral **informatief** voor beheerders; validatie in tooling richt zich primair op [bronbestanden](@) en [samenstelling](@)-includes.

|               | Voorbeeld                                                                                           |
| ------------- | --------------------------------------------------------------------------------------------------- |
| **Ja**        | `lokaal/…/liturgikon-weekdagen/variant.yaml`                                                        |
| **Ja**        | `lokaal/…/hemelum/uitvoeringsvorm.yaml` met `representaties: [{ representatie-id: hemelum, … }]`    |
| **Nee**       | `hemelum.vsa` ([bronbestand](@) / [representatie](@))                                               |
| **Nee**       | `zangstuk.yaml` in [bron-repository](@) ([source-entry](@)-model)                                   |
| **Nee**       | `antifonen-hemelum.md` ([samenstelling](@))                                                         |
| **Nee**       | npm `package.json`, PWA manifest, CI build-manifest, `.gitignore`-patroon `*.manifest`              |
| **Randgeval** | [Manifest](@) zonder representatie-verwijzing — [uitvoeringsvorm](@) met 0 [representaties](@) (§1) |

---

## 17. Promotie (registratie)

**Criterium:** [Promotie](@) is overgang [parochie-lokaal](@) → [geregistreerd](geregistreerde-representatie@) door [source-entry](@) (+ [bronbestand](@)) in [bron-repository](@), met behoud van canonieke ids.

|         | Voorbeeld                                                                                 |
| ------- | ----------------------------------------------------------------------------------------- |
| **Ja**  | PR: `hemelum.vsa` + yaml `id: hemelum, based_on: liturgikon`                              |
| **Nee** | Nieuw [zangstuk](@)-map terwijl extra [representatie](@) onder bestaand zangstuk volstaat |

---

## 18. Samenstelling

**Criterium:** D is een [samenstelling](@) dan en slechts dan als D markdown (met VSA-directives) [representaties](@) ordent voor een lezersdoel, zonder zelf [representatie](@) te zijn.

|         | Voorbeeld                                  |
| ------- | ------------------------------------------ |
| **Ja**  | `zondag-toon-1.md`, `antifonen-hemelum.md` |
| **Nee** | `groningen.vsa`; `zangstuk.yaml`           |

---

## 19. Compositie

**Criterium:** C is een [compositie](@) dan en slechts dan als C YAML onder `composities/` in **[bron-repository](@)** is met geordende verwijzingen naar [zangstukken](@) (toekomst: `(zangstuk-id, variant-id, uitvoeringsvorm-id)`).

*(Nog niet geïmplementeerd in bron.)*

**Niet verwarren met sjabloon:** een parochie-**sjabloon** is markdown in de
content-source (dienst-, koormap- of herkomst-sjabloon) met **`:::include zoek="…"`**;
ingevuld (opgelost pad) is een [samenstelling](@) (§18). Zie
[catalogus-samenstelling-zangstuk.md](catalogus-samenstelling-zangstuk.md).

| Term                   | Waar                              | Formaat                                                    |
| ---------------------- | --------------------------------- | ---------------------------------------------------------- |
| **[Compositie](@)**    | org-brede ordered list (toekomst) | yaml in `bron/composities/`                                |
| **Sjabloon**           | parochie                          | markdown + `default.gelegenheidstype` + `:::include zoek=` |
| **[Samenstelling](@)** | parochie-publicatie               | markdown + `:::include` met catalogus-pad (§18)            |

---

## 20. Conversiemechanisme, exportmechanisme, exporttype

**[Conversiemechanisme](@) M:** gedefinieerde tool M(B)=G; G is [afgeleide](@).

**[Exportmechanisme](@):** hoe een [samenstelling](@) [bronbestand](@) of [afgeleide](@) ontsluit.

**[Exporttype](@):** naam in `:::include <type>` — `svg`, `coria`, `mxl`.

---

## 21. Disambiguatie “variant”

| Bedoeling                                                 | Term                     | Toets                                                  |
| --------------------------------------------------------- | ------------------------ | ------------------------------------------------------ |
| Andere vastlegging, **zelfde** [uitvoeringsvorm](@)       | **[representatie](@)**   | Zelfde U; zelfde hoorbare uitvoering                   |
| **Andere** muziek, **zelfde** liturgische functie onder Z | **[variant](@)**         | Wezenlijk andere melodie t.o.v. andere variant onder Z |
| **Zelfde** [variant](@), **andere** hoorbare invulling    | **[uitvoeringsvorm](@)** | Operationele test §7                                   |
| Waar iets vandaan komt                                    | **[herkomst](@)**        | Metadata, geen bestand                                 |

---

## 22. Open punten

| Onderwerp                                              | Status                                                                                                       |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Geneste yaml variant→uitvoeringsvorm→repr in bron      | Uitgesteld                                                                                                   |
| Manifest-term bij geneste yaml in bron (§16)           | Open                                                                                                         |
| Alias-resolver in tooling                              | Geïmplementeerd (basis) — zie [catalogus-architectuur](catalogus-architectuur.md)                            |
| Sjabloon `:::include zoek=` + `vsa resolve-catalogus`  | **Geïmplementeerd** (basis) — zie [catalogus-samenstelling-zangstuk.md](catalogus-samenstelling-zangstuk.md) |
| **referentie** (herkomst) vs **catalogus-pad** in docs | Gedocumenteerd in catalogus-samenstelling-zangstuk.md                                                        |
| Metadata-zoek (`catalogus.zoek` / `zoek_kandidaten`)   | **Geïmplementeerd** (basis)                                                                                  |
| Automatische terminologie-lint (R1–R2)                 | Open                                                                                                         |
| `.coria.html` definitief bron vs afgeleide             | Open                                                                                                         |

---

## Wijzigingshistorie

| Datum   | Wijziging                                                                         |
| ------- | --------------------------------------------------------------------------------- |
| 2026-07 | Term **manifest** (§16); yaml id-velden met koppelteken; §17–§21 hernummerd       |
| 2026-06 | Vier-niveau-model, uitvoeringsvorm-id, aliassen, canonieke ids, gebruiksregels §0 |
