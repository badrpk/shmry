@echo off
title SHMRY Main Dashboard
color 0A

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 Opening SHMRY Main Dashboard
echo.

echo 📍 Opening main dashboard...
echo 💡 This will open in your default web browser
echo.

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "MAIN_FILE=%CURRENT_DIR%SHMRY-MAIN.html"

echo File: %MAIN_FILE%
echo.

REM Open the HTML file directly
start "" "%MAIN_FILE%"

echo ✅ Main Dashboard opened successfully!
echo.
echo 💡 Available Options:
echo    🎛️ Master Admin Dashboard
echo    💾 Smart Storage Dashboard
echo    🔍 AI Search Engine
echo.
echo 🚀 Click any dashboard button to get started!
echo.
pause
