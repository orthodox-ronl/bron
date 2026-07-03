@echo off
REM Wrapper voor catalogus CLI — zelfde gedrag als `catalogus` op PATH.
setlocal
cd /d "%~dp0.."
python -m catalogus.cli %*
exit /b %errorlevel%
