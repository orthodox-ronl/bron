@echo off
REM MkDocs build — python -m + geen Material MkDocs-2.0-banner (zie requirements-docs.txt: mkdocs<2).
setlocal
cd /d "%~dp0.."
set NO_MKDOCS_2_WARNING=1

python -m pip install -r requirements-docs.txt
if errorlevel 1 exit /b 1

python -m mkdocs build --strict --site-dir site %*
exit /b %errorlevel%
