---
term: vsa-tooling
termType: concept
glossaryTerm: "VSA-tooling"
glossaryText: "De Python-toolchain (`vsa` CLI) waarmee [vsa-notatie](@)-bestanden worden geparseerd, gevalideerd en omgezet naar [afgeleiden](@) zoals SVG en MusicXML."
glossaryNotes:
  - "De `vsa`-CLI biedt subcommando's voor validatie, rendering en export; zie de [CLI-referentie](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/reference/cli/index.md)."
  - "VSA-tooling genereert [afgeleiden](@) uit [bronbestanden](@); de [afgeleiden](@) zelf worden niet in de [bron-repository](@) opgeslagen."
  - "De tooling bevindt zich in de repo [orthodox-groningen/VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling)."
formPhrases:
  - vsa-tooling
  - vsa-tool
  - vsa-tools
---

# VSA-tooling

**VSA-tooling** is de Python-toolchain voor het verwerken van
[VSA-notatie](@)-bestanden. De kern is de `vsa` CLI: die parseert, valideert en
zet [vsa-bestanden](@) om naar [afgeleiden](@) (bijv. `.svg`, `.mxl`). Die
afgeleiden worden **niet** in de [bron-repository](@) bewaard, maar bij de build
opnieuw gemaakt.

Volledige commando’s, opties en voorbeelden:
[CLI-referentie (`vsa`)](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/reference/cli/index.md).

## Wat je ermee doet

| Doel                         | Typisch subcommando   |
| ---------------------------- | --------------------- |
| Controleren of VSA klopt     | `validate`            |
| Notatie als plaatje (SVG)    | `svg`                 |
| MusicXML voor MuseScore/Coria| `musicxml`            |
| Documenten voor de site bouwen | `build-markdown`    |
| `zoek=` in markdown oplossen | `resolve-catalogus`   |

VSA-tooling is een [conversiemechanisme](@): het zet bronbestanden om naar
afgeleiden. Org-contracten (wat/wanneer):
[conversiemechanismen](../reference/conversiemechanismen.md).

## Installatie (kort)

```cmd
cd /d C:\Git\orthodox-groningen\VSA-tooling
scripts\bootstrap.cmd
```

Daarna kun je in de [bron-repository](@) valideren:

```cmd
cd /d C:\Git\orthodox-groningen\bron
vsa validate zangstukken
```

Details: [CLI-overzicht](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/reference/cli/index.md).

## Motivatie

[VSA-notatie](@)-bestanden zijn tekst die mensen schrijven. Zonder tooling is er
geen garantie dat ze syntactisch kloppen, en is omzetten naar SVG of MusicXML
handmatig en foutgevoelig. VSA-tooling maakt dat automatisch en
reproduceerbaar — elke build genereert afgeleiden opnieuw uit de getrackte
bronbestanden. In CI valideert `vsa validate zangstukken` bij push of PR.

## Zie ook

- [CLI-referentie](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/reference/cli/index.md)
- [VSA-demo](https://orthodox-groningen.github.io/VSA-demo/)
- [GitHub orthodox-groningen/VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling)
