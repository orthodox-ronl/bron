---
doc_type: integratie
audience: "P5 — Docs-/tool-contributor; P6 — Spec-/PR-reviewer"
---
# Repo-scripts (orthodox-ronl)

**Status:** normatief (augustus 2026).

Gedeelde conventie voor uitvoerbare scripts in alle repository's van
[orthodox-ronl](https://github.com/orthodox-ronl). Tool-specifieke CLI's
(bijv. `vsa`) blijven in de tool-repo; deze spec gaat over **repo-root
commando's** onder `scripts/`.

---

## Pad en PATH

- Uitvoerbare gebruikerscommando's staan in `scripts/` t.o.v. de repo-root.
- Op Windows (`cmd.exe`) hoort `.\scripts` op PATH. In de **repo-root** is
  `test` dan `scripts\test.cmd`.
- Elk `.cmd` doet `cd` naar de repo-root via `%~dp0`.
- Alleen `.cmd` is de PATH-interface. Python-helpers in `scripts/` zijn geen
  commando's (niet tikken als `kalender` / `validate.py`).
- Zet geen executables `test`, `serve`, `build` of `check` in een globale
  venv-`Scripts`-map (bijv. `VSA-tooling\.venv\Scripts`): die staat vóór
  `.\scripts` op PATH en zou de repo-commando's overschaduwen.

Referentie-PATH (één ontwikkelmachine; `where` mag een andere map vinden):

| Tool | Verwacht pad |
| ---- | ------------ |
| Python 3.14 | `C:\Python314\` en `C:\Python314\Scripts\` |
| Hugo Extended | `C:\Git\tools\hugo` |
| `vsa` CLI | `C:\Git\orthodox-ronl\VSA-tooling\.venv\Scripts` |
| Repo-commando's | `.\scripts` |
| Node (TEv2) | `C:\Program Files\nodejs\` |

Lokale clones: `C:\Git\orthodox-ronl\<repo>` (GitHub-org: `orthodox-ronl`).

---

## Canonieke namen

Gebruikerscommando = bestandsnaam zonder `.cmd`. Alleen aanbieden als de
repo die functie heeft.

| Naam | Functie |
| ---- | ------- |
| `test` | Geautomatiseerde tests (pytest). Extra flags: `test -q`, `test -v`. |
| `check` | CI-spiegel / preflight: groen ≈ veilig om te pushen. |
| `build` | Statische productie-achtige build (Hugo of MkDocs). MkDocs: CI-pariteit (TEv2 waar CI TEv2 gebruikt). `build --no-tev2` = snelle MkDocs-build zonder TEv2. |
| `serve` | Lokale preview van de primaire site (Hugo of MkDocs). MkDocs: snel, zonder TEv2. |
| `serve-tev2` | MkDocs-preview met TEv2 (CI-pariteit), waar van toepassing. |
| `validate` | Alleen brondata/content valideren, zonder sitebuild. |
| `clean` | Generated/cache weg, waar de repo dat al had. |

Repo-specifiek mag blijven: `catalogus`, `import`, `sync-bron-zondagen`, `h`,
`run-example`.

**Niet** als gebruikersstap: `bootstrap`. Interne helper: `_ensure.cmd` /
`_ensure.py`. Oude namen (`docs-serve`, `serve-hugo`, `build-hugo`, `ci`)
mogen één cyclus als dunne alias blijven (`use: serve`).

---

## Toolchain (zelfde tool = zelfde versie)

Lokaal en CI gebruiken dezelfde pins. Geen matrix 3.12+3.14.

| Tool | Versie |
| ---- | ------ |
| Python | **3.14** (`python-version: "3.14"`; `requires-python = ">=3.14"`) |
| Hugo | **Extended 0.160.1** |
| Node | **22** (alleen TEv2-repo's) |

MkDocs Material: `>=9.5,<10` in `requirements-docs.txt` — gelijk houden tussen
`bron` en VSA-tooling.

Poort (augustus 2026): PyPI-metadata weigert 3.14 niet; pip-install + pytest
op 3.14 slaagde voor catalogus, vsa-tool (incl. Pillow) en heiligen-lage-landen.

---

## `_ensure`

Elk gebruikers-`.cmd` start met `call scripts\_ensure.cmd` plus de flags die
**dit** commando nodig heeft. Geen `activate`, geen nieuwe `.venv`.

1. `%PATH%` bevat `.\scripts`; anders: voeg `.\scripts` toe aan de
   gebruikers-PATH en werk in de repo-root.
2. `where python` + versie 3.14.x (geen WindowsApps-stub). Anders: Python 3.14
   installeren, `C:\Python314\` + `Scripts` op PATH.
3. Optioneel `hugo` (v0.160.1 + extended), `vsa`, `node` 22.x — `where` plus
   versie. Bij falen: referentiestappen, geen stille tweede venv.
4. Packages in **die** Python: import/stamp; zo niet `python -m pip install`.
   Catalogus: editable `..\bron` of `vendor\bron`. `vsa-tool`: editable
   `..\VSA-tooling` of `vendor\VSA-tooling` als `import vsa` ontbreekt.
5. Console-`echo`: eenvoudige ASCII (`->`, `-`).

CI (Linux) roept Python/Hugo rechtstreeks aan met dezelfde versies; `.cmd` is
voor lokaal Windows. Semantiek van `check`/`build` is gelijk.

---

## Documentatie

- Elke **README** somt de commando's van *die* repo (naam, doel, flags) en
  linkt naar deze spec — geen tweede org-glossary.
- Als de gepubliceerde site een **beheer-afdeling** heeft: dezelfde lijst daar
  (eigen pagina of in de how-to), gelinkt vanaf het beheer-overzicht.
- MkDocs-sites zonder `/beheer/`: dezelfde lijst in de contributor-handleiding.
- Scriptwijziging = README **en** beheer-/docs-pagina in dezelfde wijziging.
- `AGENTS.md`: dezelfde namen; `cd` naar `C:\Git\orthodox-ronl\<repo>`.

---

## Gerelateerd

- [Documentatie-eigendom](documentatie-eigendom.md)
- [Repo-structuur](repo-structuur.md)
