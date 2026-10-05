@echo off
setlocal
cd /d "%~dp0"

python backend\setup_database.py

echo.
if errorlevel 1 (
    echo Database setup failed. Read the Oracle error above.
) else (
    echo You can now open Open-Library-Project.bat.
)
pause
