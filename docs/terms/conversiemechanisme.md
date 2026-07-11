---
term: conversiemechanisme
formPhrases:
  - conversiemechanismen
  - conversiemechanisme
glossaryTerm: Conversiemechanisme
glossaryText: "Een gedefinieerde, geautomatiseerde en herhaalbare tool CM die een [bronbestand](@) B omzet naar een [afgeleide](@) AB = CM(B)."
glossaryNotes:
  - "Voorbeelden: `vsa svg` (VSA → SVG), `vsa musicxml` (VSA → MXL)."
  - "Het bestaan van een conversiemechanisme is het criterium waarmee onderscheid wordt gemaakt tussen [bronbestand](@) en [afgeleide](@)."
---

# Conversiemechanisme

Een **conversiemechanisme** is een gedefinieerde, geautomatiseerde en herhaalbare tool M die een [bronbestand](@) B volledig omzet naar een [afgeleide](@) G, zodat M(B) = G.

Het bestaan van een conversiemechanisme is precies het criterium waarmee [bronbestand](@) en [afgeleide](@) worden onderscheiden: bestaat zo'n mechanisme voor G, dan is G een [afgeleide](@) en geen [bronbestand](@).

| Bronbestand | Conversiemechanisme | Afgeleide |
| ----------- | ------------------- | --------- |
| `.vsa`      | `vsa svg`           | `.svg`    |
| `.vsa`      | `vsa musicxml`      | `.mxl`    |

## Motivatie

Het onderscheid tussen [bronbestand](@) en [afgeleide](@) draait volledig om de vraag: bestaat er een geautomatiseerd, herhaalbaar mechanisme om dit bestand te genereren? Door 'conversiemechanisme' formeel te definiëren, wordt dat criterium concreet en toetsbaar — ook voor tooling die automatisch kan controleren of een bestand terecht als afgeleide is aangemerkt.

Tegelijk wordt duidelijk wat de rol van de VSA-tooling is: zij levert de [conversiemechanismen](@) (`vsa svg`, `vsa musicxml`) die van [bronbestanden](@) in de [bron-repository](@) [afgeleiden](@) maken ten behoeve van publicatie.

Zie ook: [Terminologie, paragraaf 20](../specs/terminologie.md#20-conversiemechanisme-exportmechanisme-exporttype), [afgeleide](@), [bronbestand](@).
