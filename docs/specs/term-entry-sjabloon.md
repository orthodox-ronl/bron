# Term-entry-sjabloon (curated texts)

Canonieke structuur voor bestanden in `docs/terms/` (en spiegel in tool-repo’s
onder `terminologie/` voor lokale termen). Normatieve betekenis blijft in
[terminologie.md](terminologie.md); de termpagina **motiveert** en illustreert,
zij **herdefinieert** niet.

Schrijfregels elders: [schrijfconventies](schrijfconventies.md).

`docs/terms/**` staat buiten de MkDocs-nav; lezers komen via glossary/TermRef.
Dit sjabloon staat bewust **niet** onder `docs/terms/` (mrgt zou het anders als
curated term inlezen).

---

## Verplichte onderdelen

### 1. Frontmatter (YAML)

| Veld                             | Rol                                                                          |
| -------------------------------- | ---------------------------------------------------------------------------- |
| `term`                           | Canoniek id (`[a-z0-9_-]+`)                                                  |
| `formPhrases`                    | Vormen die in tekst herkend mogen worden (meervoud, alias, …)                |
| `glossaryTerm`                   | Weergavenaam in glossary / HRG                                               |
| `glossaryText`                   | **Eén zin** definitie (mag TermRefs bevatten)                                |
| `glossaryNotes`                  | Optioneel: voorbeelden, afbakening (geen self-TermRef op deze term)          |
| `glossaryAbbr` / `glossaryAlias` | Optioneel; HRG maakt aparte rijen                                            |

Morph-notatie in formPhrases (`afgeleide(n)`) mag; inject/HRG slaat `{}`-morph
over waar nodig.

### 2. Body

1. **Korte herhaling** van de definitie (mag TermRefs) — geen tweede, afwijkende
   definitie t.o.v. `glossaryText` / `terminologie.md`.
2. **Ja/Nee-tabel** (of gelijkwaardige afbakening): wat telt wel / niet.
3. **Motivatie (`## Motivatie`)** — beantwoordt *waartoe bestaat dit begrip?*
   (wat kun je ermee wat je zonder niet kunt?).
4. **Gerelateerd / verder lezen** — verplicht: TermRefs naar verwante terms **vanuit
   het gezichtspunt van deze term** (wat hangt eraan vast? wat is het niet?), plus
   link naar de canonieke paragraaf in [terminologie.md](terminologie.md) /
   Zangstukmodel (bijv. `Zie ook: … §N`). De termpagina vertelt de samenhang lokaal;
   het Zangstukmodel geeft het overzicht over alle niveaus.

### 3. Wat niet

- Body die SVG/afgeleiden tot “representatie” rekent terwijl de spec dat
  uitsluit (geen drift).
- Self-TermRef in `glossaryNotes` op de eigen term (blijft plain tekst).
- Spreektaal-monoloog zonder Ja/Nee of waartoe.

---

## Mini-voorbeeld (structuur)

Gebruik bestaande terms als voorbeeld van volledige TermRefs; hier alleen de
skeletvorm (geen nep-TermRefs, zodat TEv2 niet faalt):

```markdown
---
term: voorbeeldterm
formPhrases:
  - voorbeeldterm
  - voorbeeldtermen
glossaryTerm: Voorbeeldterm
glossaryText: "Eén zin definitie; TermRefs naar bestaande terms indien nodig."
glossaryNotes:
  - "Voorbeeld of afbakening zonder self-TermRef."
---

# Voorbeeldterm

Korte zin parallel aan glossaryText.

| Status | Voorbeeld |
| ------ | --------- |
| Ja     | …         |
| Nee    | …         |

## Motivatie

Waartoe dit begrip bestaat …

Zie ook: verwante terms; Terminologie, paragraaf N.
```

Referentie-implementatie: [afgeleide.md](../terms/afgeleide.md),
[representatie.md](../terms/representatie.md).
