---
termid: vsa
term: vsa
termType: concept
glossaryTerm: "Vereenvoudigde Slavische Accentnotatie"
glossaryAbbr: VSA
glossaryText: "Overkoepelend begrip voor zowel de [vsa-notatie](@) (het notatieformaat voor liturgische zangteksten) als de [vsa-tooling](@) (de CLI en toolchain voor validatie en publicatie)."
glossaryNotes:
  - "Gebruik [vsa-notatie](@) als je specifiek de notatiesyntaxis bedoelt, en [vsa-tooling](@) als je de tools bedoelt."
  - "Een `.vsa`-bestand is een [bronbestand](@) en tevens een [representatie](@) van een [uitvoeringsvorm](@)."
formPhrases:
  - vsa
---

# VSA — Vereenvoudigde Slavische Accentnotatie

**VSA** (Vereenvoudigde Slavische Accentnotatie) is een overkoepelend begrip dat twee samenhangende onderdelen omvat:

- **[VSA-notatie](@)** — de notatie-taal waarmee liturgische zangteksten worden opgeschreven in een formeel, machine-leesbaar formaat.
- **[VSA-tooling](@)** — de CLI en toolchain waarmee `.vsa`-bestanden worden gevalideerd en omgezet naar publicatievormen (SVG, MusicXML).

Een `.vsa`-bestand is een [bronbestand](@) in de [bron-repository](@) en fungeert als [representatie](@) van een [uitvoeringsvorm](@). Uit dat bestand worden via [conversiemechanismen](@) in de [vsa-tooling](@) [afgeleiden](@) gegenereerd.

## Motivatie

De afkorting VSA wordt in de praktijk gebruikt voor zowel het notatieformaat ("schrijf het in VSA") als voor de tooling ("draai [`vsa validate`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/validate/)"). Door VSA als parapluterm te definiëren met twee sub-termen, wordt die dubbelzinnigheid opgelost: documentatie, code-commentaar en issues kunnen de juiste specifieke term gebruiken.

Zie ook: [VSA-demo](https://orthodox-ronl.github.io/VSA-demo/), [vsa-notatie](vsa-notatie.md), [vsa-tooling](vsa-tooling.md).
