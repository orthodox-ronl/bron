@echo off
setlocal
cd /d "%~dp0.."
call scripts\_ensure.cmd --pip-e ".[dev]" --import catalogus
if errorlevel 1 exit /b 1
python -m catalogus.cli %*
exit /b %errorlevel%
