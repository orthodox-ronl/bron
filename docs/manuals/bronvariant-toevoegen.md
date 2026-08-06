# Bronvariant toevoegen

Procedure voor een nieuwe source binnen een **bestaand** [zangstuk](@)
(workflow 9.2).

## Stappen

1. Controleer dat het om een [variant](@) van hetzelfde zangstuk gaat, niet een nieuw zangstuk.
2. Plaats het [bronbestand](@) in `sources/<formaat>/` van het bestaande zangstuk.
3. Voeg een [source-entry](@) toe aan `zangstuk.yaml` met unieke `id:`.
4. Zet `based_on:` naar de oorspronkelijke source indien van toepassing.
5. Valideer `.vsa` indien van toepassing; commit en push.

## Scan → VSA (definitievere bron)

Voeg [VSA-notatie](@) toe als **nieuwe** source-entry; verwijder de scan-source niet automatisch.
Gebruik `based_on` en eventueel `note:` over status van de scan.

## Bron vervangen

Oudere sources blijven behouden tenzij expliciet opgeruimd — zie
[Inhoudslevenscyclus](../specs/inhoudslevenscyclus.md).
