---
term: promotie
formPhrases:
  - promotie
  - registratie
glossaryTerm: Promotie (registratie)
glossaryText: "De overgang van een [parochie-lokale representatie](@) naar een [geregistreerde representatie](@), door het toevoegen van een [source-entry](@) en bijbehorend [bronbestand](@) in de [bron-repository](@) via een PR."
glossaryNotes:
  - "Bij promotie blijven de canonieke ids behouden."
  - "Promotie vereist een PR op de [bron-repository](@) met [source-entry](@) én [bronbestand](@)."
---

# Promotie

**Promotie** (ook: registratie) is de overgang van een [parochie-lokale representatie](@) naar een [geregistreerde representatie](@). Dit gebeurt door een [source-entry](@) — samen met het bijbehorende [bronbestand](@) — toe te voegen aan de [bron-repository](@) via een PR.

Bij promotie blijven de canonieke ids behouden.

| Status | Voorbeeld                                                                            |
| ------ | ------------------------------------------------------------------------------------ |
| Ja     | PR: `hemelum.vsa` + yaml `id: hemelum, based_on: liturgikon`                         |
| Nee    | Nieuw zangstuk-map terwijl extra [representatie](@) onder bestaand zangstuk volstaat |

## Motivatie

Er moet een duidelijk, herhaalbaar proces zijn voor de overgang van lokaal naar gedeeld. Zonder zo'n begrip blijft de grens tussen "lokaal experimenteren" en "bijdragen aan de gemeenschap" vaag, en weten beheerders niet wanneer materiaal stabiel genoeg is om op te vertrouwen.

Promotie formaliseert die stap: het is de expliciete handeling waarbij een parochie besluit haar [representatie](@) beschikbaar te stellen voor alle andere parochies, via de gecontroleerde route van een PR. Het behoud van canonieke ids bij promotie zorgt ervoor dat verwijzingen in bestaande [samenstellingen](@) en metadata geldig blijven.

Zie ook: [Terminologie, paragraaf 17](../specs/terminologie.md#17-promotie-registratie), [parochie-lokaal zangstukken](../manuals/parochie-lokaal-zangstukken.md).
