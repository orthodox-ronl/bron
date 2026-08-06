# Zangstuk toevoegen

Procedure voor beheerders (workflow 9.1): een nieuw [zangstuk](@) registreren in
de [bron-repository](@).

## Stappen

1. **Bepaal `id`** volgens [Repo-structuur](../specs/repo-structuur.md#naamgeving-zangstuk-id).
2. **Maak map** `zangstukken/<id>/` met `sources/vsa/`, `sources/scan/` indien nodig.
3. **Plaats [bronbestand](@)** in de juiste submap.
4. **Schrijf `zangstuk.yaml`:** minimaal `id`, `title`, één source met `file:`, `access:` of
   `status: nog-niet-getranscribeerd`.
5. **Liturgische metadata** invullen waar van toepassing.
6. **Valideer** `.vsa` met `vsa validate` ([VSA-tooling](@)).
7. **Commit en push** — documentatie-deploy draait via GitHub Actions.

## Meerdere zangstukken in één bronbestand

| Brontype    | Actie                                                                      |
| ----------- | -------------------------------------------------------------------------- |
| VSA / tekst | Splitsen: één `.vsa` per [zangstuk](@)                                     |
| Scan/PDF    | Niet splitsen; tweede zangstuk krijgt relatieve `file:` naar gedeelde scan |

Zie [Bronvariant toevoegen](bronvariant-toevoegen.md) voor [varianten](@) binnen
één zangstuk.

## Checklist metadata

- [ ] `id` = mapnaam
- [ ] Elke source heeft precies één statusveld
- [ ] `file:`-paden bestaan
- [ ] `copyright_status` klopt bij wel/niet aanwezig bestand

Schema: [Zangstuk-formaat](../specs/zangstuk-formaat.md).
