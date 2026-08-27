# bron

Centrale bronrepository van zangstukken voor orthodoxe kerkmuziek (Slavische
traditie, Vereenvoudigde Slavische Accentnotatie / VSA), beheerd binnen de
GitHub-organisatie [orthodox-ronl](https://github.com/orthodox-ronl).

Deze repository is de **single source of truth** voor de muzikale inhoud die
door verschillende parochies wordt gebruikt. Parochies bouwen hun eigen site
(bijv. met Hugo) en putten daarbij uit het materiaal in deze repository.

## Documentatie (GitHub Pages)

**https://orthodox-ronl.github.io/bron/**

Specificaties, handleidingen, referentie en ontwikkelplannen — gebouwd met MkDocs
Material. Preview van branches: **https://orthodox-ronl.github.io/bron/preview/**

## Commando's

Org-conventie: [repo-scripts](docs/specs/repo-scripts.md). Python **3.14**.

| Commando | Doel |
| -------- | ---- |
| `test` | catalogus-pytest |
| `validate` | catalogus index validate + `vsa validate zangstukken` |
| `catalogus` | catalogus CLI |
| `serve` | MkDocs preview zonder TEv2 |
| `serve-tev2` | MkDocs preview met TEv2 |
| `build` | TEv2 + MkDocs `--strict` (CI-pariteit) |
| `build --no-tev2` | MkDocs zonder TEv2 |

```cmd
cd /d C:\Git\orthodox-ronl\bron
serve
```

## Wat staat hier wel, en wat niet

- **Wel**: zangstukken onder `zangstukken/`, met `zangstuk.yaml` en brondocumenten
- **Wel**: metadata over zangstukken waarvan het bronbestand *niet* hier staat
  (`access:` bij copyright)
- **Niet**: afgeleide bestanden (SVG, MXL uit VSA) — zie [inhoudslevenscyclus](docs/specs/inhoudslevenscyclus.md)
- **Niet**: parochie-specifiek gebruik of samenstellingen (eigen repo's)

## Structuur (inhoud)

```
zangstukken/<zangstuk-id>/
  zangstuk.yaml
  sources/vsa|scan|musicxml/
composities/          # toekomst
docs/                 # → GitHub Pages (niet de zangstuk-inhoud zelf)
```

Zie [Zangstuk-formaat](docs/specs/zangstuk-formaat.md) en [Repo-structuur](docs/specs/repo-structuur.md).

## Copyright-gevoelig materiaal

Zie [Handleiding: copyright en access](docs/manuals/copyright-access.md).

## Gebruik door parochies

Parochies consumeren deze repository via build-time fetch (geen submodule).
Een publieke index (JSON) is gepland — zie plannen in `docs/plans/`.

## Licentie

Inhoud: [CC BY-SA 4.0](LICENSE-CONTENT). Code/scripts: [MIT](LICENSE-CODE).
