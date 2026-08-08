# Parochie-lokaal zangstukken

Handleiding voor parochie-specifiek zangmateriaal in een Hugo/content-source-repo, naast materiaal uit [orthodox-groningen/bron](https://github.com/orthodox-groningen/bron).

Terminologie: [specs/terminologie.md](../specs/terminologie.md), [specs/zangstuk-identificatie.md](../specs/zangstuk-identificatie.md).

---

## Wanneer parochie-lokaal?

| Situatie                             | Aanpak                                                     |
| ------------------------------------ | ---------------------------------------------------------- |
| Zangstuk staat (deels) in bron       | Bron-sync + eventueel parochie-lokaal uitvoeringsvorm      |
| Parochie-bewerking, nog niet gedeeld | `content-source/lokaal/`                                   |
| Eenmalig concept, kort fragment      | Inline notatie-directive (tool-specifiek; zie VSA-tooling) |
| Export, diff t.o.v. bron, hergebruik | Losse bronbestand onder `lokaal/…/repr/`                   |

---

## Mappenstructuur

```text
content-source/
└── lokaal/
    └── <zangstuk-id>/
        └── <variant-id>/
            ├── variant.yaml
            └── <uitvoeringsvorm-id>/
                ├── uitvoeringsvorm.yaml
                └── repr/
                    └── <representatie-id>.<ext>
```

**Canonieke ids:** `^[a-z0-9_-]+$` — zie [terminologie](../specs/terminologie.md).

**Referentie-implementatie (VSA-demo):** [VSA-demo — content-source/lokaal](https://github.com/orthodox-groningen/VSA-demo/tree/main/content-source/lokaal).

---

## Manifest

Zie [terminologie §16](../specs/terminologie.md#16-manifest).

### `variant.yaml`

```yaml
zangstuk-id: antifoon-1-weekdagen
variant-id: liturgikon-weekdagen
title: "1e antifoon weekdagen (Liturgikon-melodielijn)"

aliases:
  - { text: "1e antifoon weekdagen", lang: nl }
```

### `uitvoeringsvorm.yaml`

```yaml
uitvoeringsvorm-id: hemelum
based_on: liturgikon
herkomst:
  author: "Parochie Hemelum (Liturgikon-praktijk)"
  reference: "Liturgikon, pp. 174, 270"

aliases:
  - { text: "Hemelum", lang: nl }

representaties:
  - representatie-id: hemelum
    file: repr/hemelum.vsa
```

Yaml-velden zijn **informatief** voor beheerders; de build valideert vandaag vooral bronbestanden en markdown-includes (tool-specifiek).

---

## Inline vs los bestand

| Situatie                                     | Aanbevolen                                     |
| -------------------------------------------- | ---------------------------------------------- |
| Parochie-bewerking, diff, hergebruik, export | **Los bestand + include-directive**            |
| Eenmalig kort fragment, concept              | Inline notatie (tool-specifiek)                |
| Meerdere stukken op één pagina               | Eén bestand per stuk of per `<details>`-sectie |

---

## Verwijzen in samenstellingen

**Relatief pad** (legacy): vanuit het markdown-bestand (VSA-tooling).

**Id-gebaseerd (fase 3, basis):** `bron:<zangstuk-id>/<variant-id>/<uitvoeringsvorm-id>`,
`lokaal:…` — zie [catalogus-architectuur](../specs/catalogus-architectuur.md).

**Sjabloon (fase 4, geïmplementeerd):** markdown met `:::include zoek=` — zie
[catalogus-samenstelling-zangstuk.md](../specs/catalogus-samenstelling-zangstuk.md).
Resolve naar catalogus-pad via
[`vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/)
(VSA-tooling).

---

## Promotie naar bron-repository

1. Behoud **canonieke ids** (`variant-id`, `uitvoeringsvorm-id`, `representatie-id`).
2. Open PR naar `orthodox-groningen/bron` met bronbestand + metadata (zie [zangstuk toevoegen](zangstuk-toevoegen.md) / [bronvariant toevoegen](bronvariant-toevoegen.md)).
3. Na merge: samenstelling kan bron-referentie gebruiken i.p.v. `lokaal/`-pad.

Parochie-lokaal mag als kopie blijven staan; **canonical** is bron na sync.

---

## Build-pipeline (algemeen)

| Stap                                                                                                         | Parochie-lokaal                              |
| ------------------------------------------------------------------------------------------------------------ | -------------------------------------------- |
| Sync bron                                                                                                    | Niet nodig — bestanden in git                |
| [`vsa resolve-catalogus`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/resolve-catalogus/) | Als markdown **`zoek=`** bevat (VSA-tooling) |
| Validatie                                                                                                    | Tool valideert `content-source` recursief    |
| Site-build                                                                                                   | Includes op relatief pad / catalogus-pad     |
| Static site generator                                                                                        | Ongewijzigd t.o.v. bron-materiaal            |

**VSA-tooling:** concrete commando's — [docs/guides/parochie-lokaal-vsa.md](https://orthodox-groningen.github.io/VSA-tooling/guides/parochie-lokaal-vsa/).
