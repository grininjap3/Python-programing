@echo off
setlocal
set "SCRIPT=%~dp0Install-StudySyncAI.ps1"
if not exist "%SCRIPT%" (
  echo Missing Install-StudySyncAI.ps1. Keep it beside this file.
  pause
  exit /b 1
)
powershell.exe -NoLogo -NoProfile -File "%SCRIPT%"
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" pause
exit /b %RESULT%
