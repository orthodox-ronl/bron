---
doc_type: org-contract
audience: "P4 — Consumer-site builder; P1 — Parochie-docs-maintainer"
---
# Exporttype: Coria

Contract voor het **coria**-[exporttype](@): link of ingebedde speler naar
[Coria](https://coria.nl) voor online oefenen.

Technische build-details (shortcodes, static-mappen): zie
[MusicXML exporteren](https://orthodox-groningen.github.io/VSA-tooling/guides/musicxml-export/)
(sectie Coria) en de directives-specificatie in [VSA-tooling](@).

---

## Samenvatting

[Exporttype](@) **coria** voegt een knop of link toe waarmee de lezer de melodie in
Coria kan openen — met vooraf gekozen partij (Coria-HTML sibling) of via een
MusicXML deep-link. Het [vsa-bestand](@) moet bestaan; MXL of HTML moet
bereikbaar zijn op de gepubliceerde site. De link verschijnt in een
[samenstelling](@).

---

## Beoogde doelen

- **Online oefenen** tijdens repetitie of thuis
- Partij al vastgelegd in Coria-export (HTML-modus)
- Fallback naar MXL wanneer geen handmatige Coria-HTML beschikbaar is
- **Niet:** afdrukken (verberg via CSS of `web-only`)

---

## Authoring

### Doelsyntax

```markdown
:::include coria "praktijk/zondagen/tropaar-zondag-toon-3.vsa" label="Oefenen in Coria" mode="auto":::
```

### Huidige equivalent

```markdown
:::coria "praktijk/zondagen/tropaar-zondag-toon-3.vsa" label="Oefenen in Coria" mode="auto":::
```

`:::coria` en `:::include coria` zijn functioneel gelijk.

### Handmatige sibling (optioneel)

```text
praktijk/zondagen/tropaar-zondag-toon-3.vsa
praktijk/zondagen/tropaar-zondag-toon-3.coria.html
```

Exporteer `.coria.html` vanuit Coria na partijkeuze. De site-build plaatst die
naast de gepubliceerde assets (details in tooling).

---

## Parameters

### `pad` (eerste argument)

| Veld                   | Waarde                                                      |
| ---------------------- | ----------------------------------------------------------- |
| **Verplicht?**         | Ja                                                          |
| **Type**               | Relatief pad naar `.vsa`                                    |
| **Doel**               | Anker voor sibling `{stem}.coria.html` en MXL-URL-afleiding |
| **Toegestane waarden** | Bestaand `.vsa` onder de content-root                       |
| **Verboden**           | Ontbrekend bestand, geen `.vsa`-extensie, pad buiten root   |
| **Effect**             | Bepaalt welke Coria- of MXL-URL wordt gebruikt              |
| **Voorbeeld ongeldig** | `"ontbreekt.vsa"` → VSA-bestand niet gevonden               |

### `label`

| Veld                   | Waarde                             |
| ---------------------- | ---------------------------------- |
| **Verplicht?**         | Nee                                |
| **Type**               | String: `label="…"`                |
| **Standaard**          | `"Oefenen in Coria"`               |
| **Doel**               | Zichtbare linktekst op de pagina   |
| **Toegestane waarden** | Willekeurige tekst                 |
| **Voorbeeld**          | `label="Tropaar oefenen (Toon 3)"` |

### `mode`

| Veld           | Waarde                      |
| -------------- | --------------------------- |
| **Verplicht?** | Nee                         |
| **Type**       | Enum: `auto`, `html`, `mxl` |
| **Standaard**  | `auto`                      |
| **Doel**       | Coria-HTML sibling of MXL   |

#### Waarden `mode`

| Waarde | Gedrag                                           | Wanneer gebruiken                                 |
| ------ | ------------------------------------------------ | ------------------------------------------------- |
| `auto` | HTML als `{stem}.coria.html` bestaat, anders MXL | Standaard; minste configuratie                    |
| `html` | Alleen Coria-HTML                                | Partij moet vast staan; geen MXL-fallback gewenst |
| `mxl`  | Alleen MXL via Coria `play_from_url`             | Geen HTML-sibling; MXL is gepubliceerd            |

| Waarde     | Verboden / fout                                    |
| ---------- | -------------------------------------------------- |
| `html`     | Geen sibling → fout: geen Coria-HTML naast het VSA |
| `mxl`      | MXL niet op site → 404 in Coria (runtime)          |
| `onbekend` | Onbekende mode                                     |

---

## Inputs

| Input                       | Vereist?     | Opmerking                                                    |
| --------------------------- | ------------ | ------------------------------------------------------------ |
| `.vsa`                      | Ja           | Wordt in de coria-pass niet opnieuw semantisch gevalideerd   |
| `{stem}.coria.html`         | Conditioneel | Voor `mode=html` of `auto` met sibling                       |
| `.mxl` op gepubliceerde URL | Conditioneel | Voor `mode=mxl` of `auto` zonder sibling                     |

MXL wordt **niet** tijdens coria-export gegenereerd; conversie
([conversie-vsa-musicxml](conversie-vsa-musicxml.md)) moet eerder gedraaid hebben.

**Catalogus-pad `bron:`:** na resolve wijst de include naar een `.vsa` in
org-bron (vaak buiten de parochie-content-root). Coria-export faalt dan bij
build; **svg** op hetzelfde catalogus-pad werkt wel. Zie
[catalogus-samenstelling-zangstuk](../specs/catalogus-samenstelling-zangstuk.md).

---

## Validatie (bedoeling)

| Check                     | Blokkeert build? | Toelichting                |
| ------------------------- | ---------------- | -------------------------- |
| `.vsa` bestaat            | Ja               | Pad moet kloppen           |
| `.vsa` onder content-root | Ja (parochie)    | Beperking bij `bron:`-pad  |
| `mode=html` + sibling     | Ja               | Sibling verplicht          |
| VSA semantisch geldig     | Nee (huidig)     | Niet opnieuw in coria-pass |
| MXL bereikbaar            | Nee bij build    | Wel 404 voor de gebruiker  |

---

## Wat de eindgebruiker ziet

| Modus | Resultaat                                      |
| ----- | ---------------------------------------------- |
| HTML  | Opent statische Coria-export (partij vast)     |
| MXL   | Opent Coria met deep-link naar `.mxl`          |

Verberg op afdruk: CSS class `.coria-play` of plaats de directive in `:::web-only`.

---

## Geschikt / niet geschikt

| Geschikt                    | Niet geschikt                |
| --------------------------- | ---------------------------- |
| Online uitgave, oefenen     | Afdrukboek zonder interactie |
| Gemeente met Coria-licentie | Offline-only distributie     |

---

## Veelvoorkomende problemen (betekenis)

| Situatie                  | Typische oorzaak                    | Richting oplossing                                                                                         |
| ------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| VSA-bestand niet gevonden | Pad-typo                            | Pad t.o.v. `.md` corrigeren                                                                                |
| Geen Coria-HTML naast …   | `mode=html` zonder sibling          | Sibling toevoegen of `mode=auto` / `mxl`                                                                   |
| Onbekende mode            | Typo                                | `auto`, `html`, of `mxl`                                                                                   |
| Coria 404 op MXL          | MXL niet gepubliceerd               | [`vsa musicxml`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/musicxml/) + static deploy |

---

## Open punten (TBD)

- Automatisch MXL kopiëren naar static in alle builds
- Optionele VSA re-validatie vóór Coria-export
- Documentatie Coria-licentie / parochie-instellingen

---

## Gerelateerd

- [Conversie vsa musicxml](conversie-vsa-musicxml.md)
- [Exporttype mxl](exporttype-mxl.md)
- [Guide: MusicXML / Coria](https://orthodox-groningen.github.io/VSA-tooling/guides/musicxml-export/)
- [CLI: `vsa musicxml`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/musicxml/)
