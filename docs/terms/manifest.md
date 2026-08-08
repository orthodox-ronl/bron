---
term: manifest
formPhrases:
  - manifesten
  - manifest
glossaryTerm: Manifest
glossaryText: "Een YAML-bestand met vaste bestandsnaam (`variant.yaml` of `uitvoeringsvorm.yaml`) dat precies één entiteit op [variant](@)- of [uitvoeringsvorm](@)-niveau registreert en uitsluitend metadata over die entiteit beschrijft."
glossaryNotes:
  - "Niet verwarren met npm-package-manifest, PWA-manifest, CI-build-manifest of andere generieke gebruiken van het woord *manifest*."
  - "`zangstuk.yaml` in de [bron-repository](@) is geen manifest — dat volgt het [source-entry](@)-model."
  - "Een manifest is zelf geen [representatie](@), [bronbestand](@) of [samenstelling](@)."
---

# Manifest

Een **manifest** is een YAML-bestand met een vaste bestandsnaam op [variant](@)- of [uitvoeringsvorm](@)-niveau binnen het vier-niveaumodel, dat precies één entiteit registreert via het bijbehorende id-veld en uitsluitend metadata beschrijft: titels, aliassen, [herkomst](@), `based_on`, verwijzingen naar [representaties](@).

| Niveau          | Bestandsnaam           | Id-veld in yaml      |
| --------------- | ---------------------- | -------------------- |
| Variant         | `variant.yaml`         | `variant-id`         |
| Uitvoeringsvorm | `uitvoeringsvorm.yaml` | `uitvoeringsvorm-id` |

Op [uitvoeringsvorm](@)-niveau mag een manifest [representaties](@) **verwijzen** (`representaties:` met `representatie-id` en relatief `file:`), zonder zelf notatie te bevatten.

| Status    | Voorbeeld                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------ |
| Ja        | `lokaal/…/liturgikon-weekdagen/variant.yaml`                                                     |
| Ja        | `lokaal/…/hemelum/uitvoeringsvorm.yaml` met `representaties: [{ representatie-id: hemelum, … }]` |
| Nee       | `hemelum.vsa` ([bronbestand](@) / [representatie](@))                                            |
| Nee       | `zangstuk.yaml` in [bron-repository](@) ([source-entry](@)-model)                                |
| Nee       | `antifonen-hemelum.md` ([samenstelling](@))                                                      |
| Nee       | npm `package.json`, PWA manifest, CI build-manifest                                              |
| Randgeval | Manifest zonder representatie-verwijzing — [uitvoeringsvorm](@) met 0 [representaties](@)        |

## Motivatie

Het vier-niveaumodel vereist machine-leesbare metadata op [variant](@)- en [uitvoeringsvorm](@)-niveau: titels in meerdere talen, aliassen voor de alias-resolver, [herkomst](@), `based_on`-relaties. Die metadata heeft een vaste, voorspelbare locatie nodig zodat tooling haar kan inlezen zonder ad-hoc zoeklogica.

Een manifest biedt precies dat: een vaste bestandsnaam, één entiteit per bestand, uitsluitend metadata. De scheiding van [bronbestand](@) en [samenstelling](@) is bewust: een manifest beschrijft, het registreert niet zelf muziek en ordent niet voor een lezer.

Zie ook: [Terminologie, paragraaf 16](../specs/terminologie.md#16-manifest).
