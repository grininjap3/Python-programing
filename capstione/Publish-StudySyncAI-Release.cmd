@echo off
setlocal
set "SCRIPT=%~dp0Publish-StudySyncAI-Release.ps1"
if not exist "%SCRIPT%" (
  echo Missing Publish-StudySyncAI-Release.ps1.
  pause
  exit /b 1
)
powershell.exe -NoLogo -NoProfile -File "%SCRIPT%"
set "RESULT=%ERRORLEVEL%"
if not "%RESULT%"=="0" pause
exit /b %RESULT%
