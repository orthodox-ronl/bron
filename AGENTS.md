# AGENTS.md

Richtlijnen voor AI-assistenten in
[orthodox-groningen/bron](https://github.com/orthodox-groningen/bron).

Zuster-repo tooling: [VSA-tooling/AGENTS.md](https://github.com/orthodox-groningen/VSA-tooling/blob/main/AGENTS.md).

---

## Projectoverzicht

**bron** is de centrale bronrepository voor orthodoxe kerkmuziek (VSA). Parochies consumeren
deze repo via build-time fetch (geen submodule). Documentatie op GitHub Pages:

- Productie: https://orthodox-groningen.github.io/bron/
- Preview (niet-`main`): https://orthodox-groningen.github.io/bron/preview/

**Wel:** zangstukken (`zangstukken/`), `zangstuk.yaml`, scans, `.vsa`, metadata bij copyright (`access:`).

**Niet:** afgeleide SVG/MXL uit VSA; parochie-samenstellingen; tool-specs.

Licenties: [CC BY-SA 4.0](LICENSE-CONTENT) (inhoud), [MIT](LICENSE-CODE) (code/scripts).

---

## Terminologie en documentatie-eigendom

Normatieve glossary: **`docs/specs/terminologie.md`**

Vier niveaus: `zangstuk-id` → `variant-id` → `uitvoeringsvorm-id` → `representatie-id`

| Regel | Inhoud |
| ----- | ------ |
| R1–R5 | Zie terminologie §0 |
| D1    | Org-specs **alleen** in `bron/docs/`; andere repo's linken |
| D3    | Org-spec wijzigen → PR hier; daarna stubs in VSA-tooling controleren |

Zie `docs/specs/documentatie-eigendom.md`. Cursor: `.cursor/rules/orthodox-groningen-terminologie.mdc`.

**Vermijden:** `uv-id`, afkorting `uv`, **uitvoeringsalternatief**, impliciet `variant-id: standaard`.

---

## LLM Coding Guidelines

<!-- Gebaseerd op https://github.com/multica-ai/andrej-karpathy-skills -->

Gedragsrichtlijnen om veelvoorkomende LLM-fouten te verminderen. Bij triviale taken: gebruik je oordeel.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- If you write 200 lines and it could be 50, rewrite it.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code, comments, or formatting.
- Match existing style; remove orphans only from **your** changes.

### 4. Goal-Driven Execution

Define verifiable success criteria (`vsa validate zangstukken`, `mkdocs build --strict`) en loop tot ze slagen.

---

## Ontwikkelomgeving

| Vereiste      | Versie / tool                           |
| ------------- | --------------------------------------- |
| Python        | ≥ 3.12                                  |
| Docs lokaal   | MkDocs Material (`requirements-docs.txt`) |
| Catalogus     | `pip install -e ".[dev]"` in bron-root    |
| VSA-validatie | `vsa` CLI uit repo VSA-tooling          |

```cmd
cd /d C:\Git\orthodox-groningen\bron
scripts\docs-serve.cmd
```

VSA-validatie (VSA-tooling naast `bron`):

```cmd
cd /d C:\Git\orthodox-groningen\VSA-tooling
scripts\bootstrap.cmd
cd /d C:\Git\orthodox-groningen\bron
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
cd /d C:\Git\orthodox-groningen\bron
scripts\test.cmd
python -m catalogus.cli index validate --bron-root .
```

### Documentatie (MkDocs)

```cmd
cd /d C:\Git\orthodox-groningen\bron
scripts\docs-build.cmd
scripts\docs-serve.cmd
```

### Zangstukken valideren

```cmd
cd /d C:\Git\orthodox-groningen\bron
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
cd /d C:\Git\orthodox-groningen\bron
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

| Workflow                   | Trigger  | Doel                                       |
| -------------------------- | -------- | ------------------------------------------ |
| `validate-zangstukken.yml` | push, PR | `vsa validate zangstukken`                 |
| `validate-catalogus.yml`   | push, PR | pytest + `catalogus index validate`        |
| `docs-pages.yml`           | push     | MkDocs → GitHub Pages (prod of `/preview/`) |

---

## Markdown-tabellen

Kolommen alignen in de bron (padding met spaties); pipes in celinhoud escapen als `\|`.
