@echo off
REM Catalogus-tests — altijd dezelfde Python als `python` in PATH.
setlocal
cd /d "%~dp0.."

python -m pip install -e ".[dev]"
if errorlevel 1 exit /b 1

python -m pytest %*
exit /b %errorlevel%
