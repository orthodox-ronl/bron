---
term: bronbestand
formPhrases:
  - bronbestanden
  - bronbestand
glossaryTerm: Bronbestand
glossaryText: "Een bestand waarvoor geen geautomatiseerd, herhaalbaar [conversiemechanisme](@) bestaat dat het volledig uit een ander getrackt bestand in dezelfde repository genereert."
glossaryNotes:
  - "Voor het opnemen van bronbestanden in de [bron-repo](@) is dus altijd tenminste één handmatige actie vereist."
  - heading: "Voorbeelden van bronbestanden:"
    items:
      - "handmatig geschreven `.vsa` bestanden."
      - "gescande documenten (met extensies als `.tif`, `.jpg`, `.pdf` e.d.)"
      - "MusicXML of MXL bestanden die door een programma als MuseScore zijn gemaakt"
      - "Een `.coria.html` bestand zoals je die door `https://coria.nl/` kunt laten maken (en dan in de repo zetten)"
  - heading: "Voorbeelden van [afgeleiden](@) (dat zijn per definitie GEEN bronbestanden):"
    items:
      - "`.svg` bestanden die middels de [vsa tool](@) zijn gegenereerd."
      - "HTML bestanden zoals die zijn gegenereerd uit geautomatiseerde workflows."
---

# Bronbestand

Een **bronbestand** is een bestand waarvoor in de repository geen geautomatiseerd, herhaalbaar [conversiemechanisme](@) bestaat dat het volledig uit een ander getrackt bestand genereert.

Bronbestanden worden wél getrackt in git; bestanden die volledig mechanisch worden gegenereerd zijn [afgeleiden](@).

| Status    | Voorbeeld                                                                        |
| --------- | -------------------------------------------------------------------------------- |
| Ja        | handmatig `.vsa`; scan-PDF; MusicXML uit MuseScore                               |
| Nee       | `.svg` na `vsa svg`; gegenereerde Hugo-pagina                                    |
| Randgeval | `.coria.html` naast `.vsa` → voorlopig bronbestand; herbeoordelen bij Coria-spec |

## Motivatie

De build-pipeline moet weten welke bestanden *ingevoerd* worden en welke *gegenereerd* worden. Bronbestanden gaan in git en zijn de stabiele basis; [afgeleiden](@) worden elke build opnieuw aangemaakt uit die basis.

Door dit criterium formeel te definiëren, vermijden we dat gegenereerde bestanden per ongeluk getrackt worden — dat levert onnodige diffs, merge-conflicten en onduidelijkheid op over welke versie leidend is. Tegelijk weten tools en beheerders precies wat zij als betrouwbare input mogen beschouwen.

Zie ook: [Terminologie, paragraaf 10](../specs/terminologie.md#10-bronbestand).
