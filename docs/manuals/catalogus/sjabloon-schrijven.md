---
doc_type: task-guide
audience: "P1 — Parochie-docs-maintainer"
---
# Sjabloon schrijven (catalogus)

Praktische handleiding voor **Rene** en andere parochie-beheerders. Normatief contract:
[Zangstuk-opzoeken in sjablonen](../../specs/catalogus-samenstelling-zangstuk.md).

Voorbeeld workflow: [verhaal 1](rene-liturgie-geboorte-moeder-gods.md).

---

## Wat is een sjabloon?

Een **sjabloon** is een herbruikbaar markdown-bestand in de parochie **content-source**:

- vaste **tekst** (kopjes, liturgische aanwijzingen) — jij schrijft dat zelf;
- **`default.gelegenheidstype`** (en parochie-defaults) — **geen** individuele feesten;
- **`:::include`** met [exporttype](@) en **`zoek="…"`** — liturgische rol, nog geen pad.

Als jij het sjabloon **gebruikt** voor een concrete dienst, maak je een **sessie**:
zelfde structuur, plus **`default.gelegenheid`** (en evt. `toon`, titel, datum).

---

## Drie soorten sjablonen

| Soort        | Wanneer                                 | Typische `default` in **sjabloon**                   |
| ------------ | --------------------------------------- | ---------------------------------------------------- |
| **Dienst**   | Goddelijke liturgie (alle vast-feesten) | `gelegenheidstype: vast-feest`, `uitvoeringsvorm`    |
| **Koormap**  | Zondagse stukken per toon               | `gelegenheidstype: zondag-cyclus`, `uitvoeringsvorm` |
| **Herkomst** | Verzameling uit één bron (bijv. VOK)    | `referentie`, `koormap_nummer`                       |

**Legacy (niet meer aanbevolen):** yaml-inventarisatie
[goddelijke-liturgie.yaml](https://github.com/orthodox-groningen/VSA-demo/blob/main/content-source/praktijk/goddelijke-liturgie.yaml)
in de VSA-demo — ruwe VOKN-koormap-notities, **geen** geldig sjabloon- of
compositie-schema. Nieuw werk: markdown-sjablonen (hierboven) en
[catalogus-samenstelling-zangstuk](../../specs/catalogus-samenstelling-zangstuk.md).
Zie ook [samenvatting-project — sjabloon vs compositie](../../plans/samenvatting-project.md).

---

## Stap 1 — Frontmatter (sjabloon)

Minimaal **`default.gelegenheidstype`**. **`default.uitvoeringsvorm`** alleen als het
sjabloon bedoeld is voor **homogene** sessies (zelfde parochie-praktijk overal).

Geen **`default.gelegenheid`** in het sjabloon — die zet Rene in de **sessie**.

```yaml
---
sjabloon: goddelijke-liturgie-groningen
default:
  gelegenheidstype: vast-feest
  uitvoeringsvorm: Groningen
---
```

**Sessie** (Rene, Geboorte Moeder Gods — **mixed session**):

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

Feest-stukken komen uit **bron** (`liturgikon`); Cherubijnenhymne uit **lokaal**
(`groningen`). Daarom **geen** `default.uitvoeringsvorm` in deze sessie — één
parochie-default dekt beide niet. Zie [mixed session](../../specs/catalogus-samenstelling-zangstuk.md#mixed-session).

Eigen yaml-sleutels naast `sjabloon` / `titel` / `default` / `bronnen` mag — de
catalogus negeert ze.

---

## Stap 2 — Tekst en includes

Schrijf gewone markdown. Waar notatie komt — meteen het [exporttype](@) dat je op de site wilt:

```markdown
## Kleine intocht

### Troparion

:::include svg zoek="Troparion" alt="Troparion" scale="85%":::
:::include coria zoek="Troparion" label="Oefenen Troparion" mode="auto":::

Tekst of aanwijzing voor het koor (vrij).

### Kondakion

:::include svg zoek="Kondakion" alt="Kondakion":::
```

**Regels voor `zoek=`**

- Alleen de **liturgische rol** (`Troparion`, `Kondakion`, `Prokimen`) — geen feestnaam;
  die zit in **`default.gelegenheid`** van de sessie.
- Meerdere `:::include`-regels met **dezelfde** `zoek=` voor svg, coria, mp3-player, …
- `(Kastorski)` in `zoek=` mag voor disambiguation — bijv. Cherubijnenhymne.
- Geen `variant-id` tenzij je na review een vast **`bron:…`**-pad zet
  ([variant](@) alleen dan expliciet).

---

## Stap 3 — Koormap-sjabloon (voorbeeld)

```yaml
---
sjabloon: groningen-koormap-zondag
default:
  gelegenheidstype: zondag-cyclus
  uitvoeringsvorm: Groningen
---
```

Rene zet in de sessie **`default.toon`**. In `zoek=` geen toon herhalen:

```markdown
# Zondag — toon {{toon}}

:::include svg zoek="Troparion" alt="Troparion zondag":::
:::include svg zoek="Kondakion" alt="Kondakion zondag":::
:::include svg zoek="Prokimen" alt="Prokimen zondag":::
```

---

## Stap 4 — Resolve en publiceren

1. Controleer dat de catalogus-index in orde is
   ([Catalogus CLI](../../reference/catalogus-cli.md)).
2. Los elke `zoek=` op tot `bron:…` / `lokaal:…`
   ([`vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/)).
   Bij meerdere treffers: lijst bekijken of `default.*` / `zoek=` verfijnen
   ([`catalogus zoek`](../../reference/catalogus-cli.md#catalogus-zoek)).
3. Valideer en bouw het **opgeloste** bestand
   ([`vsa validate`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/validate/),
   [`vsa build-markdown`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/build-markdown/)).

**Let op (demo):** mappen `samenstellingen/` en `sjablonen/` worden in de
Hugo-demo niet automatisch gepubliceerd. Kopieer opgeloste inhoud naar een
publishbare content-map, of pas de build-config aan — zie
[parochie-lokaal VSA](https://orthodox-groningen.github.io/VSA-tooling/guides/parochie-lokaal-vsa/).

**Export:** **`:::include svg`** op `bron:` werkt; **`:::include coria`** op
`bron:` faalt zolang het `.vsa` buiten de content-root staat (org-bron). Coria
op `lokaal:` werkt wel.

---

## Verder lezen

- [Catalogus — gebruikersverhalen](index.md)
- [Parochie-lokaal zangstukken](../parochie-lokaal-zangstukken.md)
- [Exportcontracten](../../reference/exportcontracten.md)
