# Catalogus — gebruikersverhalen

Deze verhalen beschrijven hoe **Rene** (liturgiecoördinator in de parochie
Groningen) en **Nana** (parochie-componist) de **catalogus**-tool gebruiken om
zangmateriaal te vinden, lokaal toe te voegen, **sjablonen** te vullen tot
**samenstellingen**, en materiaal te delen via **bron**.

Ze zijn bedoeld als **userdocumentatie**: leesbaar voor vrijwilligers, bruikbaar
als basis voor latere handleidingen en GUI-ontwerp.

## Kernworkflow (doelbeeld)

1. Rene opent een **markdown-sjabloon** (dienst, koormap of herkomst) — zonder
   individuele **`default.gelegenheid`**.
2. Hij maakt een **sessie** en vult **`default.gelegenheid`** (en evt. `toon`) in.
3. Op vaste plekken staat **`:::include`** met **`zoek="…"`** — liturgische rol.
4. **`vsa resolve-catalogus`** → catalogus-pad; **review** alleen bij ambiguïteit.
5. **`vsa build-markdown`** op het opgeloste bestand → site / export.

Contract: [zangstuk in samenstelling-sjablonen](../../specs/catalogus-samenstelling-zangstuk.md).

## Persona's en context

| Naam  | Rol                                      | Werkt met                                                |
| ----- | ---------------------------------------- | -------------------------------------------------------- |
| Rene  | Liturgiecoördinator, parochie Groningen  | Sjablonen, samenstellingen, parochie-repo, PR's naar bron |
| Nana  | Componist / arrangeur in de parochie     | Nieuwe stukken (PDF, VSA, MusicXML)                      |

**Repositories:**

| Repo              | Pad (voorbeeld)                                              | Inhoud                                      |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------- |
| **bron**          | `C:\Git\orthodox-groningen\bron`                             | Org-brede zangstukken (`zangstukken/`)      |
| **parochie-site** | `C:\Git\orthodox-groningen\VSA-tooling\examples\hugo-demo\content-source` | Sjablonen, samenstellingen, `lokaal/` (demo) |

Terminologie: [terminologie §2](../../specs/terminologie.md) — opslag blijft vier
niveaus; Rene typt vooral **zoektekst**.

### `Groningen`, `groningen` en `vokn` in deze verhalen

| Term | Betekenis in de verhalen |
| ---- | ------------------------ |
| **Parochie Groningen** | Persona / plaats — geen catalogus-id |
| **`default.uitvoeringsvorm: Groningen`** | Parochie-default bij zoeken (invoer alias) |
| **`uitvoeringsvorm-id: groningen`** | Parochie-specifieke uitvoeringsvorm (bijv. Nana's Kastorski-bewerking) |
| **`vokn`** | (Gepland in glossary) VOKN-standaardkoormap — **niet** hetzelfde als `groningen` |

Tot de glossary-PR over **`vokn`** vastligt, gebruiken de verhalen **`Groningen`**
/`groningen` waar het om **parochiepraktijk** gaat. Materiaal rechtstreeks uit de
VOKN-standaardkoormap krijgt later **`uitvoeringsvorm-id: vokn`**; zie
[samenvatting-project — legacy yaml](../../plans/samenvatting-project.md).

## Interface: GUI (beoogd) en CLI (nu)

!!! todo "GUI + resolve-catalogus"
    De verhalen schetsen een **grafische catalogus** (sessie vullen, resolve,
    review). Vandaag: **`catalogus resolve`**, **`catalogus index validate`**;
    **`vsa resolve-catalogus`** en **`zoek=`** zijn gepland.

Technische referentie: [Catalogus CLI](../../reference/catalogus-cli.md),
[Catalogus-architectuur](../../specs/catalogus-architectuur.md),
[Catalogus — zoek-API](../../specs/catalogus-zoek-api.md),
[Zangstuk in samenstelling-sjablonen](../../specs/catalogus-samenstelling-zangstuk.md).

## Verhalen

| # | Titel                                                                 | Wat leer je                                    |
| - | --------------------------------------------------------------------- | ---------------------------------------------- |
| — | [Sjabloon schrijven](sjabloon-schrijven.md) | `default`, `:::include zoek=`, sessie |
| 1 | [Liturgie — Geboorte Moeder Gods](rene-liturgie-geboorte-moeder-gods.md) | Sjabloon → sessie → resolve |
| 2 | [Cherubijnenhymne lokaal opnemen](rene-cherubijnenhymne-lokaal.md) | PDF/VSA in `lokaal/`                           |
| 3 | [Cherubijnenhymne naar bron](rene-cherubijnenhymne-naar-bron.md) | Promotie via pull request                      |
| 4 | [MusicXML delen](rene-cherubijnenhymne-musicxml.md) | MXL als bron                                   |

## Volgorde

Verhalen 2 → 3 → 4 sluiten aan; verhaal 1 staat op zichzelf.
