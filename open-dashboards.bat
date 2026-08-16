@echo off
title Open SHMRY Dashboards
color 0A

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 Opening SHMRY Dashboards
echo.

echo 📍 Opening dashboard access page...
echo 💡 This will open in your default web browser
echo.

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "DASHBOARD_FILE=%CURRENT_DIR%open-dashboards.html"

echo File: %DASHBOARD_FILE%
echo.

REM Open the HTML file directly
start "" "%DASHBOARD_FILE%"

echo ✅ Dashboard page opened successfully!
echo.
echo 💡 Available Options:
echo    🎛️ Master Admin Dashboard
echo    💾 Smart Storage Dashboard
echo    🔍 Search Engine
echo.
echo 🚀 Click any dashboard button to get started!
echo.

pause
