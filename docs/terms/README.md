# Term-entry-sjabloon (curated texts)

Canonieke structuur voor bestanden in `docs/terms/` (en spiegel in tool-repo’s
onder `terminologie/` voor lokale termen). Normatieve betekenis blijft in
[terminologie.md](../specs/terminologie.md); de termpagina **motiveert** en
illustreert, zij **herdefinieert** niet.

Schrijfregels elders: [schrijfconventies](../specs/schrijfconventies.md).

`docs/terms/**` staat buiten de MkDocs-nav; lezers komen via glossary/TermRef.

---

## Verplichte onderdelen

### 1. Frontmatter (YAML)

| Veld                             | Rol                                                                 |
| -------------------------------- | ------------------------------------------------------------------- |
| `term`                           | Canoniek id (`[a-z0-9_-]+`)                                         |
| `formPhrases`                    | Vormen die in tekst herkend mogen worden (meervoud, alias, …)       |
| `glossaryTerm`                   | Weergavenaam in glossary / HRG                                      |
| `glossaryText`                   | **Eén zin** definitie (mag TermRefs `[ander](@)` bevatten)          |
| `glossaryNotes`                  | Optioneel: voorbeelden, afbakening (geen self-TermRef op deze term) |
| `glossaryAbbr` / `glossaryAlias` | Optioneel; HRG maakt aparte rijen                                   |

Morph-notatie in formPhrases (`afgeleide(n)`) mag; inject/HRG slaat `{}`-morph
over waar nodig.

### 2. Body

1. **Korte herhaling** van de definitie (mag TermRefs) — geen tweede, afwijkende
   definitie t.o.v. `glossaryText` / `terminologie.md`.
2. **Ja/Nee-tabel** (of gelijkwaardige afbakening): wat telt wel / niet.
3. **Motivatie (`## Motivatie`)** — beantwoordt *waartoe bestaat dit begrip?*
   (wat kun je ermee wat je zonder niet kunt?).
4. **Gerelateerd / verder lezen** — TermRefs naar verwante terms + link naar de
   canonieke paragraaf in `terminologie.md` (bijv. `Zie ook: … §N`).

### 3. Wat niet

- Body die SVG/afgeleiden tot “representatie” rekent terwijl de spec dat
  uitsluit (geen drift).
- Self-TermRef in `glossaryNotes` op de eigen term (blijft plain tekst).
- Spreektaal-monoloog zonder Ja/Nee of waartoe.

---

## Mini-voorbeeld (structuur)

```markdown
---
term: voorbeeldterm
formPhrases:
  - voorbeeldterm
  - voorbeeldtermen
glossaryTerm: Voorbeeldterm
glossaryText: "Eén zin met eventueel [andere-term](@)."
glossaryNotes:
  - "Voorbeeld of afbakening zonder self-TermRef."
---

# Voorbeeldterm

Korte zin parallel aan glossaryText.

| Status | Voorbeeld        |
| ------ | ---------------- |
| Ja     | …                |
| Nee    | …                |

## Motivatie

Waartoe dit begrip bestaat …

Zie ook: [verwante-term](@); [Terminologie, paragraaf N](../specs/terminologie.md#…).
```

Referentie-implementatie in deze map: [afgeleide.md](afgeleide.md).
