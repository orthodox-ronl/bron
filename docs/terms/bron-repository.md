---
term: bron-repository
formPhrases:
  - "bron-repositor{yies}"
  - "bron-repo{ss}"
glossaryTerm: Bron-repository
glossaryAlias: Bron-repo
glossaryText: "De git-repository `orthodox-groningen/bron` (of een expliciet aangewezen opvolger); de centrale opslagplaats voor [representaties](@) van [uitvoeringsvormen](@) (van [varianten](@)) van [zangstukken](@), alsmede voor de specificaties van de opslag, en van manieren om daarin te zoeken."
glossaryNotes:
  - "Niet verwarren met [bronbestand](@) (een bestand) of [herkomst](@) (metadata over oorsprong)."
  - "Repositories voor de [VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling/), of parochie-specifieke zaken en vendor-checkouts zijn geen bron-repository."
---

# Bron-repository

De **bron-repository** is de git-repository [`orthodox-groningen/bron`](https://github.com/orthodox-groningen/bron) — of een expliciet aangewezen opvolger. Het is de centrale opslagplaats voor [representaties](@) van [uitvoeringsvormen](@) (van [varianten](@)) van [zangstukken](@), alsmede voor de specificaties van de opslag, manieren om daarin te zoeken, handleidingen, enzovoorts.

| Status | Voorbeeld                                        |
| ------ | ------------------------------------------------ |
| Ja     | `github.com/orthodox-groningen/bron`             |
| Nee    | [VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling/); parochie-Hugo-repo; vendor-checkout |

Niet verwarren met [bronbestand](@) (een bestand in een repository) of [herkomst](@) (metadata over oorsprong).

## Motivatie

Meerdere partijen — parochies, tools, CI-pipelines — werken met hetzelfde muzikale materiaal. Er moet één duidelijke centrale bron zijn die als autoriteit fungeert en waaruit anderen putten. Door 'bron-repository' als term te definiëren, is altijd eenduidig welke repo leidend is, ook als er vendor-checkouts, mirrors of forks bestaan.

De term voorkomt ook verwarring met het alledaagse woord "bron": in deze terminologie betekent "bron" altijd ofwel [bronbestand](@) (een bestand) of bron-repository (deze repo), nooit zomaar "ergens vandaan" — dat is [herkomst](@).

Zie ook: [Terminologie, paragraaf 12](../specs/terminologie.md#12-bron-repository).
