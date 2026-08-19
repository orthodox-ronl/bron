---
doc_type: workflow-guide
audience: "P5 — Docs-/tool-contributor"
---
# GitHub Pages — instelling

De MkDocs-site wordt door GitHub Actions gebouwd en naar de branch **`gh-pages`**
gepusht. GitHub Pages moet die branch **serveren** — niet `main`.

## Eenmalige instelling

1. **Repository → Settings → Pages**
2. **Build and deployment → Source:** `Deploy from a branch`
3. **Branch:** `gh-pages` — map **`/ (root)`**
4. **Save**

Boven aan de pagina moet verschijnen:

> Your site is live at **https://orthodox-ronl.github.io/bron/**

## Deploy via workflow

| Push naar     | Doel op `gh-pages` | URL                                                |
| ------------- | ------------------ | -------------------------------------------------- |
| `main`        | root (productie)   | https://orthodox-ronl.github.io/bron/         |
| andere branch | `preview/`         | https://orthodox-ronl.github.io/bron/preview/ |

Workflow: `.github/workflows/docs-pages.yml` — bouwt MkDocs, uploadt een artifact,
en roept de herbruikbare deploy-workflow uit
[`VSA-tooling/pages-deploy-reusable.yml`](https://github.com/orthodox-ronl/VSA-tooling/blob/main/.github/workflows/pages-deploy-reusable.yml)
aan (`keep_files: true`, publicatiecheck vóór deploy).

## Veelvoorkomend probleem: je ziet README i.p.v. MkDocs

**Symptoom:** op github.io staat de tekst uit **`README.md`** (repo-root), zonder
header-tabs, zonder Material-thema.

**Oorzaak:** Pages staat op branch **`main`** (Jekyll rendert README), terwijl de
gebouwde site op **`gh-pages`** staat.

**Oplossing:** Settings → Pages → branch **`gh-pages`**, folder **`/ (root)`** —
niet `main`, niet `/docs`.

**Controle:** op `gh-pages` hoort `index.html` te beginnen met MkDocs/Material
(`md-header`, `md-tabs`). Op `main` staat alleen bron-Markdown in `docs/`.

## Workflow-rechten

Settings → Actions → General → **Workflow permissions** →
**Read and write permissions** (als deploy naar `gh-pages` faalt).

## Favicon

Statische assets staan in `docs/images/` (favicon.ico, png-varianten) en worden
via `mkdocs.yml` / theme meegebouwd.

## Lokaal

```cmd
cd /d C:\Git\orthodox-ronl\bron
scripts\docs-serve.cmd
```

(`scripts\docs-serve.cmd` zet `NO_MKDOCS_2_WARNING=1` — onderdrukt de Material-banner over MkDocs 2.0; wij blijven op MkDocs 1.x via `requirements-docs.txt`.)
