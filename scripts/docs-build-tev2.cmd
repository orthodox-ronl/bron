@echo off
REM Build docs with TEv2 preprocessing, then MkDocs --strict (zelfde keten als CI).
setlocal
cd /d "%~dp0.."
set NO_MKDOCS_2_WARNING=1

call scripts\docs-tev2-run.cmd
if errorlevel 1 exit /b 1

python -m pip install -r requirements-docs.txt
if errorlevel 1 exit /b 1

python -m mkdocs build --strict -f generated\mkdocs.yml --site-dir ..\site %*
exit /b %errorlevel%
