---
term: vsa-bestand
termType: concept
glossaryTerm: "vsa-bestand"
glossaryText: "Een bestand met de extensie `.vsa` waarvan de inhoud uitsluitend syntactisch geldige [vsa-notatie](@) bevat — d.w.z. door de [vsa-tooling](@) foutloos wordt geparseerd en gevalideerd."
glossaryNotes:
  - "Een vsa-bestand is een [bronbestand](@) dat tegelijk als [representatie](@) van een [uitvoeringsvorm](@) fungeert."
  - "Bestanden in [bron-repository](@) staan onder `sources/vsa/` in de [zangstuk](@)-map; de bestandsnaam weerspiegelt de herkomst, bijv. `groningen.vsa`."
  - "Afgeleide formaten (`.svg`, `.mxl`) worden door [vsa-tooling](@) uit een vsa-bestand gegenereerd en worden niet in de [bron-repository](@) opgeslagen."
formPhrases:
  - vsa-bestanden
  - vsa-bestand
---

# vsa-bestand

Een **vsa-bestand** is een bestand met de extensie `.vsa` waarvan de inhoud uitsluitend syntactisch geldige [vsa-notatie](@) bevat. Dat betekent concreet: het bestand wordt door de [vsa-tooling](@) foutloos geparseerd en gevalideerd (`vsa validate`).

Een vsa-bestand is een [bronbestand](@): het staat in git, is door mensen geschreven (of herleiding van een scan), en vormt de primaire bron voor alle afgeleide publicatievormen. Tegelijk is het een [representatie](@) van een [uitvoeringsvorm](@): het legt de melodie en tekst van één concrete uitvoeringswijze eenduidig vast.

## Structuur

Een vsa-bestand heeft één van de volgende vormen:

**Platte VSA-notatie** — geen koptekst, direct notatietekst:

```text
Gij komt op {/voor} {/al_}{\len} die U ver{\&\e_&_}{/ren}.
```

**VSA met optionele YAML-frontmatter** — voor metadata bij stand-alone gebruik:

```yaml
---
muziek:
  do: F4
  mode: major
identificatie:
  title: Troparion, toon 1
---
Gij komt op {/voor} {/al_}{\len} die U ver{\&\e_&_}{/ren}.
```

(het bovengenoemde voorbeeld is alleen ter illustratie, en kan afwijken van de specificaties)


De frontmatter is bedoeld voor gebruik buiten de [bron-repository](@) (bijv. losse export via [vsa-tooling](@)). Binnen de [bron-repository](@) is `zangstuk.yaml` leidend voor overlappende metadata.

## Validatie

Elk vsa-bestand in de [bron-repository](@) wordt gevalideerd met:

```cmd
vsa validate zangstukken
```

CI voert deze validatie bij elke push en PR uit.

## Motivatie

Het begrip *vsa-bestand* maakt duidelijk dat niet elk bestand met de extensie `.vsa` per definitie geldig is: de inhoud moet door de [vsa-tooling](@) verwerkt kunnen worden. Door dit als apart concept te benoemen, kan de documentatie precies onderscheiden tussen:

- een *pad naar een `.vsa`*: louter een bestandsreferentie;
- een *vsa-bestand*: een bestand dat ook inhoudelijk geldig is en als [bronbestand](@) en [representatie](@) fungeert.

## Zie ook:

- [VSA-demo](https://orthodox-groningen.github.io/VSA-demo/)
- [GitHub orthodox-groningen/VSA-tooling](https://github.com/orthodox-groningen/VSA-tooling)
