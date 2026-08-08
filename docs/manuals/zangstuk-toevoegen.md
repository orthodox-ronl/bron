---
doc_type: task-guide
audience: "P2 — Bron-contentbeheerder"
---
# Zangstuk toevoegen

!!! note "Voor wie / wanneer"
    **Voor:** bron-contentbeheerder die een **nieuw** [zangstuk](@) met
    nieuw `zangstuk-id` in de [bron-repository](@) zet.

    **Wanneer:** je hebt een nieuw liturgisch stuk (nieuwe map + `zangstuk.yaml`).
    **Niet** wanneer je alleen een [variant](@) of extra [bronbestand](@) onder
    een *bestaand* zangstuk toevoegt → [Bronvariant toevoegen](bronvariant-toevoegen.md).

**Antwoord in het kort:** maak `zangstukken/<id>/` met bronnen en een minimale
`zangstuk.yaml`, valideer eventuele `.vsa`, commit en push.

## Verwachte mapboom

```text
zangstukken/<zangstuk-id>/
  zangstuk.yaml
  sources/
    vsa/          # optioneel: .vsa-bestanden
    scan/         # optioneel: scans/PDF
```

## Voorbeeld `zangstuk.yaml` (minimaal)

```yaml
id: troparion-voorbeeld-toon-1
title: "Troparion voorbeeld, toon 1"

gelegenheidstype: zondag-cyclus
toon: 1

sources:
  - id: groningen
    file: sources/vsa/groningen.vsa
    copyright_status: vrij
```

`id` moet gelijk zijn aan de mapnaam. Schema en meer velden:
[Zangstuk-formaat](../specs/zangstuk-formaat.md).

## Stappen

1. **Bepaal `id`** volgens
   [Repo-structuur — naamgeving](../specs/repo-structuur.md#naamgeving-zangstuk-id)
   (alleen `[a-z0-9_-]+`).
2. **Maak de mapboom** hierboven (`sources/vsa/` en/of `sources/scan/` naar behoefte).
3. **Plaats het [bronbestand](@)** in de juiste submap (of gebruik `access:` /
   `status:` — zie [Copyright en access](copyright-access.md)).
4. **Schrijf `zangstuk.yaml`:** minimaal `id`, `title`, één [source-entry](@)
   met precies één van `file:`, `access:` of `status: nog-niet-getranscribeerd`.
5. **Liturgische metadata** invullen waar van toepassing (`gelegenheid`, `toon`, …).
6. **Valideer** `.vsa` (indien aanwezig):

   ```cmd
   cd /d C:\Git\orthodox-groningen\VSA-tooling
   scripts\bootstrap.cmd
   cd /d C:\Git\orthodox-groningen\bron
   vsa validate zangstukken\<zangstuk-id>
   ```

7. **Commit en push** — docs-deploy via GitHub Actions.

## Verwacht resultaat

- Map `zangstukken/<id>/` bestaat met geldige `zangstuk.yaml`.
- `vsa validate` op die map (of `zangstukken`) eindigt met `OK` als er `.vsa` is.
- Op `main`/PR verschijnt het zangstuk in de repo; het staat **niet** als
  aparte webpagina op de docs-site.

## Meerdere zangstukken in één bronbestand

| Brontype    | Actie                                                                      |
| ----------- | -------------------------------------------------------------------------- |
| VSA / tekst | Splitsen: één `.vsa` per [zangstuk](@)                                     |
| Scan/PDF    | Niet splitsen; tweede zangstuk krijgt relatieve `file:` naar gedeelde scan |

## Typische fouten

| Symptoom / melding                         | Oorzaak                                        | Fix                                                                                                                |
| ------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Mapnaam ≠ `id:` in yaml                    | Typo of hernoemen vergeten                     | Gelijk trekken; zie checklist                                                                                      |
| Twee van `file:` / `access:` / `status:`   | Meer dan één statusveld op één source-entry    | Precies één houden                                                                                                 |
| `file:`-pad bestaat niet                   | Verkeerde relatieve pad t.o.v. `zangstuk.yaml` | Pad controleren onder `sources/…`                                                                                  |
| `vsa validate` faalt (syntax/semantiek)    | Ongeldige [VSA-notatie](@)                     | Melding lezen; man-page [`vsa validate`](https://orthodox-groningen.github.io/VSA-tooling/reference/cli/validate/) |

## Checklist metadata

- [ ] `id` = mapnaam
- [ ] Elke source heeft precies één statusveld (`file:` / `access:` / `status:`)
- [ ] `file:`-paden bestaan (relatief t.o.v. `zangstuk.yaml`)
- [ ] `copyright_status` klopt bij wel/niet aanwezig bestand

## Zie ook

- [Bronvariant toevoegen](bronvariant-toevoegen.md)
- [Copyright en access](copyright-access.md)
- [Zangstuk-formaat](../specs/zangstuk-formaat.md)
- [Inhoudslevenscyclus](../specs/inhoudslevenscyclus.md)
