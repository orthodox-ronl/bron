# Exporttype: Coria

Contract voor het **coria**-exporttype: link of ingebedde speler naar
[Coria](https://coria.nl) voor online oefenen.

---

## Samenvatting

Exporttype **coria** voegt een knop of link toe waarmee de lezer de melodie in
Coria kan openen — met vooraf gekozen partij (Coria-HTML sibling) of via MusicXML
deep-link (`play_from_url`). De `.vsa`-bron moet bestaan; MXL of HTML moet
bereikbaar zijn op de gepubliceerde site.

---

## Beoogde doelen

- **Online oefenen** tijdens repetitie of thuis
- Partij al vastgelegd in Coria-export (HTML-modus)
- Fallback naar MXL wanneer geen handmatige Coria-HTML beschikbaar is
- **Niet:** afdrukken (verberg via CSS `.coria-play` of `web-only`)

---

## Authoring

### Doelsyntax (gepland)

```markdown
:::include coria "praktijk/zondagen/tropaar-zondag-toon-3.vsa" label="Oefenen in Coria" mode="auto":::
```

### Huidige equivalent (geïmplementeerd)

```markdown
:::coria "praktijk/zondagen/tropaar-zondag-toon-3.vsa" label="Oefenen in Coria" mode="auto":::
```

`:::coria` en `:::include coria` zijn functioneel gelijk zodra de alias is
geïmplementeerd.

### Handmatige sibling (optioneel)

```text
praktijk/zondagen/tropaar-zondag-toon-3.vsa
praktijk/zondagen/tropaar-zondag-toon-3.coria.html
```

Exporteer `.coria.html` vanuit Coria na partijkeuze; build kopieert naar
`static/coria/…/tropaar-zondag-toon-3.html`.

---

## Parameters

### `pad` (eerste argument)

| Veld                   | Waarde                                                               |
| ---------------------- | -------------------------------------------------------------------- |
| **Verplicht?**         | Ja                                                                   |
| **Type**               | Relatief pad naar `.vsa`                                             |
| **Doel**               | Anker voor sibling `{stem}.coria.html` en MXL-URL-afleiding          |
| **Toegestane waarden** | Bestaand `.vsa`-bestand onder content-root                           |
| **Verboden**           | Ontbrekend bestand, geen `.vsa`-extensie, pad buiten content-root   |
| **Effect**             | Bepaalt URL-paden `/coria/…` of `/vsa/mxl/…`                         |
| **Voorbeeld ongeldig** | `"ontbreekt.vsa"` → `CoriaDirectiveError: VSA-bestand niet gevonden` |

### `label`

| Veld                   | Waarde                                                |
| ---------------------- | ----------------------------------------------------- |
| **Verplicht?**         | Nee                                                   |
| **Type**               | String: `label="…"`                                   |
| **Standaard**          | `"Oefenen in Coria"`                                  |
| **Doel**               | Zichtbare linktekst op de pagina                      |
| **Toegestane waarden** | Willekeurige tekst                                    |
| **Effect**             | Doorgegeven aan Hugo shortcode `coria` / `coria-html` |
| **Voorbeeld**          | `label="Tropaar oefenen (Toon 3)"`                    |

### `mode`

| Veld           | Waarde                                            |
| -------------- | ------------------------------------------------- |
| **Verplicht?** | Nee                                               |
| **Type**       | Enum: `auto`, `html`, `mxl`                       |
| **Standaard**  | `auto`                                            |
| **Doel**       | Kiezen tussen Coria-HTML sibling en MXL deep-link |

#### Waarden `mode`

| Waarde | Gedrag                                           | Wanneer gebruiken                                 |
| ------ | ------------------------------------------------ | ------------------------------------------------- |
| `auto` | HTML als `{stem}.coria.html` bestaat, anders MXL | Standaard; minste configuratie                    |
| `html` | Alleen Coria-HTML                                | Partij moet vast staan; geen MXL-fallback gewenst |
| `mxl`  | Alleen MXL-URL via Coria `play_from_url`         | Geen HTML-sibling; MXL gepubliceerd               |

| Waarde     | Verboden / fout                                             |
| ---------- | ----------------------------------------------------------- |
| `html`     | Geen sibling → `ContentAssetError: Geen Coria-HTML naast …` |
| `mxl`      | MXL niet op site → 404 in Coria (runtime)                   |
| `onbekend` | `CoriaDirectiveError: Onbekende coria mode`                 |

**Effect in HTML:**

- HTML-modus → shortcode `{{< coria-html src="/coria/…" >}}`
- MXL-modus → shortcode `{{< coria src="/vsa/mxl/…" >}}`

---

## Inputs

| Input                       | Vereist?     | Opmerking                                                      |
| --------------------------- | ------------ | -------------------------------------------------------------- |
| `.vsa`                      | Ja           | Moet bestaan; wordt **niet** opnieuw gevalideerd in coria-pass |
| `{stem}.coria.html`         | Conditioneel | Voor `mode=html` of `auto` met sibling                         |
| `.mxl` op gepubliceerde URL | Conditioneel | Voor `mode=mxl` of `auto` zonder sibling                       |

MXL wordt **niet** tijdens coria-resolve gegenereerd; conversie
([conversie-vsa-musicxml](conversie-vsa-musicxml.md)) moet eerder gedraaid hebben
en build moet MXL naar static kopiëren (deels gepland).

---

## Validatie vóór export

| Check                        | Moment        | Blokkeert?                              |
| ---------------------------- | ------------- | --------------------------------------- |
| `.vsa` bestaat               | coria-resolve | Ja                                      |
| `.vsa` onder content-root    | pad-resolve   | Ja — `Bestand ligt buiten content-root` |

**Catalogus-pad `bron:`:** na **`vsa resolve-catalogus`** wijst de include naar een `.vsa` in
org-bron (buiten parochie `--content-root`). Coria-export faalt dan bij build; **svg** op
hetzelfde catalogus-pad werkt wel. Zie [catalogus-samenstelling-zangstuk](../specs/catalogus-samenstelling-zangstuk.md).
| `mode=html` + sibling        | coria-resolve | Ja                                      |
| VSA-inhoud semantisch geldig | —             | **Nee** in huidige coria-pass           |
| MXL bereikbaar               | runtime       | Nee bij build; wel 404 voor gebruiker   |

---

## Build-gedrag

1. **Include-resolutie** (vóór coria)
2. **Coria-resolve** — `resolve_coria_directives` → Hugo shortcode
3. Bij HTML: kopieer `.coria.html` naar `static/coria/…`
4. Hugo rendert shortcode naar Coria-link/speler

URL-prefixen (defaults):

| Asset      | Default prefix |
| ---------- | -------------- |
| MXL        | `/vsa/mxl`     |
| Coria HTML | `/coria`       |

---

## Output

| Modus | Eindgebruiker                               |
| ----- | ------------------------------------------- |
| HTML  | Opent statische Coria-export (partij vast)  |
| MXL   | Opent Coria met `play_from_url` naar `.mxl` |

Verberg op afdruk: CSS class `.coria-play` of plaats directive in `:::web-only`.

---

## Geschikt / niet geschikt

| Geschikt                    | Niet geschikt                |
| --------------------------- | ---------------------------- |
| Online uitgave, oefenen     | Afdrukboek zonder interactie |
| Gemeente met Coria-licentie | Offline-only distributie     |

---

## Fouten en oplossingen

| Melding                     | Oorzaak                             | Oplossing                                  |
| --------------------------- | ----------------------------------- | ------------------------------------------ |
| `VSA-bestand niet gevonden` | Pad typo                            | Pad t.o.v. `.md` corrigeren                |
| `Geen Coria-HTML naast …`   | `mode=html` zonder sibling          | Sibling toevoegen of `mode=auto`/`mxl`     |
| `Onbekende coria mode`      | Typo in mode                        | `auto`, `html`, of `mxl`                   |
| Coria 404 op MXL            | MXL niet gepubliceerd               | `vsa musicxml` + static deploy             |
| Lege speler                 | Verkeerde URL-prefix in site-config | Hugo `baseURL` en static-paden controleren |

---

## Open punten (TBD)

- `:::include coria` alias in `markdown_include.py`
- Automatisch MXL kopiëren naar static in alle builds
- VSA re-validatie optioneel vóór Coria-export
- Documentatie Coria-licentie / parochie-instellingen

---

## Gerelateerd

- [Conversie vsa musicxml](conversie-vsa-musicxml.md)
- [Exporttype mxl](exporttype-mxl.md)
- [MusicXML-export (VSA-tooling)](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/user/musicxml-export.md)
