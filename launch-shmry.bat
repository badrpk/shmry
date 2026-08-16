@echo off
title SHMRY Launcher
color 0E

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 SHMRY Dashboard Launcher
echo.

echo 📍 Opening SHMRY Dashboard Launcher...
echo 💡 This will open in your default web browser
echo.

REM Get the current directory and convert to proper file:// URL
set "CURRENT_DIR=%~dp0"
set "LAUNCHER_FILE=%CURRENT_DIR%launch-dashboards.html"

REM Convert backslashes to forward slashes for URL
set "LAUNCHER_FILE=%LAUNCHER_FILE:\=/%"

REM Create proper file:// URL
set "FILE_URL=file:///%LAUNCHER_FILE%"

echo File URL: %FILE_URL%
echo.

REM Try to open with default browser using file:// protocol
start "" "%FILE_URL%"

echo ✅ SHMRY Launcher opened successfully!
echo.
echo 💡 Available Dashboards:
echo    🎛️ Master Admin Dashboard - Complete system control
echo    💾 Smart Storage Dashboard - Storage management
echo    🔍 Search Engine - AI-powered search
echo.
echo 🔧 Quick Access:
echo    - Ctrl+M: Master Dashboard
echo    - Ctrl+S: Storage Dashboard
echo    - Ctrl+E: Search Engine
echo.
echo 🚀 Choose your dashboard and get started!
echo.

pause
