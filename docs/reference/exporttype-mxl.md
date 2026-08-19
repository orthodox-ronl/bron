---
doc_type: org-contract
audience: "P4 — Consumer-site builder; P1 — Parochie-docs-maintainer"
---
# Exporttype: MXL-download

Contract voor het **mxl**-[exporttype](@): downloadlink naar MusicXML (`.mxl`) voor
bewerking in MuseScore of als fallback voor Coria.

Technische resolver- en shortcode-details: zie
[MusicXML exporteren](https://orthodox-ronl.github.io/VSA-tooling/guides/musicxml-export/)
en [CLI `vsa musicxml`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/musicxml/)
([VSA-tooling](@)).

---

## Samenvatting

[Exporttype](@) **mxl** plaatst een link in de [samenstelling](@) waarmee de lezer een
`.mxl`-bestand kan downloaden. Het bestand moet vooraf zijn gegenereerd via
[conversie-vsa-musicxml](conversie-vsa-musicxml.md) ([conversiemechanisme](@)) en
bereikbaar op de gepubliceerde site staan. De exportstap **genereert geen** MXL zelf
— dat is een [afgeleide](@).

---

## Beoogde doelen

- **Bewerking** in MuseScore of een andere MusicXML-editor
- Archief / uitwisseling met musici
- Optionele download naast Coria (online)
- **Niet:** inline notatie op papier (→ [svg](exporttype-svg.md))

---

## Authoring

### Doelsyntax (gepland)

```markdown
:::include mxl "praktijk/zondagen/tropaar-zondag-toon-3.vsa" label="Download MusicXML":::
```

### Huidige stand

`:::include mxl` is **nog niet overal geïmplementeerd**. URL-afleiding bestaat
al in de tooling; tot volledige implementatie: handmatige link naar gepubliceerde
MXL of wachten op afronding in [VSA-tooling](@).

---

## Parameters

### `pad` (eerste argument)

| Veld                   | Waarde                                                     |
| ---------------------- | ---------------------------------------------------------- |
| **Verplicht?**         | Ja                                                         |
| **Type**               | Relatief pad naar `.vsa`                                   |
| **Doel**               | Afleiden van de publicatie-URL van het bijbehorende `.mxl` |
| **Toegestane waarden** | Bestaand `.vsa` onder de content-root                      |
| **Verboden**           | Ontbrekend `.vsa`, pad buiten content-root                 |
| **Effect**             | Link wijst naar het MXL-pad (typisch `/vsa/mxl/…`)         |
| **Voorbeeld**          | `"praktijk/melodie.vsa"` → URL eindigend op `melodie.mxl`  |

### `label`

| Veld                   | Waarde                                                  |
| ---------------------- | ------------------------------------------------------- |
| **Verplicht?**         | Nee                                                     |
| **Type**               | String: `label="…"`                                     |
| **Standaard**          | TBD bij implementatie (voorstel: `"Download MusicXML"`) |
| **Doel**               | Linktekst voor de download                              |
| **Toegestane waarden** | Willekeurige tekst                                      |

---

## Inputs

| Input                 | Vereist?     | Opmerking                                                 |
| --------------------- | ------------ | --------------------------------------------------------- |
| `.vsa`                | Ja           | Anker voor URL-afleiding                                  |
| `.mxl` [afgeleide](@) | Ja (runtime) | Moet op de site staan; niet overal automatisch gekopieerd |

Sibling-conventie: `melodie.mxl` hoort bij `melodie.vsa` (zelfde stam, andere
extensie).

---

## Validatie (bedoeling)

| Check                  | Blokkeert build? | Toelichting                                      |
| ---------------------- | ---------------- | ------------------------------------------------ |
| `.vsa` bestaat         | Ja               | Pad moet kloppen                                 |
| Pad onder content-root | Ja               |                                                  |
| `.mxl` op schijf       | Nee (huidig)     | Build kan slagen terwijl download 404 geeft      |
| MXL well-formed        | Nee bij export   |                                                  |

!!! warning "Runtime vs. build"
    De build kan slagen terwijl de download 404 geeft als MXL niet is
    gegenereerd en gepubliceerd. CI moet conversie + static afdwingen (TBD).

---

## Wat de eindgebruiker ziet

| Profiel   | Resultaat                              |
| --------- | -------------------------------------- |
| Bewerking | Download `.mxl`, open in MuseScore     |
| Online    | Optionele extra link naast svg/coria   |

---

## Geschikt / niet geschikt

| Geschikt                    | Niet geschikt                       |
| --------------------------- | ----------------------------------- |
| MuseScore-bewerking         | Pixel-perfect afdruk van VSA-glyphs |
| Muzikale analyse buiten VSA | Inline weergave in liturgieboek     |

---

## Veelvoorkomende problemen (betekenis)

| Situatie                    | Typische oorzaak               | Richting oplossing                                                                                      |
| --------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| 404 op download             | MXL niet in static             | [`vsa musicxml`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/musicxml/) + publiceren |
| Verkeerde toonsoort in MXL  | Verkeerd conversieprofiel      | Zie [conversie musicxml](conversie-vsa-musicxml.md)                                                     |
| Verwacht een `.vsa`-bestand | Pad naar `.mxl` i.p.v. `.vsa`  | Eerste argument moet `.vsa` zijn                                                                        |

---

## Open punten (TBD)

- Volledige implementatie `:::include mxl` + Hugo-shortcode
- Build-kopie `.mxl` → static
- Validatie dat MXL bestaat vóór build (fail fast)
- `label`-default en toegankelijkheid

---

## Gerelateerd

- [Conversie vsa musicxml](conversie-vsa-musicxml.md)
- [Exporttype coria](exporttype-coria.md) (deelt MXL-URL)
- [CLI: `vsa musicxml`](https://orthodox-ronl.github.io/VSA-tooling/reference/cli/musicxml/)
