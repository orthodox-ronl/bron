# AGENTS.md

Richtlijnen voor AI-assistenten in
[orthodox-ronl/bron](https://github.com/orthodox-ronl/bron).

Zuster-repo tooling: [VSA-tooling/AGENTS.md](https://github.com/orthodox-ronl/VSA-tooling/blob/main/AGENTS.md).

---

## Projectoverzicht

**bron** is de centrale bronrepository voor orthodoxe kerkmuziek (VSA). Parochies consumeren
deze repo via build-time fetch (geen submodule). Documentatie op GitHub Pages:

- Productie: https://orthodox-ronl.github.io/bron/
- Preview (niet-`main`): https://orthodox-ronl.github.io/bron/preview/

**Wel:** zangstukken (`zangstukken/`), `zangstuk.yaml`, scans, `.vsa`, metadata bij copyright (`access:`).

**Niet:** afgeleide SVG/MXL uit VSA; parochie-samenstellingen; tool-specs.

Licenties: [CC BY-SA 4.0](LICENSE-CONTENT) (inhoud), [MIT](LICENSE-CODE) (code/scripts).

---

## Terminologie

Normatieve glossary: `docs/specs/terminologie.md` · Vier niveaus: `zangstuk-id` → `variant-id` → `uitvoeringsvorm-id` → `representatie-id`

**Vermijden:** `uv-id`, afkorting `uv`, **uitvoeringsalternatief**, impliciet `variant-id: standaard`.

Docs-prose (persona’s, paginatypen, jargon→TermRef, foutpaden, term-sjabloon):
[schrijfconventies](docs/specs/schrijfconventies.md) en
[term-entry-sjabloon](docs/specs/term-entry-sjabloon.md).

---

## Ontwikkelomgeving

| Vereiste      | Versie / tool                             |
| ------------- | ----------------------------------------- |
| Python        | ≥ 3.12                                    |
| Docs lokaal   | MkDocs Material (`requirements-docs.txt`) |
| Catalogus     | `pip install -e ".[dev]"` in bron-root    |
| VSA-validatie | `vsa` CLI uit repo VSA-tooling            |

```cmd
cd /d C:\Git\orthodox-ronl\bron
scripts\docs-serve.cmd
```

VSA-validatie (VSA-tooling naast `bron`):

```cmd
cd /d C:\Git\orthodox-ronl\VSA-tooling
scripts\bootstrap.cmd
cd /d C:\Git\orthodox-ronl\bron
vsa validate zangstukken
```

**Commando's voor de gebruiker:** één kopieerbaar cmd-blok, Windows-paden (`\`).

---

## Build, lint en test

### Catalogus (alias-resolver)

Gebruik `python -m` (niet bare `pytest` / `catalogus`) — voorkomt Python-mismatch op Windows.

Sjablonen: [sjabloon schrijven](docs/manuals/catalogus/sjabloon-schrijven.md),
spec [catalogus-samenstelling-zangstuk.md](docs/specs/catalogus-samenstelling-zangstuk.md).

```cmd
cd /d C:\Git\orthodox-ronl\bron
scripts\test.cmd
python -m catalogus.cli index validate --bron-root .
```

### Documentatie (MkDocs)

| Script                    | Doel                                              |
| ------------------------- | ------------------------------------------------- |
| `scripts\docs-serve.cmd`  | Snelle preview zonder TEv2                        |
| `scripts\docs-serve-tev2.cmd` | Preview met TermRefs (CI-parity)              |
| `scripts\docs-build.cmd`  | `mkdocs build --strict` zonder TEv2               |
| `scripts\docs-build-tev2.cmd` | TEv2 + TermRef-check + MkDocs (CI)            |

```cmd
cd /d C:\Git\orthodox-ronl\bron
npm install
scripts\docs-build-tev2.cmd
```

Handleiding: [docs/manuals/docs-bijdragen.md](docs/manuals/docs-bijdragen.md).

### Zangstukken valideren

```cmd
cd /d C:\Git\orthodox-ronl\bron
vsa validate zangstukken
```

Zelfde stap als CI (`.github/workflows/validate-zangstukken.yml`).

---

## Architectuur

```
zangstukken/<zangstuk-id>/
  zangstuk.yaml
  sources/vsa|scan|musicxml/
composities/          # toekomst
docs/                 # MkDocs → GitHub Pages
```

### Kernspecificaties (canoniek — wijzig hier)

| Document              | Pad                                   |
| --------------------- | ------------------------------------- |
| Terminologie          | `docs/specs/terminologie.md`          |
| Schrijfconventies     | `docs/specs/schrijfconventies.md`     |
| Term-entry-sjabloon   | `docs/specs/term-entry-sjabloon.md`   |
| Zangstuk-formaat      | `docs/specs/zangstuk-formaat.md`      |
| Repo-structuur        | `docs/specs/repo-structuur.md`        |
| Inhoudslevenscyclus   | `docs/specs/inhoudslevenscyclus.md`   |
| Documentatie-eigendom | `docs/specs/documentatie-eigendom.md` |

### `zangstuk.yaml`

- Canoniek **zangstuk-id**: `[a-z0-9_-]+`.
- Sources: `file:`, `access:` (copyright), of `status: nog-niet-getranscribeerd`.
- **`zangstuk.yaml` prevaleert** boven VSA-frontmatter binnen deze repo.

### Naamgevingspatronen

- Vast feest: `<type>-<gelegenheid-slug>`
- Zondagscyclus: `<type>-zondag-toon-<n>`
- `koormap_nummer` ≠ scan-sorteerprefix (`010-`, `020-`)

---

## Werkwijze bij wijzigingen

1. Org-brede spec → PR op `bron`; stubs/links in VSA-tooling controleren.
2. Nieuw zangstuk → `docs/manuals/zangstuk-toevoegen.md`.
3. Copyright → geen bestand; `access:` (`docs/manuals/copyright-access.md`).
4. Geen afgeleide SVG/MXL uit VSA-tool committen.

---

## Git commits

[Conventional Commits](https://www.conventionalcommits.org/). Typische scopes: `docs`, `zangstukken`, `ci`, `specs`.

```
docs(terminologie): verduidelijk representatie-id
fix(zangstukken): corrigeer tone in troparion-zondag-toon-3
```

**Maak alleen commits wanneer de gebruiker dat expliciet vraagt.**

---

## Pull requests

Gebruik **`gh` CLI**. Stel titel, body en commando **voor aan de gebruiker** vóór uitvoering.

```cmd
cd /d C:\Git\orthodox-ronl\bron
git push -u origin HEAD
gh pr create --title "docs(specs): korte beschrijving" --body "## Summary
- …

## Test plan
- [ ] vsa validate zangstukken
- [ ] mkdocs build --strict
"
```

---

## CI/CD

| Workflow                   | Trigger  | Doel                                        |
| -------------------------- | -------- | ------------------------------------------- |
| `validate-zangstukken.yml` | push, PR | `vsa validate zangstukken`                  |
| `validate-catalogus.yml`   | push, PR | pytest + `catalogus index validate`         |
| `docs-pages.yml`           | push     | MkDocs → GitHub Pages (prod of `/preview/`) |
