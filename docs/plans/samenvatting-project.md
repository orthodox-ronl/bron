---
doc_type: plan
audience: "P5 — Docs-/tool-contributor; P6 — Spec-/PR-reviewer"
---
# Samenvatting: Orthodoxe kerkmuziek-repository project

Status per 25 juni 2026. Bedoeld als startpunt voor een vervolggesprek met
Claude als het huidige gesprek de sessielimiet bereikt.

## Doel van het project

Een systeem voor orthodoxe kerkmuziek (Slavische traditie) waarmee parochies
zangmateriaal kunnen beheren, delen en gebruiken voor de liturgie en voor het
instuderen van stemmen door koorleden. Het geheel wordt opgezet binnen de
GitHub-organisatie `github.com/orthodox-groningen`, ontsloten via
GitHub Pages (`*.github.io`).

## Huidig experiment

We bouwen een **bron-repository** (`bron`) met daarin de zangstukken, en
zijn van plan om die te gaan testen via een kale **Hugo-installatie** voor de
parochie Hemelum (en later Groningen) die zangstukken uit `bron` ophaalt en
toont. Doel van dat experiment: erachter komen welke ontwerpbeslissingen de
bron-repo nodig heeft door 'm echt te proberen *gebruiken*, niet om nu al een
kant-en-klare site te bouwen.

**Stand van zaken: alleen de bron-repo is uitgewerkt. De Hugo-kant is nog
niet gestart.** Dat is de logische volgende stap.

## Architectuur — overwogen scenario's (besloten)

Drie scenario's zijn overwogen voor hoe parochies en de bron-repo zich tot
elkaar verhouden:

- **A. Monoliet bron + dunne parochie-sites** — alles centraal, parochies
  consumeren alleen.
- **B. Federatief** — elke parochie een eigen volwaardige repo, bron-repo
  alleen gedeelde basis.
- **C. Hybride** — bron-repo blijft centraal, met een laagdrempelig
  contributieproces voor parochies.

**Besluit**: voorlopig **scenario C in lichte vorm**. Met 2-3 parochies
(Hemelum, Groningen, mogelijk later Leeuwarden en Zwolle) en jij (de
opdrachtgever) als enige technische beheerder — de koorleider/priester
beoordeelt inhoudelijk maar werkt niet zelf met git — voegt een federatieve
opzet (B) alleen overhead toe zonder voordeel. Eén bron-repo dus, met
lichte, aparte presentatie-repo's per parochie (eigen "gezicht", gedeelde
content).

## Bron-repo: kernconcepten

### Terminologie
- **Zangstuk**: de eenheid waarvoor een bron (VSA, scan, MusicXML, ...)
  bestaat. Vervangt de eerder gebruikte, te generieke term "item".
- **Source / bron-variant**: een specifieke versie van een zangstuk, met
  eigen herkomst (auteur/componist/arrangeur, referentie).
- **Compositie** (nog niet uitgewerkt): een verzameling zangstukken in een
  bepaalde volgorde voor een gebruikscontext (bijv. "Antifonen - weekdagen,
  Hemelum"). Bedoeld om duplicatie van VSA-inhoud over meerdere
  markdown-bestanden te voorkomen. Vorm (YAML vs. leesbaar document) nog
  niet bepaald — bewust opengelaten, prioriteit lager dan de bron-repo zelf.

### Bron versus afgeleid: een principiële regel
Een bestand is een **bron** als er geen geautomatiseerd, herhaalbaar pad
bestaat om het uit een ander bestand in de repository te genereren. Dit
geldt voor scans, VSA-bestanden, en MusicXML/andere bestanden die
rechtstreeks uit een muziekprogramma komen (niet afgeleid van VSA). Een SVG
of MusicXML die door de vsa-tool automatisch uit een `.vsa`-bestand is
gegenereerd is **afgeleid** en wordt niet in de repository opgenomen — wordt
gegenereerd op het moment dat het nodig is (build-stap, nog niet
geïmplementeerd).

### Drie statussen voor een source-entry
1. **`file:`** — het bronbestand staat daadwerkelijk in de repository.
2. **`access:`** — het bestand wordt *niet* opgenomen omdat er copyright op
   rust; in plaats daarvan een contactpunt of URL.
3. **`status: nog-niet-getranscribeerd`** — de bron is bekend (en vaak vrij
   van rechten), maar nog niet als bestand aanwezig. Geen `file:`, geen
   `access:`. Nieuw geïntroduceerd toen bleek dat "bron nog niet
   getranscribeerd" iets anders is dan een copyright-kwestie.

### Eén bronbestand met meerdere zangstukken — een algemene regel
- **Tekst/VSA-bronbestanden** met meerdere zangstukken (bijv. een markdown
  met meerdere `::: vsa-notatie :::`-blokken) → **meteen splitsen** in losse
  `.vsa`-bestanden, één per zangstuk. Geen probleem, want elk zangstuk krijgt
  zijn eigen klein bestand.
- **Scans/PDF's** met meerdere zangstukken op één blad (zoals
  Troparion+Kondakion toon 1 op één scan) → **niet** splitsen (zou bijsnijden
  vereisen). In plaats daarvan: het bestand blijft bij één zangstuk, en het
  andere zangstuk verwijst ermee naar het bestand via een relatief pad
  (`file: ../ander-zangstuk/sources/scan/bestand.pdf`). Als dit patroon
  vaker voorkomt, een gedeelde `/scans/`-map op het hoogste niveau overwegen.

### Auteurschap / copyright
- Velden: `author`, `composer`, `arranger` (gebruik wat van toepassing is;
  ook waarden als "Anoniem" of "Anoniem-2" zijn toegestaan).
- `copyright_status`: `vrij`, `copyrighted`, of `onbekend`.
- Copyright-gevoelig materiaal wordt vooralsnog **niet** in een aparte
  private repo gezet — de metadata staat gewoon in de publieke bron-repo,
  alleen het bestand zelf ontbreekt (zie `access:` hierboven). Voor
  individuele zangstukken kan copyright-status worden vastgelegd; in het
  algemeen gaan we ervan uit dat het geen probleem wordt, zonder dat nu
  overal preventief uit te zoeken.

### Liturgische metadata (nieuw, ad-hoc geïntroduceerd, mag verder groeien)
- `gelegenheid`: de liturgische gelegenheid (bijv. "H. Nicolaas van Myra",
  "Zondag (opstandingscyclus)").
- `gelegenheidsdatum`: vaste kalenderdatum indien van toepassing (bijv. "12-06").
- `gelegenheidstype`: bijv. `vast-feest` of `zondag-cyclus`.
- `tone`: de liturgische toon (los van de identiteit/id van het zangstuk —
  bleek nodig omdat meerdere, totaal verschillende zangstukken in dezelfde
  toon kunnen staan).
- `koormap_nummer`: een bestaand, stabiel nummeringssysteem uit de
  Nederlandse liturgiepraktijk. Cijfer = volgorde van zangstukken voor
  niet-speciale zondagen; letter erachter = variant daarvan (bijv. "8a",
  "15c"). **Let op**: dit is iets anders dan de numerieke prefix in
  bestandsnamen zoals `010-`/`020-`/`034-` — dat laatste is slechts een
  sorteervolgorde van de scanbestanden zelf, geen liturgisch nummer (status:
  bevestigd door opdrachtgever).
- `language`: voor zangstukken met meerdere taalversies van dezelfde
  compositie (bijv. Cherubijnenhymne Kastorski: Kerkslavisch getranslitereerd
  + Nederlands).
- **Bewust nog niet vastgelegd**: schriftlezingen (epistel/evangelie) die in
  sommige bronbestanden bij een feest stonden. Die horen bij de
  viering/liturgische context als geheel, niet bij het zangstuk zelf — te
  behandelen zodra het liturgisch-kalender-subsysteem aan de orde is.

### Naamgevingsconventie voor zangstuk-id's
- Voor zangstukken die bij een **specifieke gelegenheid** horen (heiligenfeest
  op vaste datum): `<type>-<gelegenheid-slug>`, bijv.
  `troparion-nicolaas-van-myra`, `kondakion-tempelgang-moeder-gods`.
- Voor zangstukken die bij de **zondagscyclus** horen (afhankelijk van de
  toon van de week, niet van een vaste datum): `<type>-zondag-toon-<n>`,
  bijv. `troparion-zondag-toon-1`. Aanvankelijk per ongeluk `troparion-toon-1`
  genoemd; later hernoemd zodra de feest-specifieke naamgeving duidelijk
  maakte dat "toon" alléén niet onderscheidend genoeg is.
- Geen vaste regel (nog) voor zangstukken zonder duidelijke
  gelegenheid/cyclus (bijv. `trisagion`, `eengeboren-zoon`) — daar is de
  algemene naam van het zangstuk zelf voldoende.

## Licenties
Twee aparte licentiebestanden, omdat inhoud en eventuele code andere
licentievormen vragen:
- **`LICENSE-CONTENT`**: CC BY-SA 4.0, voor de zangstukken/notatie/metadata.
- **`LICENSE-CODE`**: MIT, voor eventuele scripts/tools.

## Openstaande vragen / nog te beslissen

1. **Compositie-laag**: vorm nog niet gekozen (puur YAML-verwijzingen vs.
   leesbaarder documentformaat). Lage prioriteit; pas relevant zodra er echt
   meerdere composities zijn om mee te vergelijken.
2. **Vierde zangstuk uit het Hemelum-bestand** ("Rest van de kleine
   intocht") — bewust nog niet uitgewerkt op verzoek van de opdrachtgever.
3. **Gedeelde `/scans/`-map**: nu opgelost met cross-reference vanuit één
   zangstuk naar het bestand bij een ander zangstuk. Zodra dit patroon
   vaker voorkomt, dit herzien.
4. **Kastorski copyright**: status `onbekend`, bewust niet uitgezocht
   (overlijdensjaar componist, auteursrechtelijke termijn).
5. **`docs/zangstuk-formaat.md`**: nog te schrijven — een formele
   specificatie van het zangstuk.yaml-formaat, gebaseerd op de vele
   praktijkgevallen die inmiddels zijn doorlopen.
6. **Hugo-opzet**: nog te beginnen. Eerste concrete stap: kale Hugo-site
   voor Hemelum, met als doel één pagina die één zangstuk toont. Open vraag
   daarbij: hoe haalt Hugo de data uit de bron-repo op (git submodule,
   build-time fetch via CI, of Hugo Modules)? Voorlopige voorkeur:
   build-time fetch, om submodule-gedoe en tight coupling te vermijden.
7. **Mogelijk ontbrekende uploads**: de opdrachtgever dacht meer
   markdown-/scanbestanden geüpload te hebben dan er daadwerkelijk zijn
   aangekomen. Geen technisch probleem geconstateerd — gewoon opnieuw
   uploaden indien nodig.

## Technische randvoorwaarden van de werkomgeving (voor Claude zelf)
- Geen directe toegang tot de computer van de opdrachtgever: alleen
  bestanden die expliciet zijn geüpload, zijn leesbaar; alleen bestanden die
  expliciet via `present_files` worden aangeboden, zijn voor de
  opdrachtgever downloadbaar.
- Werk gebeurt in een tijdelijke containeromgeving die niet persisteert
  tussen gesprekken.

## Volledige boomstructuur van de bron-repo tot nu toe

Onderstaande structuur toont alle bestanden zoals ze tot nu toe zijn
aangemaakt, inclusief de inhoud van elke `zangstuk.yaml` als commentaar
(zodat boom en inhoud in één oogopslag te zien zijn). PDF/VSA-bestanden zijn
hier alleen als bestandsnaam genoemd; hun inhoud staat niet herhaald (die is
al apart gedeeld in dit gesprek, en blijft ook gewoon op je eigen schijf
staan zodra je de eerder gedeelde bestanden hebt gedownload).

```yaml
bron/                                    # root van de bron-repository
  README.md
  LICENSE-CONTENT                        # CC BY-SA 4.0
  LICENSE-CODE                           # MIT
  .gitignore
  docs/
    zangstuk-formaat.md                  # NOG TE SCHRIJVEN

  zangstukken/

    antifoon-1-weekdagen/
      zangstuk.yaml
      # id: antifoon-1-weekdagen
      # title: "1e Antifoon (weekdagen)"
      # sources:
      #   - id: liturgikon
      #     author: "Liturgikon"
      #     reference: "Liturgikon, pp. 174-175, 270-271"
      #     copyright_status: vrij
      #     status: nog-niet-getranscribeerd
      #     note: "Bron bekend en vrij van rechten, maar nog niet als
      #            VSA-bestand getranscribeerd."
      #   - id: groningen
      #     file: sources/vsa/groningen.vsa
      #     based_on: liturgikon
      #     author: "Parochie Groningen"
      #     description: "Refreintekst 'Door de gebeden van de heilige
      #                    Moeder Gods, o Heiland, red ons'"
      #     copyright_status: vrij
      sources/
        vsa/
          groningen.vsa

    antifoon-2-weekdagen/
      zangstuk.yaml
      # id: antifoon-2-weekdagen
      # title: "2e Antifoon (weekdagen)"
      # sources:
      #   - id: liturgikon
      #     author: "Liturgikon"
      #     reference: "Liturgikon, pp. 174-175, 270-271"
      #     copyright_status: vrij
      #     status: nog-niet-getranscribeerd
      #     note: "Bron bekend en vrij van rechten, maar nog niet als
      #            VSA-bestand getranscribeerd."
      #   - id: groningen
      #     file: sources/vsa/groningen.vsa
      #     based_on: liturgikon
      #     author: "Parochie Groningen"
      #     description: "Refreintekst 'Verlos ons Zoon van God, Die
      #                    wonderbaar zijt in Uw heiligen...'"
      #     copyright_status: vrij
      sources/
        vsa/
          groningen.vsa

    eengeboren-zoon/
      zangstuk.yaml
      # id: eengeboren-zoon
      # title: "Eengeboren Zoon (weekdagen)"
      # sources:
      #   - id: liturgikon
      #     file: sources/vsa/liturgikon.vsa
      #     author: "Liturgikon"
      #     copyright_status: vrij
      sources/
        vsa/
          liturgikon.vsa

    # NOG NIET UITGEWERKT (op verzoek opdrachtgever):
    # troparia-kleine-intocht-weekdagen/   ("Rest van de kleine intocht")

    troparion-zondag-toon-1/
      zangstuk.yaml
      # id: troparion-zondag-toon-1
      # title: "Troparion - Zondag, toon 1"
      # gelegenheid: "Zondag (opstandingscyclus)"
      # gelegenheidstype: zondag-cyclus
      # toon: 1
      # sources:
      #   - id: scan-koormap-010
      #     file: sources/scan/010-troparion-kondakion-toon-1.pdf
      #     author: "Liturgikon"
      #     copyright_status: vrij
      #     note: "Scan bevat zowel het Troparion als het Kondakion van
      #            toon 1. Zie ook het zangstuk kondakion-zondag-toon-1,
      #            dat naar dit bestand verwijst. Voorlopige bron (platte
      #            tekst, geen notatie); te vervangen zodra een VSA- of
      #            MusicXML-versie beschikbaar is."
      #   - id: groningen
      #     file: sources/vsa/groningen.vsa
      #     based_on: scan-koormap-010
      #     author: "Parochie Groningen"
      #     copyright_status: vrij
      #     note: "VSA-transcriptie, afkomstig uit bronbestand
      #            'zondag-toon-1.md' (koormap Groningen). Inhoudelijk
      #            gelijk aan scan-koormap-010, nu als VSA-notatie
      #            beschikbaar."
      sources/
        scan/
          010-troparion-kondakion-toon-1.pdf
        vsa/
          groningen.vsa

    kondakion-zondag-toon-1/
      zangstuk.yaml
      # id: kondakion-zondag-toon-1
      # title: "Kondakion - Zondag, toon 1"
      # gelegenheid: "Zondag (opstandingscyclus)"
      # gelegenheidstype: zondag-cyclus
      # toon: 1
      # sources:
      #   - id: scan-koormap-010
      #     file: ../troparion-zondag-toon-1/sources/scan/010-troparion-kondakion-toon-1.pdf
      #     author: "Liturgikon"
      #     copyright_status: vrij
      #     note: "Dit zangstuk heeft geen eigen scanbestand: de scan
      #            bevat zowel het Troparion als het Kondakion van toon 1,
      #            en is fysiek opgeslagen bij het zangstuk
      #            troparion-zondag-toon-1. Eerste geval van een scan die
      #            door meerdere zangstukken wordt gedeeld; bij herhaling
      #            een gedeelde /scans/-map overwegen."
      #   - id: groningen
      #     file: sources/vsa/groningen.vsa
      #     based_on: scan-koormap-010
      #     author: "Parochie Groningen"
      #     copyright_status: vrij
      #     note: "VSA-transcriptie, afkomstig uit bronbestand
      #            'zondag-toon-1.md' (koormap Groningen)."
      sources/
        vsa/
          groningen.vsa
        # (geen sources/scan/ hier - zie note hierboven)

    trisagion/
      zangstuk.yaml
      # id: trisagion
      # title: "Trisagion"
      # koormap_nummer: "8a"
      # sources:
      #   - id: scan-koormap-020
      #     file: sources/scan/020-_8a__trisagion.pdf
      #     author: onbekend
      #     copyright_status: onbekend
      #     note: "Scan met genoteerde muziek (geen VSA). Tekst in het
      #            Nederlands met Kerkslavische transliteratie.
      #            Componist/arrangeur niet op het blad vermeld."
      sources/
        scan/
          020-_8a__trisagion.pdf

    cherubijnenhymne-kastorski/
      zangstuk.yaml
      # id: cherubijnenhymne-kastorski
      # title: "Cherubijnenhymne (Kastorski)"
      # koormap_nummer: "15c"
      # sources:
      #   - id: scan-koormap-034-ru
      #     file: sources/scan/034-_15c__cherubijnen_hymne__kastorski_-_ru_.pdf
      #     composer: "A. Kastorski"
      #     language: kerkslavisch-getranslitereerd
      #     copyright_status: onbekend
      #     note: "Zelfde compositie als scan-koormap-034-nl, alleen
      #            andere taal. Copyright-status nog niet uitgezocht."
      #   - id: scan-koormap-034-nl
      #     file: sources/scan/034-_15c__cherubijnen_hymne__kastorski_-_nl_.pdf
      #     composer: "A. Kastorski"
      #     language: nederlands
      #     copyright_status: onbekend
      #     note: "Zelfde compositie als scan-koormap-034-ru, Nederlandse
      #            vertaling van de tekst."
      sources/
        scan/
          034-_15c__cherubijnen_hymne__kastorski_-_ru_.pdf
          034-_15c__cherubijnen_hymne__kastorski_-_nl_.pdf

    cherubijnenhymne-onbekend/
      zangstuk.yaml
      # id: cherubijnenhymne-onbekend
      # title: "Cherubijnenhymne (vooralsnog ongeïdentificeerd)"
      # sources:
      #   - id: scan-koormap-groningen-2019
      #     file: sources/scan/koormap-groningen-2019.pdf
      #     author: onbekend
      #     copyright_status: onbekend
      #     note: "Scan uit koormap Groningen, 2019. Voorlopige bron; te
      #            vervangen zodra een VSA- of MusicXML-versie beschikbaar
      #            is. Componist/herkomst nog niet vastgesteld.
      #            PLACEHOLDER-bestand in de huidige uitwerking, geen
      #            echte scan-inhoud."
      sources/
        scan/
          koormap-groningen-2019.pdf      # placeholder, nog te vervangen

    troparion-nicolaas-van-myra/
      zangstuk.yaml
      # id: troparion-nicolaas-van-myra
      # title: "Troparion - H. Nicolaas van Myra"
      # gelegenheid: "H. Nicolaas van Myra"
      # gelegenheidsdatum: "12-06"
      # gelegenheidstype: vast-feest
      # toon: 4
      # sources:
      #   - id: liturgikon
      #     file: sources/vsa/liturgikon.vsa
      #     author: "Liturgikon"
      #     copyright_status: vrij
      sources/
        vsa/
          liturgikon.vsa

    kondakion-nicolaas-van-myra/
      zangstuk.yaml
      # id: kondakion-nicolaas-van-myra
      # title: "Kondakion - H. Nicolaas van Myra"
      # gelegenheid: "H. Nicolaas van Myra"
      # gelegenheidsdatum: "12-06"
      # gelegenheidstype: vast-feest
      # toon: 3
      # sources:
      #   - id: liturgikon
      #     file: sources/vsa/liturgikon.vsa
      #     author: "Liturgikon"
      #     copyright_status: vrij
      sources/
        vsa/
          liturgikon.vsa

    troparion-apostel-andreas/
      zangstuk.yaml
      # id: troparion-apostel-andreas
      # title: "Troparion - Apostel Andreas, de Eerstgeroepene"
      # gelegenheid: "Apostel Andreas, de Eerstgeroepene"
      # gelegenheidsdatum: "11-30"
      # gelegenheidstype: vast-feest
      # toon: 4
      # sources:
      #   - id: liturgikon
      #     file: sources/vsa/liturgikon.vsa
      #     author: "Liturgikon"
      #     copyright_status: vrij
      sources/
        vsa/
          liturgikon.vsa

    kondakion-apostel-andreas/
      zangstuk.yaml
      # id: kondakion-apostel-andreas
      # title: "Kondakion - Apostel Andreas, de Eerstgeroepene"
      # gelegenheid: "Apostel Andreas, de Eerstgeroepene"
      # gelegenheidsdatum: "11-30"
      # gelegenheidstype: vast-feest
      # toon: 2
      # sources:
      #   - id: liturgikon
      #     file: sources/vsa/liturgikon.vsa
      #     author: "Liturgikon"
      #     copyright_status: vrij
      sources/
        vsa/
          liturgikon.vsa

    troparion-tempelgang-moeder-gods/
      zangstuk.yaml
      # id: troparion-tempelgang-moeder-gods
      # title: "Troparion - Tempelgang van de Moeder Gods"
      # gelegenheid: "Tempelgang van de Moeder Gods"
      # gelegenheidsdatum: "11-21"
      # gelegenheidstype: vast-feest
      # toon: 4
      # sources:
      #   - id: liturgikon
      #     file: sources/vsa/liturgikon.vsa
      #     author: "Liturgikon"
      #     copyright_status: vrij
      sources/
        vsa/
          liturgikon.vsa

    kondakion-tempelgang-moeder-gods/
      zangstuk.yaml
      # id: kondakion-tempelgang-moeder-gods
      # title: "Kondakion - Tempelgang van de Moeder Gods"
      # gelegenheid: "Tempelgang van de Moeder Gods"
      # gelegenheidsdatum: "11-21"
      # gelegenheidstype: vast-feest
      # toon: 4
      # sources:
      #   - id: liturgikon
      #     file: sources/vsa/liturgikon.vsa
      #     author: "Liturgikon"
      #     copyright_status: vrij
      sources/
        vsa/
          liturgikon.vsa
```

## Sjablonen vs composities (notitie 2026-07)

| Concept | Waar | Normatief |
| ------- | ---- | --------- |
| **Compositie** | `bron/composities/*.yaml` (toekomst) | [terminologie §19](../specs/terminologie.md#19-compositie) |
| **Sjabloon** | markdown parochie content-source | [catalogus-samenstelling-zangstuk.md](../specs/catalogus-samenstelling-zangstuk.md) |
| **Samenstelling** | gepubliceerde markdown + `:::include` | [terminologie §18](../specs/terminologie.md#18-samenstelling) |

De hugo-demo `goddelijke-liturgie.yaml` is een **legacy** inventarisatie; nieuw
parochiewerk: sjablonen + catalogus (handleiding
[sjabloon schrijven](../manuals/catalogus/sjabloon-schrijven.md)).

## Hoe verder te gaan in een nieuw gesprek

Plak dit document als eerste bericht, en voeg toe wat je daarna wilt doen —
bijvoorbeeld:
- "Laten we nu `docs/zangstuk-formaat.md` schrijven op basis van het
  bovenstaande."
- "Laten we beginnen met de Hugo-opzet voor Hemelum."
- "Hier zijn nog een paar markdown-/scanbestanden met zangstukken, voeg die
  toe volgens dezelfde conventies."
