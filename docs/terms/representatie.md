---
termid: representatie-van-uitvoeringsvorm
term: representatie
formPhrases:
  - representatie
  - representaties
glossaryTerm: Representatie
glossaryText: "Een bestand waarin een [uitvoeringsvorm](@) concreet is vastgelegd."
glossaryNotes:
  - "Vormen: [vsa-notatie](@), scan van een partituur, MusicXML/MXL als bron, audio, e.d."
  - "Onderscheid van [afgeleide](@): `.svg` of `.mxl` die een tool volledig uit een [bronbestand](@) herhaalt, is een [afgeleide](@), geen representatie."
  - "Onder dezelfde [uitvoeringsvorm](@) mogen meerdere representaties bestaan (bijv. scan + getrouwe [vsa-bestand](@))."
---

# Representatie

Een **representatie** is een bestand waarmee een [uitvoeringsvorm](@) concreet is
vastgelegd — bijvoorbeeld een [vsa-bestand](@), een scan, of MusicXML als bron.

| Status      | Voorbeeld                                                                                                            |
| ----------- | -------------------------------------------------------------------------------------------------------------------- |
| Ja          | `hemelum.vsa`; Liturgikon-scan (PDF/JPG); inline VSA-blok (tot extractie)                                            |
| Nee         | Abstract [zangstuk](@); `melodie.svg` ([afgeleide](@)); [manifest](@) zonder [bronbestand](@)                        |
| Nee         | Tweede melodie Cherubijnenhymne → andere [variant](@), geen tweede representatie onder dezelfde [uitvoeringsvorm](@) |
| Randgeval   | Identieke `.vsa` met twee `representatie-id`s → duplicaat; vermijden                                                 |

## Motivatie

Zonder representatie kun je een [uitvoeringsvorm](@) niet concreet bewaren,
delen of omzetten. Met een representatie kun je:

- een partituur of notatie vastleggen die bij een uitvoering past;
- meerdere bronnen van *dezelfde* uitvoeringsvorm naast elkaar houden (scan én
  transcriptie);
- [afgeleiden](@) (SVG, oefen-MXL, …) produceerbaar maken via een
  [conversiemechanisme](@).

Gebruiksvormen zoals MuseScore (MusicXML) of Coria (oefenexport) horen bij
*wat je met een representatie of haar afgeleiden doet* — niet bij de definitie
van representatie zelf.

## Gerelateerd

- [uitvoeringsvorm](@), [variant](@), [zangstuk](@) — hogere niveaus
- [bronbestand](@) / [afgeleide](@) — opslag vs. gegenereerd
- [source-entry](@) — registratie in de [bron-repository](@)
- [Terminologie, paragraaf 8](../specs/terminologie.md#8-representatie)
