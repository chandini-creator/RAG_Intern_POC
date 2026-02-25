@echo off
title MediQuery Server
cd /d "%~dp0"
echo Stopping any existing server on port 8000...
powershell -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"
timeout /t 2 /nobreak >nul
echo.
echo Starting MediQuery...
echo When you see "Uvicorn running on http://0.0.0.0:8000", open in your browser:
echo   http://localhost:8000
echo.
echo Keep this window open. Closing it will stop the server.
echo.
"%LOCALAPPDATA%\GenAI-venv\Scripts\python.exe" run.py
pause
