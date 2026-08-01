# Conversie: vsa musicxml

Contract voor het conversiemechanisme **`vsa musicxml`**: VSA-bron (`.vsa`) naar
MusicXML (`.mxl` of `.musicxml`).

---

## Samenvatting

`vsa musicxml` zet VSA-notatie om naar MusicXML voor MuseScore, Coria
(`play_from_url`) en exporttype [mxl-download](exporttype-mxl.md) /
[coria](exporttype-coria.md) (MXL-modus). Muziek-metadata in VSA-frontmatter
wordt aanbevolen voor titel, toonsoort en tempo.

---

## Wanneer gebruiken

| Scenario                  | Aanroep                                              |
| ------------------------- | ---------------------------------------------------- |
| MuseScore bewerken        | Handmatig `.mxl` genereren                           |
| Coria zonder HTML-sibling | MXL publiceren + `:::coria` met `mode=auto` of `mxl` |
| CI                        | Batch over `content-source` (deels in site-build)    |

---

## Commando en aanroep

### Enkel bestand (default `.mxl`)

```cmd
vsa musicxml mijn-lied.vsa mijn-lied.mxl
```

Zonder extensie op output → `.mxl`:

```cmd
vsa musicxml mijn-lied.vsa output\mijn-lied
```

### Platte MusicXML

```cmd
vsa musicxml mijn-lied.vsa mijn-lied.musicxml
```

of:

```cmd
vsa musicxml mijn-lied.vsa mijn-lied --format musicxml
```

### Map-batch

```cmd
vsa musicxml content-source\praktijk output\mxl
```

Eén `.mxl` per `.vsa` in de map.

Uitgebreide gebruikersdoc:
[MusicXML-export (VSA-tooling)](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/guides/musicxml-export.md).

---

## Invoer

| Veld           | Vereiste                                          |
| -------------- | ------------------------------------------------- |
| Bestand        | `.vsa`, UTF-8                                     |
| Validatie      | `vsa validate` aanbevolen vóór conversie          |
| Frontmatter    | Aanbevolen: titel, toon, tempo voor bruikbare MXL |
| Notatie-inhoud | Moet musicXML-exporteerbare structuren bevatten   |

---

## Opties / flags

### `--format`

| Veld           | Waarde                                                        |
| -------------- | ------------------------------------------------------------- |
| **Verplicht?** | Nee                                                           |
| **Standaard**  | `mxl` (gecomprimeerd)                                         |
| **Waarden**    | `mxl`, `musicxml`                                             |
| **Doel**       | `.mxl` voor distributie; `.musicxml` voor debugging/MuseScore |
| **Effect**     | Output-extensie en compressie                                 |

### Exportprofiel (playback vs. engraving)

Standaardprofiel in tooling: **`playback`** (geschikt voor Coria).

| Profiel     | Doel              | Wanneer                                  |
| ----------- | ----------------- | ---------------------------------------- |
| `playback`  | Afspelen, oefenen | Coria, online                            |
| `engraving` | Notatie-layout    | MuseScore bewerking (indien ondersteund) |

Raadpleeg `vsa musicxml --help` voor actuele profiel-flag (`--profile`).

---

## Validatie vóór conversie

| Check                   | Blokkeert?                                           |
| ----------------------- | ---------------------------------------------------- |
| `vsa validate`          | Aanbevolen; invalid `.vsa` geeft slechte of geen MXL |
| Ontbrekend inputbestand | Ja — CLI error                                       |

Export-resolve valideert MXL-inhoud **niet** op build-time.

---

## Uitvoer

| Veld              | Waarde                               |
| ----------------- | ------------------------------------ |
| Default           | `.mxl` (ZIP met MusicXML)            |
| Alternatief       | `.musicxml` plat XML                 |
| Locatie lokaal    | `derived/` of door gebruiker gekozen |
| Public URL (site) | `/vsa/mxl/{relatief-pad}.mxl`        |

---

## Downstream (export)

| Exporttype                   | Gebruik                                   |
| ---------------------------- | ----------------------------------------- |
| [mxl](exporttype-mxl.md)     | Downloadlink                              |
| [coria](exporttype-coria.md) | `mode=mxl` of `auto` zonder `.coria.html` |

---

## Fouten en oplossingen

| Probleem                 | Oorzaak                 | Oplossing                       |
| ------------------------ | ----------------------- | ------------------------------- |
| Lege of minimale MXL     | Weinig muziek in `.vsa` | Notatie uitbreiden              |
| Verkeerde toon in speler | Metadata ontbreekt      | Frontmatter / `zangstuk.yaml`   |
| MuseScore layout vreemd  | playback-profiel        | `--profile engraving` proberen  |
| Coria laadt niet         | MXL niet op server      | Static deploy + URL controleren |

---

## Open punten (TBD)

- Automatisch MXL kopiëren in alle parochie-builds
- Validatie well-formed XML in CI
- Volledige profiel-matrix in dit contract

---

## Gerelateerd

- [Exporttype mxl](exporttype-mxl.md)
- [Exporttype coria](exporttype-coria.md)
- [Conversiemechanismen — overzicht](conversiemechanismen.md)
