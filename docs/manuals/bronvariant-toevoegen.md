---
doc_type: task-guide
audience: "P2 — Bron-contentbeheerder"
---
# Bronvariant toevoegen

!!! note "Voor wie / wanneer"
    **Voor:** bron-contentbeheerder die onder een **bestaand** [zangstuk](@)
    een nieuwe [source-entry](@) / [representatie](@) (of [variant](@)-materiaal)
    toevoegt.

    **Wanneer:** het `zangstuk-id` bestaat al; je voegt scan, VSA of andere bron toe.
    **Niet** wanneer je een nieuw liturgisch stuk met nieuw id nodig hebt →
    [Zangstuk toevoegen](zangstuk-toevoegen.md).

**Antwoord in het kort:** plaats het [bronbestand](@) onder het bestaande
zangstuk, voeg een unieke source-entry toe (eventueel `based_on:`), valideer,
commit.

## Voorbeeld: tweede source-entry

Bestaande entry `scan-koormap`, nieuwe VSA-transcriptie:

```yaml
sources:
  - id: scan-koormap
    file: sources/scan/010-voorbeeld.pdf
    copyright_status: vrij
  - id: groningen
    file: sources/vsa/groningen.vsa
    based_on: scan-koormap
    copyright_status: vrij
    note: "Transcriptie van scan-koormap"
```

## Stappen

1. Controleer dat het om het **zelfde** [zangstuk](@) gaat (zelfde map /
   `zangstuk-id`), niet een nieuw zangstuk.
2. Plaats het [bronbestand](@) in `sources/<formaat>/` van dat zangstuk.
3. Voeg een [source-entry](@) toe aan `zangstuk.yaml` met unieke `id:`.
4. Zet `based_on:` naar de oorspronkelijke source indien van toepassing.
5. Valideer `.vsa` indien van toepassing:

   ```cmd
   cd /d C:\Git\orthodox-groningen\bron
   vsa validate zangstukken\<zangstuk-id>
   ```

6. Commit en push.

## Verwacht resultaat

- Nieuwe source-entry met unieke `id` in `zangstuk.yaml`.
- Bijbehorend bestand onder `sources/…` (of `access:` — zie
  [Copyright en access](copyright-access.md)).
- `vsa validate` groen als er nieuwe `.vsa` is.

## Scan → VSA (definitievere bron)

Voeg [VSA-notatie](@) toe als **nieuwe** source-entry; verwijder de scan-source
niet automatisch. Gebruik `based_on` en eventueel `note:` over de status van de
scan.

## Bron vervangen

Oudere sources blijven behouden tenzij expliciet opgeruimd — zie
[Inhoudslevenscyclus](../specs/inhoudslevenscyclus.md).

## Typische fouten

| Symptoom                              | Oorzaak                         | Fix                                                                                        |
| ------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------ |
| Dubbele `id:` in `sources:`           | Kopie zonder hernoemen          | Unieke `id` per entry                                                                      |
| Nieuwe map i.p.v. bestaande           | Verkeerde handleiding gekozen   | Onder bestaand `zangstuk-id` werken                                                        |
| `based_on` wijst naar onbekende id    | Typo of oude id                 | Id van bestaande source-entry gebruiken                                                    |
| Validate faalt na nieuwe `.vsa`       | Notatiefout                     | [`vsa validate`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/validate/) |

## Checklist

- [ ] Zelfde `zangstuk-id` / map
- [ ] Nieuwe `sources[].id` is uniek
- [ ] `file:` bestaat of `access:`/`status:` is correct
- [ ] `based_on` (indien gezet) verwijst naar bestaande entry
- [ ] Validate OK (bij `.vsa`)

## Zie ook

- [Zangstuk toevoegen](zangstuk-toevoegen.md)
- [Zangstuk-formaat](../specs/zangstuk-formaat.md)
- [Inhoudslevenscyclus](../specs/inhoudslevenscyclus.md)
