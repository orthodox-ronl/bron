---
term: vsa-notatie
termType: concept
glossaryTerm: "VSA-notatie"
glossaryText: "Het tekstgebaseerde notatieformaat waarmee liturgische zangteksten worden vastgelegd: een formeel gespecificeerde taal met scopes, modifiers en bracket-directives, parseeerbaar en valideerbaar door [vsa-tooling](@)."
glossaryNotes:
  - "Een [vsa-bestand](@) is een [bronbestand](@) en tevens een [representatie](@) van een [uitvoeringsvorm](@)."
  - "VSA-notatie sluit aan bij de notatiepraktijk zoals beschreven in het Nederlandse Liturgikon (Den Haag, 1968)."
  - "VSA-notatie is niet bedoeld als vervanging van historische neumennotaties, maar als een formeel definieerbare variant van de vereenvoudigde praktijk in Nederlandse orthodoxe parochies."
formPhrases:
  - vsa-notatie
  - vsa-notaties
---

# VSA-notatie

**VSA-notatie** is het tekstgebaseerde notatieformaat dat VSA gebruikt om liturgische zangteksten op te schrijven. Het is een formeel gespecificeerde taal met scopes, modifiers en bracket-directives, waarmee de melodische structuur, accentuering en stemverdeling van een [zangstuk](@) eenduidig vastgelegd kunnen worden.

Een bestand in VSA-notatie is een [vsa-bestand](@): het heeft de extensie `.vsa`, is een [bronbestand](@) in de [bron-repository](@) en fungeert als [representatie](@) van een [uitvoeringsvorm](@). [Afgeleiden](@) zoals `.svg` (notenbalken) en `.mxl` (MusicXML) worden door de [vsa-tooling](@) uit dit bronbestand gegenereerd.

## Kernprincipes

VSA-notatie is ontworpen om:

- eenvoudig te leren te zijn voor zangers zonder gespecialiseerde notatiekennis;
- aan te sluiten bij de notatiepraktijk uit het Nederlandse Liturgikon (Den Haag, 1968);
- formeel definieerbaar te zijn in een grammatica, zodat ze betrouwbaar parseerbaar en valideerbaar is;
- bruikbaar te zijn in tekstgebaseerde en geautomatiseerde workflows;
- voldoende semantische informatie te bevatten voor conversie naar MusicXML.

## Motivatie

Orthodoxe zangteksten hebben specifieke eigenschappen — accentpatronen, toonsoorten, stemverdelingen — die gangbare notatieformaten (MusicXML, ABC, LilyPond) niet rechtstreeks en compact kunnen uitdrukken. Tegelijk bestaat er in Nederlandse orthodoxe parochies al een notatiepraktijk die aansluit bij het Liturgikon, maar die niet gestandaardiseerd of formeel gedocumenteerd was.

VSA-notatie formaliseert die praktijk: door een expliciete grammatica te definiëren, kunnen bestanden automatisch worden gevalideerd, gerenderd en geconverteerd. Dat maakt reproduceerbare, foutarme publicatie van [representaties](@) mogelijk zonder handmatig omzetten.

## Zie ook:

- [VSA-demo](https://orthodox-ronl.github.io/VSA-demo/)
- [GitHub orthodox-ronl/VSA-tooling](https://github.com/orthodox-ronl/VSA-tooling)
