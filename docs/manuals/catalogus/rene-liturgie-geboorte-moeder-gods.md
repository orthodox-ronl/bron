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

| | **Sjabloon** (parochie-repo) | **Sessie** (deze dienst) |
| --- | --- | --- |
| **`default.gelegenheid`** | ontbreekt | `geboorte-moeder-gods` |
| **`default.gelegenheidstype`** | `vast-feest` | overnemen |
| **`zoek=`** | `Troparion`, `Kondakion`, … | zelfde regels |
| **Tekst ertussen** | wel | wel (aanpassen mag) |

| Soort sjabloon | Voorbeeld | `default` in sjabloon |
| -------------- | --------- | ----------------------- |
| **Dienst** | Goddelijke liturgie | `gelegenheidstype`, `uitvoeringsvorm` |
| **Koormap** | Zondag per toon | `gelegenheidstype: zondag-cyclus`, `uitvoeringsvorm` |
| **Herkomst** | VOK-verzameling | `referentie`, `koormap_nummer` |

---

## Beoogde interface (GUI)

1. **Sjabloon kiezen** — *Goddelijke liturgie — parochie Groningen*.
2. **Sessie aanmaken** — Rene vult **`default.gelegenheid`**, `toon`, titel.
3. **`vsa resolve-catalogus`** — elke `zoek=` + `default.*` → catalogus-pad.
4. **Review** — alleen bij ambiguïteit.
5. **Tekst aanpassen** — markdown tussen includes blijft van Rene.
6. **Build** — `vsa validate` / `vsa build-markdown` op **opgelost** bestand.
7. **Opslaan** — `content-source/samenstellingen/geboorte-moeder-gods-2026.md`.

!!! todo "resolve-catalogus"
    `zoek=`, `catalogus zoek` en `vsa resolve-catalogus` zijn **gepland**.
    Onderstaand is het **doelbeeld**; Rene kan het markdown al schrijven.

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
  uitvoeringsvorm: Groningen
---
```

(Daarna dezelfde markdown als het sjabloon, eventueel met aangepaste tekst.)

Na **`vsa resolve-catalogus`**:

```markdown
:::include svg bron:troparion-geboorte-moeder-gods/obikhod/groningen alt="Troparion" scale="85%":::
:::include coria bron:troparion-geboorte-moeder-gods/obikhod/groningen label="Oefenen Troparion" mode="auto":::
```

---

## Wat Rene vandaag doet (tussenstap)

### 1. Index valideren

```cmd
cd /d C:\Git\orthodox-groningen\bron
python -m catalogus.cli index validate --bron-root . --content-root ..\VSA-tooling\examples\hugo-demo\content-source
```

### 2. Losse zoekregels testen (tot `catalogus zoek` bestaat)

```cmd
python -m catalogus.cli resolve zangstuk "troparion" --bron-root .
python -m catalogus.cli resolve uitvoeringsvorm --zangstuk troparion-geboorte-moeder-gods --variant obikhod Groningen --bron-root .
```

Bij unieke match: handmatig **`bron:…`** in de `:::include` zetten.

### 3. Resolve en publiceren (doel)

```cmd
cd /d C:\Git\orthodox-groningen\VSA-tooling
vsa resolve-catalogus examples\hugo-demo\content-source\samenstellingen\geboorte-moeder-gods-2026.md --content-root examples\hugo-demo\content-source --bron-root ..\bron
vsa validate examples\hugo-demo\content-source
```

---

## Wat Rene bereikt

- Vaste liturgische **tekst** blijft onder zijn controle.
- Zangstukken via **`zoek=`** + **`default.gelegenheid`**, niet via ids.
- Herbruikbaar sjabloon volgend jaar: alleen nieuwe sessie met andere `gelegenheid`.

## Verder lezen

- [Sjabloon schrijven](sjabloon-schrijven.md)
- [Zangstuk-opzoeken in sjablonen](../../specs/catalogus-samenstelling-zangstuk.md)
- [VSA — `:::include` met `zoek=`](https://github.com/orthodox-groningen/VSA-tooling/blob/main/docs/parochie-lokaal-vsa.md#include-met-zoek-catalogus)
- [Verhaal 2 — Cherubijnenhymne lokaal opnemen](rene-cherubijnenhymne-lokaal.md)
