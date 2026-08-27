@echo off
REM MkDocs build. Default = CI-parity (TEv2). Fast: build --no-tev2
setlocal
cd /d "%~dp0.."
set NO_MKDOCS_2_WARNING=1

if /I "%~1"=="--no-tev2" (
  shift
  call scripts\_ensure.cmd --pip-r requirements-docs.txt --import mkdocs
  if errorlevel 1 exit /b 1
  python -m mkdocs build --strict --site-dir site %*
  exit /b %errorlevel%
)

call scripts\docs-tev2-run.cmd
if errorlevel 1 exit /b 1

python -m mkdocs build --strict -f generated\mkdocs.yml --site-dir ..\site %*
exit /b %errorlevel%
