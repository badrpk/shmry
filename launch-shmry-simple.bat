@echo off
title SHMRY Simple Launcher
color 0E

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 SHMRY Simple Launcher
echo.

echo 📍 Choose your dashboard:
echo.
echo 1. 🎛️ Master Admin Dashboard
echo 2. 💾 Smart Storage Dashboard
echo 3. 🔍 Search Engine
echo 4. 🎨 HTML Launcher Page
echo 5. ❌ Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🎛️ Opening Master Admin Dashboard...
    start "" "%~dp0master-admin-dashboard.html"
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo 💾 Opening Smart Storage Dashboard...
    start "" "%~dp0admin-dashboard.html"
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo 🔍 Opening Search Engine...
    start "" "%~dp0search\index.html"
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo 🎨 Opening HTML Launcher Page...
    start "" "%~dp0launch-dashboards.html"
    goto :end
)

if "%choice%"=="5" (
    echo.
    echo 👋 Goodbye!
    goto :end
)

echo.
echo ❌ Invalid choice. Please enter 1-5.
goto :menu

:end
echo.
echo ✅ Dashboard launched successfully!
echo 💡 You can now use your SHMRY systems
echo.
pause
