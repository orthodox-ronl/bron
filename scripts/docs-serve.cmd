@echo off
REM MkDocs serve — python -m + geen Material MkDocs-2.0-banner (zie requirements-docs.txt: mkdocs<2).
setlocal
cd /d "%~dp0.."
set NO_MKDOCS_2_WARNING=1

python -m pip install -r requirements-docs.txt
if errorlevel 1 exit /b 1

copy /y mkdocs.yml mkdocs.yml.serve-bak >nul
if errorlevel 1 exit /b 1

REM Zelfde tijdstempel-patroon als docs-pages.yml (lokaal: Europe/Amsterdam).
for /f "usebackq delims=" %%I in (`python -c "from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime.now(ZoneInfo('Europe/Amsterdam')).strftime('%%Y-%%m-%%d %%H:%%M %%Z'))"`) do set "BUILD_TIME=%%I"
python scripts\set-mkdocs-site-url.py "https://orthodox-ronl.github.io/bron/" false "%BUILD_TIME%" "local"
if errorlevel 1 (
  copy /y mkdocs.yml.serve-bak mkdocs.yml >nul
  del mkdocs.yml.serve-bak 2>nul
  exit /b 1
)

echo.
echo MkDocs serve — open http://127.0.0.1:8000/  (Ctrl+C om te stoppen)
echo Gegenereerd-stempel: %BUILD_TIME%
echo.
python -m mkdocs serve %*
set "SERVE_EXIT=%ERRORLEVEL%"

copy /y mkdocs.yml.serve-bak mkdocs.yml >nul
del mkdocs.yml.serve-bak 2>nul

exit /b %SERVE_EXIT%
