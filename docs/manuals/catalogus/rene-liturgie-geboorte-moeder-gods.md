---
doc_type: user-story
audience: "P1 — Parochie-docs-maintainer"
---
# Verhaal 1 — Rene stelt een liturgiemap samen voor het feest van de Geboorte van de Moeder Gods

*Rene bereidt de zang voor de liturgie op **8 september** (Geboorte van de
Moeder Gods) voor. Hij start vanuit een **sjabloon** voor de goddelijke liturgie,
zet **`default.gelegenheid`** in een **sessie**, en laat de catalogus de
**`zoek=`**-parameters in zijn **`:::include`**-regels oplossen tot een
**samenstelling** voor de parochie-site.*

Normatief contract: [zangstuk-opzoeken in sjablonen](../../specs/catalogus-samenstelling-zangstuk.md).

---

## Situatie

Rene kent de liturgische volgorde (vredeslitanie, antifoon, kleine intocht,
troparion, kondakion, …) en schrijft zelf tekst tussen de stukken. Het
**sjabloon** bevat al `:::include svg`, `:::include coria`, en later evt.
`:::include mp3-player` — allemaal met **`zoek="Troparion"`**, niet
`zoek="Troparion geboorte Moeder Gods"`. Het feest zet hij eenmalig in
**`default.gelegenheid`** van de sessie.

Variant- en uitvoeringsvorm-ids ziet hij **alleen** als de catalogus meerdere
kandidaten teruggeeft (review).

---

## Sjabloon vs sessie

|                                | **Sjabloon** (parochie-repo) | **Sessie** (deze dienst)       |
| ------------------------------ | ---------------------------- | ------------------------------ |
| **`default.gelegenheid`**      | ontbreekt                    | `geboorte-moeder-gods`         |
| **`default.gelegenheidstype`** | `vast-feest`                 | overnemen                      |
| **`default.uitvoeringsvorm`**  | optioneel (homogene sessies) | **weglaten** bij mixed session |
| **`zoek=`**                    | `Troparion`, `Kondakion`, …  | zelfde regels                  |
| **Tekst ertussen**             | wel                          | wel (aanpassen mag)            |

| Soort sjabloon | Voorbeeld           | `default` in sjabloon                                |
| -------------- | ------------------- | ---------------------------------------------------- |
| **Dienst**     | Goddelijke liturgie | `gelegenheidstype`, `uitvoeringsvorm`                |
| **Koormap**    | Zondag per toon     | `gelegenheidstype: zondag-cyclus`, `uitvoeringsvorm` |
| **Herkomst**   | VOK-verzameling     | `referentie`, `koormap_nummer`                       |

---

## Beoogde interface (GUI)

1. **Sjabloon kiezen** — *Goddelijke liturgie — parochie Groningen*.
2. **Sessie aanmaken** — Rene vult **`default.gelegenheid`**, `toon`, titel.
3. **Zoekopdrachten oplossen** — elke `zoek=` + `default.*` → catalogus-pad.
4. **Review** — alleen bij ambiguïteit.
5. **Tekst aanpassen** — markdown tussen includes blijft van Rene.
6. **Build** — opgelost bestand valideren en publiceren.
7. **Opslaan** — bijv. onder `samenstellingen/` in de parochie-content.

!!! note "GUI"
    Stappen 1–2 en 4 zijn in een **grafische catalogus** nog **gepland**. Stappen 3
    en 5–6 werken vandaag via CLI (links hieronder).

---

## Sjabloon (doelbeeld — zonder gelegenheid)

```yaml
---
sjabloon: goddelijke-liturgie-groningen
default:
  gelegenheidstype: vast-feest
  uitvoeringsvorm: Groningen
---
```

```markdown
## Kleine intocht

### Troparion

:::include svg zoek="Troparion" alt="Troparion" scale="85%":::
:::include coria zoek="Troparion" label="Oefenen Troparion" mode="auto":::

Tekst voor het koor (Rene).

### Kondakion

:::include svg zoek="Kondakion" alt="Kondakion":::

## Cherubijnenhymne

:::include svg zoek="Cherubijnenhymne (Kastorski)" alt="Cherubijnenhymne":::

## Prokimen

:::include svg zoek="Prokimen" alt="Prokimen":::
```

---

## Sessie (Rene — 8 september)

```yaml
---
sjabloon: goddelijke-liturgie-groningen
titel: "Goddelijke liturgie — Geboorte Moeder Gods (8 september)"
default:
  gelegenheid: geboorte-moeder-gods
  gelegenheidstype: vast-feest
  toon: 4
---
```

(Daarna dezelfde markdown als het sjabloon, eventueel met aangepaste tekst.)

**Mixed session:** geen `default.uitvoeringsvorm` — feest-stukken uit bron (`liturgikon`),
Cherubijnenhymne lokaal (`groningen`).

Na [`vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/):

```markdown
:::include svg bron:troparion-geboorte-moeder-gods/troparion-geboorte-moeder-gods/liturgikon alt="Troparion" scale="85%":::
:::include svg bron:kondak-geboorte-moeder-gods/kondak-geboorte-moeder-gods/liturgikon alt="Kondakion":::
:::include svg lokaal:cherubijnenhymne/kastorski/groningen alt="Cherubijnenhymne":::
```

**Coria** op `bron:`-paden faalt bij build zolang `.vsa` buiten content-root ligt;
**svg** werkt wel. Coria op `lokaal:` werkt.

---

## Wat Rene vandaag doet (stap voor stap)

Voorbeeld-sessie in de demo: `praktijk/samenstellingen/geboorte-moeder-gods-2026.md`
onder de VSA-demo content-source.

1. **Index controleren** — zodat bron én lokaal in de catalogus staan.
   Exacte aanroep: [Catalogus CLI](../../reference/catalogus-cli.md).
2. **Zoekregels proberen** — bijv. `Troparion` met
   `default.gelegenheid: geboorte-moeder-gods`, en
   `Cherubijnenhymne (Kastorski)`. Bij meerdere treffers: lijst bekijken of
   `zoek=` / `default.*` aanscherpen ([Catalogus CLI — zoek](../../reference/catalogus-cli.md)).
3. **Includes oplossen** — `zoek=` → `bron:…` / `lokaal:…`
   ([`vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/)).
4. **Valideren** van de content-source
   ([`vsa validate`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/validate/)).

Workflow-overzicht:
[parochie-lokaal VSA](https://orthodox-groningen.github.io/VSA-tooling/guides/parochie-lokaal-vsa/).

---

## Wat Rene bereikt

- Vaste liturgische **tekst** blijft onder zijn controle.
- Zangstukken via **`zoek=`** + **`default.gelegenheid`**, niet via ids.
- Herbruikbaar sjabloon volgend jaar: alleen nieuwe sessie met andere `gelegenheid`.

## Verder lezen

- [Sjabloon schrijven](sjabloon-schrijven.md)
- [Zangstuk-opzoeken in sjablonen](../../specs/catalogus-samenstelling-zangstuk.md)
- [VSA — `:::include` met `zoek=`](https://orthodox-groningen.github.io/VSA-tooling/guides/parochie-lokaal-vsa/#include-met-zoek-catalogus)
- [Verhaal 2 — Cherubijnenhymne lokaal opnemen](rene-cherubijnenhymne-lokaal.md)
