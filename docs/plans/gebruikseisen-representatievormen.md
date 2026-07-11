# Gebruikseisen representatievormen (papier / tablet / telefoon)

**Status:** concept — nog niet gevalideerd met echte bestanden/gebruikers
**Doel van dit document:** vastleggen wát een `representatie` (in de zin van het catalogusmodel) moet kunnen, per drager, vóórdat hier tooling voor Rene op gebouwd wordt. Dit is een eisendocument, geen ontwerp: de kolom "status" geeft aan of iets een vastgestelde eis, een open vraag, of een bewust uitgestelde keuze is.

Elke eis krijgt drie kolommen:
- **Eis** — wat moet er kunnen
- **Reden** — de praktijksituatie die dit oproept
- **Status** — `vastgesteld` / `open` / `bewust uitgesteld`

---

## 1. Dragers

Een zangstuk/variant kan in meerdere vormen gepresenteerd worden. Dit document onderscheidt drie dragers, die elk andere eisen meebrengen:

- **Papier** — gedrukte koormap, A4, vaste paginering.
- **Tablet** — los scherm, meegenomen naar repetitie/dienst, gebruikt tijdens het zingen.
- **Telefoon** — zelfde als tablet, maar kleiner scherm; expliciet meegenomen als aparte drager omdat schermgrootte de eisen beïnvloedt.

Papier en digitaal (tablet/telefoon) zijn niet één keuze maar een verzameling losse assen (paginering, navigatie, lettergrootte, connectiviteit). Dit document behandelt die assen apart, zodat duidelijk blijft welke eis aan welke drager vastzit en welke universeel is.

---

## 2. Responsiviteit (vastgesteld)

| Eis | Reden | Status |
|---|---|---|
| Digitale representaties (tablet én telefoon) moeten responsief zijn: dezelfde representatie moet bruikbaar zijn op verschillende schermgroottes zonder handmatig zoomen/pannen. | Koorleden gebruiken zowel tablets als telefoons; er is niet één vast formaat om voor te ontwerpen. | vastgesteld |
| Papier blijft gebonden aan vaste paginering (A4, druk, eventueel dubbelzijdig). | Fysieke koormappen worden gedrukt en moeten daadwerkelijk passen en bladerbaar zijn. | vastgesteld |

**Consequentie voor het model:** "papier" en "tablet/telefoon" zijn wat representatie betreft niet twee vaste formaten, maar minstens twee families: één met vaste paginering (PDF/druk) en één responsief (HTML-achtig). Dat pleit ervoor de responsieve variant als HTML (of vergelijkbaar) te genereren in plaats van als een vaste-pagina-PDF die op een tablet bekeken wordt.

---

## 3. Digitale drager: server, geen app (voorlopig)

Voor nu kiezen we bewust de eenvoudigere invulling: geen native app om mee te ontwikkelen. In plaats daarvan geldt:

| Eis | Reden | Status |
|---|---|---|
| Tablet/telefoon hebben altijd een verbinding nodig met een **server** waarop de variant-/uitvoeringsvorm-representaties staan (of vandaan gegenereerd worden). Er is geen lokale opslag op het apparaat zelf. | Eenvoudiger te bouwen en te onderhouden dan een app met eigen synchronisatie-/opslaglogica. | vastgesteld |
| Als die server **lokaal** beschikbaar is (bijv. draait in het kerkgebouw op een laptop/mini-pc, of eventueel op het apparaat zelf), is er geen internetverbinding nodig — het gaat om een verbinding met de server, niet per se om internet. | Dit maakt de eis "geen internetverbinding tijdens uitvoeren" (§4) haalbaar zonder app: internet en "verbinding met de server" zijn twee verschillende dingen. | vastgesteld |
| Als er geen lokale server beschikbaar is, is een internetverbinding naar een externe server wél nodig. | Zonder app of lokale server is een externe verbinding de enige overgebleven optie. | vastgesteld |

**Voordeel van deze aanpak:** omdat er sowieso een server in het spel is, kan die server ook representaties **genereren** (bijv. SVG's, MusicXML, PDF's) in plaats van dat alles vooraf statisch klaar moet staan of dat de client dit zelf moet doen. Dat vereenvoudigt ook §6 (koppeling aan het model): de server is de plek die weet of iets al bestaat, nog gegenereerd moet worden, of nog gekopieerd moet worden.

**Een app is een mogelijke toekomstige uitbreiding**, waarmee een internetverbinding tijdens diensten helemaal niet meer nodig zou zijn (ook niet naar een lokale server) omdat het apparaat dan zelf alles bij zich heeft. Dat idee staat apart beschreven in de ideeën-backlog, en valt buiten de scope van dit document.

---

## 4. Online/offline

### 4.1 Papier: nooit online-afhankelijk materiaal, tenzij expliciet toegevoegd (vastgesteld)

| Eis | Reden | Status |
|---|---|---|
| De papieren versie wordt gebruikt voor zowel thuis oefenen als voor zingen/uitvoeren, en bevat in beide gevallen geen (links naar) materiaal dat een online verbinding vereist — zoals verwijzingen naar Coria — tenzij Rene dat later uitdrukkelijk zelf toevoegt. | Papier heeft geen mechanisme om zulk materiaal afhankelijk van context te tonen of te verbergen (zie oefenmodus, §5); het veiligste uitgangspunt is dat papier er standaard vrij van is. | vastgesteld |

### 4.2 Tablet/telefoon: oefenen versus uitvoeren (vastgesteld)

Voor digitale dragers is "geen verbinding nodig" niet overal hetzelfde — dat hangt af van de situatie én van waar de server draait (zie §3):

| Situatie | Verbinding | Status |
|---|---|---|
| Thuis oefenen (individueel, via tablet/telefoon) | Mag een (internet)verbinding naar de server vereisen | vastgesteld |
| Zingen/uitvoeren (repetitie in kerk, dienst zelf) | Moet zonder internétverbinding bruikbaar zijn — dat betekent in de huidige opzet (§3): er moet dan een **lokale server** beschikbaar zijn | vastgesteld |

**Consequentie voor het model:** een representatie die tijdens de dienst gebruikt wordt (papier of tablet/telefoon) mag geen harde afhankelijkheid hebben van een live internetverbinding. Verwijzingen naar oefenmateriaal horen dus bij het oefenscenario, niet bij het uitvoerscenario, en dat scenario-onderscheid wordt op tablet/telefoon expliciet gemaakt via de oefenmodus (§5).

---

## 5. Oefenmodus en non-invasieve verwijzingen naar oefenmateriaal (bijv. Coria)

### 5.1 Oefenmodus als concept (vastgesteld)

| Eis | Reden | Status |
|---|---|---|
| Papier heeft geen oefenmodus. | Volgt direct uit §4.1: er is sowieso geen online-afhankelijk materiaal aanwezig om achter een modus te verbergen. | vastgesteld |
| Tablet/telefoon kan een oefenmodus hebben. Alles wat met oefenmateriaal te maken heeft (links naar Coria, audio, e.d.) wordt achter deze modus verborgen. | Zo blijft de digitale representatie buiten oefenmodus qua gedrag gelijkwaardig aan papier: geen verbindingsafhankelijkheid, geen geluid, niets dat afleidt tijdens uitvoeren. | vastgesteld |
| Oefenmodus is een **globale schakelaar**: voor de hele applicatie/website-sessie, niet per zangstuk of representatie apart. | Eenvoudiger en voorspelbaarder voor de gebruiker dan een schakelaar per stuk; sluit aan bij hoe je van tevoren weet of je gaat oefenen of uitvoeren. | vastgesteld |
| De schakelaar moet een **zichtbaar icoontje/knop** zijn. Die mag in een menu zitten, maar dan **niet meer dan één niveau diep** — geen uitgebreid zoeken in instellingen. | Toegankelijk genoeg om te vinden zonder handleiding, maar hoeft niet permanent in beeld te staan. | vastgesteld |

### 5.2 Wat "non-invasief" betekent, ook binnen oefenmodus (vastgesteld)

| Eis | Reden | Status |
|---|---|---|
| Buiten oefenmodus is er geen link/verwijzing naar oefenmateriaal zichtbaar of actief. | Directe consequentie van 5.1: de gebruiker die niet in oefenmodus zit, hoeft niet te weten dat die verwijzing bestaat. | vastgesteld |
| Geen auto-play van audio, ook niet binnen oefenmodus. | Verstoort zingen/repeteren en is überhaupt ongewenst gedrag. | vastgesteld |
| Geen pop-ups (in de stijl van reclame-pop-ups). | Zelfde reden; bovendien voelt dat "invasief" aan voor de gebruiker. | vastgesteld |
| Geluid (piepjes e.d.) moet uitzetbaar zijn — zoals bij elke tablet/telefoon-functionaliteit gebruikelijk is. | Standaardgedrag van deze apparaten; geen reden om hier van af te wijken. | vastgesteld |
| Geluid staat **standaard uit**, ook binnen oefenmodus. | De gebruiker hoeft niet noodzakelijk te weten dat er een link naar oefenmateriaal (Coria) in zit; het mag niet vanzelf "aan" gaan. | vastgesteld |

---

## 6. Koppeling van de link aan het model

Een link naar oefenmateriaal hoort inhoudelijk bij het canonieke zangstuk (variant/uitvoeringsvorm), niet bij één specifieke representatie — anders moet dezelfde link in elke representatie (PDF, HTML, …) apart onderhouden worden. Tegelijk bepaalt de representatie wél wat je ermee kunt: een PDF kun je niet laten afspelen; alleen een digitale, interactieve representatie kan dat.

Voorstel (te valideren met een experiment, zie §7):

- Rene specificeert bij een variant/uitvoeringsvorm een **directive**: welke presentatievorm(en) van oefenmateriaal er relevant zijn (bijv. `audio`, `visueel`, verder te specificeren), zonder zelf op te zoeken/te weten waar het bronbestand precies vandaan komt.
- De server (§3) zoekt vervolgens op:
  - waar het bijbehorende bestand al bestaat, of
  - of het nog gegenereerd moet worden uit ander bronmateriaal, of
  - of het nog gekopieerd/verplaatst moet worden,
  - en of het als link (online, alleen bij oefenen) of als deel van de representatie (bruikbaar zonder internet, zolang de server lokaal is) aangeboden wordt.
- De representatie die uiteindelijk getoond wordt (PDF vs. digitaal) bepaalt of die directive zichtbaar wordt als bruikbare link (digitaal) of genegeerd wordt (PDF/papier kan de directive niet uitvoeren, alleen eventueel tonen als verwijzing in tekst).
- Het (digitale) materiaal dat hierbij gepresenteerd wordt, dan wel gegenereerd moet worden, komt ofwel uit een lokale repo, ofwel uit de `bron`-repo — zoals dat in de bestaande specificaties (lokaal/bron-scheiding) is vastgelegd. Deze directive introduceert dus geen nieuwe opslagplek naast wat er al is; hij verwijst er alleen naar.

| Openstaande punten | Status |
|---|---|
| Exacte vorm van de directive (syntax, plek in manifest) | open |
| Volledige lijst van presentatievormen (audio, visueel, …) | open — "verder te specificeren" |
| Wat een digitale representatie doet als het bronbestand van de link nog niet bestaat/nog gegenereerd moet worden — foutmelding, stil negeren, placeholder? | open |

---

## 7. Validatie-aanpak

Dit document wordt niet in één keer "af" verklaard. Per open vraag: een klein experiment met een bestaand zangstuk en een echt koorlid, bijvoorbeeld:
- één zangstuk zowel als PDF als kale HTML-pagina op een echte tablet/telefoon laten zien tijdens oefenen (niet tijdens een dienst), en vragen wat er misgaat;
- een testlink naar oefenmateriaal toevoegen en checken of geluid inderdaad standaard uit staat en niets vanzelf opent;
- een lokale server opzetten (bijv. op een laptop) en testen of een tablet/telefoon daar zonder internet verbinding mee kan maken tijdens een repetitie.

Elk experiment sluit af met één van drie uitkomsten: (1) eis in dit document bevestigd, (2) eis aangepast, of (3) nog steeds open — expliciet gemarkeerd, niet stilzwijgend laten vervallen.

---

## 8. Beslist: geen apart probleem

- **Consistentie in nummering/paginaverwijzing** tussen papier- en tabletgebruikers binnen dezelfde context (bijv. een repetitie) hoeft hier niet apart behandeld te worden. Uitgangspunt: binnen zo'n context bestaat er altijd al een indexeringsmechanisme (het nummer van de variant/uitvoeringsvorm in de koormap, of de titel van het zangstuk), en dat sluit aan bij wat nu al gangbare praktijk is. Rene brengt dit vanzelf in orde; er is geen aparte eis of ontwerpbeslissing nodig.

## 9. Nog niet in dit document behandeld (bewust uitgesteld)

- Toegankelijkheid (grotere lettertypes, contrast) — genoemd maar nog geen expliciete eis.
- Wie/wat genereert de digitale representatie uit hetzelfde bronmateriaal als de PDF (redactieproces vs. automatische server-generatie) — hangt samen met §3 en §6 maar is nog niet uitgewerkt.
- De app als toekomstige uitbreiding. Dat idee staat apart beschreven in de ideeën-backlog, en valt buiten de scope van dit document.