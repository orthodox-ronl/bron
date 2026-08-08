# Overzicht

Deze pagina verzamelt **gebruikersverhalen** over de catalogus-tool. Ze
beschrijven hoe **Rene** (liturgiecoördinator in de parochie Groningen) en
**Nana** (parochie-componist) zangmateriaal vinden, lokaal toevoegen,
**sjablonen** vullen tot **samenstellingen**, en materiaal delen via **bron**.

De verhalen zijn **voorbeelden** (parochie Groningen), bedoeld als
userdocumentatie voor vrijwilligers en als basis voor latere handleidingen.

## Kernworkflow (doelbeeld)

1. Rene opent een **markdown-sjabloon** (dienst, koormap of herkomst) — zonder
   individuele **`default.gelegenheid`**.
2. Hij maakt een **sessie** en vult **`default.gelegenheid`** (en evt. `toon`) in.
3. Op vaste plekken staat **`:::include`** met **`zoek="…"`** — liturgische rol.
4. Hij **lost de zoekopdrachten op** tot catalogus-paden; **review** alleen bij
   ambiguïteit.
5. Hij **bouwt** het opgeloste bestand naar de site / export.

Contract: [zangstuk in samenstelling-sjablonen](../../specs/catalogus-samenstelling-zangstuk.md).

Commando’s (wanneer je CLI gebruikt):
[Catalogus CLI](../../reference/catalogus-cli.md),
[`vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/),
[`vsa build-markdown`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/build-markdown/).

## Persona's en context

| Naam  | Rol                                      | Werkt met                                                 |
| ----- | ---------------------------------------- | --------------------------------------------------------- |
| Rene  | Liturgiecoördinator, parochie Groningen  | Sjablonen, samenstellingen, parochie-repo, PR's naar bron |
| Nana  | Componist / arrangeur in de parochie     | Nieuwe stukken (PDF, VSA, MusicXML)                       |

**Repositories:**

| Repo              | Pad (voorbeeld)                                              | Inhoud                                       |
| ----------------- | ------------------------------------------------------------ | -------------------------------------------- |
| **bron**          | `C:\Git\orthodox-groningen\bron`                             | Org-brede zangstukken (`zangstukken/`)       |
| **parochie-site** | `C:\Git\orthodox-groningen\VSA-demo\content-source`          | Sjablonen, samenstellingen, `lokaal/` (demo) |

Terminologie: [terminologie §2](../../specs/terminologie.md) — opslag blijft vier
niveaus; Rene typt vooral **zoektekst**.

### `Groningen`, `groningen` en `vokn` in deze verhalen

| Term                                     | Betekenis in de verhalen                                                         |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| **Parochie Groningen**                   | Persona / plaats — geen catalogus-id                                             |
| **`default.uitvoeringsvorm: Groningen`** | Parochie-default bij zoeken (invoer alias) — **niet** in mixed session           |
| **`uitvoeringsvorm-id: groningen`**      | Parochie-specifieke uitvoeringsvorm (bijv. Nana's Kastorski-bewerking)           |
| **`uitvoeringsvorm-id: liturgikon`**     | Bron-uitvoeringsvorm (Liturgikon-model; demo feest-stukken)                      |
| **`vokn`**                               | (Gepland in glossary) VOKN-standaardkoormap — **niet** hetzelfde als `groningen` |

Tot de glossary-PR over **`vokn`** vastligt, gebruiken de verhalen **`Groningen`**
/`groningen` waar het om **parochiepraktijk** gaat. Materiaal rechtstreeks uit de
VOKN-standaardkoormap krijgt later **`uitvoeringsvorm-id: vokn`**; zie
[samenvatting-project — legacy yaml](../../plans/samenvatting-project.md).

## Interface: GUI (beoogd) en CLI (nu)

!!! note "CLI vs GUI"
    [`catalogus zoek`](../../reference/catalogus-cli.md#catalogus-zoek), [`vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/) en **`:::include zoek=`** zijn
    **geïmplementeerd** (CLI). Een **grafische catalogus** (sessie-wizard,
    interactieve review bij ambiguïteit) is nog **gepland**.

Technische referentie: [Catalogus CLI](../../reference/catalogus-cli.md),
[Catalogus-architectuur](../../specs/catalogus-architectuur.md),
[Catalogus — zoek-API](../../specs/catalogus-zoek-api.md),
[Zangstuk in samenstelling-sjablonen](../../specs/catalogus-samenstelling-zangstuk.md).

## Verhalen

| #   | Titel                                                                    | Wat leer je                                    |
| -   | ---------------------------------------------------------------------    | ---------------------------------------------- |
| —   | [Sjabloon schrijven](sjabloon-schrijven.md)                              | `default`, `:::include zoek=`, sessie          |
| 1   | [Liturgie — Geboorte Moeder Gods](rene-liturgie-geboorte-moeder-gods.md) | Sjabloon → sessie → resolve                    |
| 2   | [Cherubijnenhymne lokaal opnemen](rene-cherubijnenhymne-lokaal.md)       | PDF/VSA in `lokaal/`                           |
| 3   | [Cherubijnenhymne naar bron](rene-cherubijnenhymne-naar-bron.md)         | Promotie via pull request                      |
| 4   | [MusicXML delen](rene-cherubijnenhymne-musicxml.md)                      | MXL als bron                                   |

## Volgorde

Verhalen 2 → 3 → 4 sluiten aan; verhaal 1 staat op zichzelf.
