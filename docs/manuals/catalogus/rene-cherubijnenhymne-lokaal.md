---
doc_type: user-story
audience: "P1 — Parochie-docs-maintainer"
---
# Verhaal 2 — Rene neemt Nana's Cherubijnenhymne op in de parochie-repo

*Nana stuurt Rene een **PDF** met een Cherubijnenhymne die zij heeft gezet in de
traditie van **Kastorski**, bewerkt voor hoe de parochie Groningen zingt. Rene
wil het stuk in de **lokale** parochie-catalogus zodat het in liturgiemappen
([samenstellingen](@)) kan worden opgenomen, nog vóór het org-breed in de
**[bron-repository](@)** staat.*

---

## Situatie

| Aspect                | Waarde                                              |
| --------------------- | --------------------------------------------------- |
| [Zangstuk](@)         | Cherubijnenhymne (`cherubijnenhymne`)               |
| [Variant](@)          | Kastorski (`kastorski`) — melodie-lijn              |
| [Uitvoeringsvorm](@)  | Parochie Groningen (`groningen`)                    |
| [Bronbestand](@) (nu) | PDF-scan van Nana's partituur                       |
| Status                | [Parochie-lokaal](@) — nog niet in org-brede bron   |

Terminologie en mappenstructuur:
[parochie-lokaal zangstukken](../parochie-lokaal-zangstukken.md).

---

## Beoogde interface (GUI)

Rene kiest in de catalogus *Materiaal toevoegen → [Parochie-lokaal](@)*.

1. **Wizard stap 1 — [Zangstuk](@):** zoekt “cherubijnenhymne”. Bestaat al in bron?
   Ja → koppelen aan bestaand `zangstuk-id`. Nee → nieuw id voorstellen (hier:
   bestaand).
2. **Stap 2 — [Variant](@):** “Kastorski” / `Касторский` → `kastorski`.
3. **Stap 3 — [Uitvoeringsvorm](@):** naam “Groningen”, [alias](@) registreren.
4. **Stap 4 — [Representatie](@):** PDF slepen naar `repr/`; optioneel later VSA
   toevoegen als Nana transcribeert.
5. **Stap 5 — [Manifesten](@):** tool genereert `variant.yaml` en
   `uitvoeringsvorm.yaml` met `aliases:` en `representaties:`.
6. **Validatie:** groene vinkjes; knop *Open in Verkenner* voor git commit.

!!! note "GUI + lokaal-wizard"
    De wizard is **gepland**. Rene maakt de mappen en yaml vandaag handmatig (of
    met templates); [`catalogus index validate`](../../reference/catalogus-cli.md#catalogus-index-validate) en [`catalogus zoek`](../../reference/catalogus-cli.md#catalogus-zoek) werken op CLI.

---

## Wat Rene vandaag doet (CLI + bestanden)

### 1. Mappenstructuur aanmaken

In de parochie content-source:

```text
content-source/
└── lokaal/
    └── cherubijnenhymne/
        └── kastorski/
            ├── variant.yaml
            └── groningen/
                ├── uitvoeringsvorm.yaml
                └── repr/
                    ├── nana-partituur.pdf      ← PDF van Nana
                    └── groningen.vsa           ← later, indien getranscribeerd
```

Referentie-fixture in bron-tests:
`tests/fixtures/alias-index/lokaal/cherubijnenhymne/`.

### 2. Manifesten schrijven

**`variant.yaml`:**

```yaml
zangstuk-id: cherubijnenhymne
variant-id: kastorski
title: "Cherubijnenhymne (Kastorski)"

aliases:
  - { text: "Kastorski", lang: en }
  - { text: "Касторский", lang: ru }
```

**`uitvoeringsvorm.yaml`:**

```yaml
uitvoeringsvorm-id: groningen
based_on: kastorski
herkomst:
  author: "Nana (parochie Groningen)"
  note: "Bewerking op basis van Kastorski-traditie"

aliases:
  - { text: "Groningen", lang: nl }

representaties:
  - representatie-id: scan-nana
    file: repr/nana-partituur.pdf
  # Later, wanneer VSA klaar is:
  # - representatie-id: groningen-vsa
  #   file: repr/groningen.vsa
```

### 3. PDF plaatsen

Rene kopieert Nana's bestand naar `repr/nana-partituur.pdf` en commit in de
parochie-repo.

### 4. Index valideren

Controleer dat er geen conflicterende [aliassen](@) zijn
([Catalogus CLI](../../reference/catalogus-cli.md)).

### 5. Resolve testen

Los de [alias](@) “Groningen” voor de [uitvoeringsvorm](@) op binnen
`cherubijnenhymne` / `kastorski` — verwacht [canoniek id](@) `groningen`
([Catalogus CLI — resolve](../../reference/catalogus-cli.md)).

### 6. Gebruik in een sjabloon of [samenstelling](@)

In het liturgie-sjabloon (verhaal 1):

```markdown
:::include svg zoek="Cherubijnenhymne (Kastorski)" alt="Cherubijnenhymne":::
```

Met `default.uitvoeringsvorm: Groningen` in de **sessie** (homogene liturgie) of
disambiguation `Cherubijnenhymne (Kastorski)` in mixed session. Na oplossen van
`zoek=` (bijv. `:::include svg lokaal:cherubijnenhymne/kastorski/groningen:::`) —
zie
[`vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/).

Zoektest:
[Catalogus CLI — zoek](../../reference/catalogus-cli.md).

---

## Afspraken met Nana

- **Copyright:** Nana geeft mondeling toestemming voor parochiegebruik; Rene
  noteert `herkomst.author` in het [manifest](@). Bij twijfel: [copyright en access](../copyright-access.md).
- **Transcriptie:** de PDF is de eerste [representatie](@); VSA kan later als tweede
  [representatie](@) onder dezelfde [uitvoeringsvorm](@).

---

## Wat Rene bereikt

- Het stuk is **vindbaar** via [aliassen](@) (“Cherubijnenhymne Kastorski Groningen”).
- [Samenstellingen](@) verwijzen stabiel met `lokaal:…/…/…`.
- Klaar voor **[promotie](@) naar [bron-repository](@)** (verhaal 3) zonder ids te wijzigen.

## Verder lezen

- [Verhaal 3 — Breder beschikbaar maken](rene-cherubijnenhymne-naar-bron.md)
- [Catalogus CLI — resolve](../../reference/catalogus-cli.md)
