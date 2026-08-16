@echo off
title SHMRY Launcher
color 0B

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 Opening SHMRY Launcher
echo.

echo 📍 Opening launcher page...
echo 💡 This will open in your default web browser
echo.

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "LAUNCHER_FILE=%CURRENT_DIR%launch.html"

echo File: %LAUNCHER_FILE%
echo.

REM Open the HTML file directly
start "" "%LAUNCHER_FILE%"

echo ✅ Launcher opened successfully!
echo.
echo 💡 Available Options:
echo    🎛️ Master Admin Dashboard
echo    💾 Smart Storage Dashboard
echo    🔍 Search Engine
echo.
echo 🚀 Click any dashboard button to get started!
echo.
pause
