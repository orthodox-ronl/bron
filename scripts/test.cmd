@echo off
setlocal
cd /d "%~dp0.."
call scripts\_ensure.cmd --pip-e ".[dev]" --import catalogus --import pytest
if errorlevel 1 exit /b 1
python -m pytest %*
exit /b %errorlevel%
