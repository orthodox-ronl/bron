---
doc_type: task-guide
audience: "P2 — Bron-contentbeheerder"
---
# Copyright en access

!!! note "Voor wie / wanneer"
    **Voor:** bron-contentbeheerder die copyright-gevoelig materiaal wil
    registreren **zonder** het bestand in git te zetten.

    **Wanneer:** `copyright_status` is `copyrighted` of `onbekend` en het
    [bronbestand](@) mag niet in de [bron-repository](@).
    **Niet** wanneer het materiaal wel vrij in de repo mag (`file:` + passende
    `copyright_status`).

**Antwoord in het kort:** zet `access:` (met `note` en contact) i.p.v. `file:`,
en laat het beschermde bestand buiten de repository.

## Voorbeeld in `zangstuk.yaml`

```yaml
sources:
  - id: koormap-scan
    copyright_status: copyrighted
    access:
      note: "Scan uit koormap; alleen met toestemming van de uitgever."
      contact: "koor@voorbeeld-parochie.nl"
      # url: "https://voorbeeld.nl/aanvraag"   # optioneel i.p.v. of naast contact
```

## Stappen

1. Zet `copyright_status: copyrighted` (of `onbekend`) op de [source-entry](@).
2. Vervang `file:` door `access:` met `note:` en `contact:` en/of `url:`.
3. Neem het bronbestand **niet** op in de repository (of verwijder het indien
   al aanwezig) en controleer dat git het niet meer tracked.

## Verwacht resultaat

- `zangstuk.yaml` beschrijft de source via `access:`; er is geen `file:`-pad
  naar het beschermde document.
- `git status` toont het bestand niet als toe te voegen inhoud.
- Publieke metadata (titel, liturgische context, [herkomst](@)) blijft wel in
  de repo.

## Wat blijft wel in de repo

- Het [zangstuk](@) en `zangstuk.yaml` met metadata
- Publieke titel, liturgische context, herkomst — **zonder** het beschermde bestand

## `rights` in VSA-frontmatter

Vrije weergave-tekst voor export (MusicXML e.d.). Vervangt **niet**
`copyright_status` / `access:` in `zangstuk.yaml`.

## Typische fouten

| Symptoom                                         | Oorzaak                                        | Fix                                        |
| ------------------------------------------------ | ---------------------------------------------- | ------------------------------------------ |
| Bestand staat nog in `sources/` en in de commit  | Alleen yaml aangepast, bestand niet verwijderd | Bestand uit repo halen; commit controleren |
| Zowel `file:` als `access:` op één entry         | Twee statusvelden                              | Alleen `access:` houden                    |
| Lege `access:` zonder `note`/`contact`/`url`     | Onvolledige metadata                           | Minstens `note` + bereikbaar contact/url   |

## Checklist

- [ ] `copyright_status` is gezet
- [ ] Geen `file:` meer op deze source-entry
- [ ] `access.note` legt uit waarom het bestand ontbreekt
- [ ] `contact` en/of `url` aanwezig
- [ ] Beschermd bestand niet (meer) in git

## Zie ook

- [Zangstuk toevoegen](zangstuk-toevoegen.md)
- [Zangstuk-formaat](../specs/zangstuk-formaat.md) (`access:`)
- [Source-entry](../terms/source-entry.md)
