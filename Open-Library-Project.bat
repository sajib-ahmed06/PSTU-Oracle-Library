@echo off
setlocal
cd /d "%~dp0"

if not exist "frontend\index.html" (
    echo Error: frontend\index.html was not found.
    pause
    exit /b 1
)

start "PSTU Library Server" /min powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1"
timeout /t 8 /nobreak >nul
start "" "http://localhost:8091"
exit /b 0
