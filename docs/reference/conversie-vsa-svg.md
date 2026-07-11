# Conversie: vsa svg

Contract voor het conversiemechanisme **`vsa svg`**: VSA-bron (`.vsa`) naar
scalable vector graphics (`.svg`).

---

## Samenvatting

`vsa svg` leest een gevalideerd [vsa-bestand](@) en schrijft een SVG met VSA-glyphs,
omringende tekst en layout volgens [VSA-tooling](@) rendering. De SVG is input voor
exporttype [embed svg](exporttype-svg.md) en voor static assets op de site.

---

## Wanneer gebruiken

| Scenario            | Aanroep                                                                     |
| ------------------- | --------------------------------------------------------------------------- |
| Lokaal preview      | Handmatig na wijziging `.vsa`                                               |
| CI / parochie-build | Batch over content-source (doel: expliciete job vóór Hugo)                  |
| Inline (huidig)     | Automatisch tijdens `build-markdown` bij `::: vsa-notatie` / `.vsa` include |

---

## Commando en aanroep

### Enkel bestand

```cmd
vsa svg pad\naar\melodie.vsa pad\naar\melodie.svg
```

### Typische mapstructuur (lokaal)

```text
content-source/praktijk/melodie.vsa  →  derived/praktijk/melodie.svg
```

Output-locatie in parochie-build: `static/vsa/` of CI-artefact; URL-prefix `/vsa`.

---

## Invoer

| Veld             | Vereiste                                           |
| ---------------- | -------------------------------------------------- |
| Bestand          | `.vsa`, UTF-8                                      |
| Validatie        | Moet slagen op `vsa validate` vóór betrouwbare SVG |
| Frontmatter      | Optioneel; metadata kan rendering beïnvloeden      |
| Omringende tekst | Onderdeel van `.vsa`-body                          |

---

## Opties / flags

De CLI `vsa svg` accepteert primair input- en outputpad. Rendering-opties
(max line width, fonts) worden via [VSA-tooling](@) config / build-markdown parameters
gezet in site-build — niet alle flags zijn op CLI-niveau per bestand.

| Parameter (build)       | Doel                      | Typische waarde            |
| ----------------------- | ------------------------- | -------------------------- |
| `max_line_width`        | SVG-breedte wrapping      | `800` (site-build default) |
| `svg_assets_dir`        | Waar SVG wordt gekopieerd | `generated/vsa/static/vsa` |
| `svg_assets_url_prefix` | URL in HTML               | `/vsa`                     |

!!! note "CLI vs. build"
    Gedetailleerde flag-lijst staat in [VSA-tooling](@) `--help` en architecture docs;
    dit contract beschrijft gedrag relevant voor bronbeheerders.

---

## Validatie vóór conversie

| Check              | Tool           | Blokkeert?         |
| ------------------ | -------------- | ------------------ |
| Parse              | `vsa validate` | Ja                 |
| Semantiek VSA      | Zelfde         | Ja                 |
| Ontbrekend bestand | CLI            | Ja — exit code ≠ 0 |

Bij `build-markdown` faalt de hele build bij invalid `.vsa`.

---

## Uitvoer

| Veld         | Waarde                                                       |
| ------------ | ------------------------------------------------------------ |
| Formaat      | SVG 1.x, `width`/`viewBox` voor schaling                    |
| Inhoud       | [VSA-notatie](@) + tekst; geen audio                        |
| Bestandsnaam | Meestal `{stem}.svg` naast `{stem}.vsa`                     |
| Versie       | Gekoppeld aan [VSA-tooling](@) release / git ref in CI      |

---

## Downstream (export)

| Exporttype               | Gebruik                           |
| ------------------------ | --------------------------------- |
| [svg](exporttype-svg.md) | Embed in samenstelling            |
| Direct `.svg` include    | Kopie naar static zonder VSA-blok |

---

## Fouten en oplossingen

| Probleem          | Oorzaak          | Oplossing                                        |
| ----------------- | ---------------- | ------------------------------------------------ |
| Validatiefout     | Syntax in `.vsa` | `vsa validate`; [vsa-notatie](@) spec raadplegen |
| Lege SVG          | Lege body        | Inhoud toevoegen                                 |
| Verkeerde glyphs  | Font/config      | [VSA-tooling](@) versie alignen met CI           |
| Breedte op afdruk | Te brede SVG     | `scale` in export of `max_line_width`            |

---

## Open punten (TBD)

- Expliciete CI-job alleen conversie (los van Hugo)
- Cache: alleen opnieuw converteren bij gewijzigde `.vsa`
- Documentatie alle CLI-flags in dit contract

---

## Gerelateerd

- [Exporttype svg](exporttype-svg.md)
- [Conversiemechanismen — overzicht](conversiemechanismen.md)
