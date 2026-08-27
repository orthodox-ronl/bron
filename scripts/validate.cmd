@echo off
setlocal
cd /d "%~dp0.."
call scripts\_ensure.cmd --pip-e ".[dev]" --vsa --import catalogus
if errorlevel 1 exit /b 1
python -m catalogus.cli index validate --bron-root .
if errorlevel 1 exit /b 1
vsa validate zangstukken
exit /b %errorlevel%
