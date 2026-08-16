@echo off
title SHMRY Master Admin Dashboard
color 0B

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 MASTER ADMIN DASHBOARD - Complete System Control
echo.

echo 📍 Opening SHMRY Master Admin Dashboard...
echo 💡 This will open in your default web browser
echo.

REM Get the current directory and convert to proper file:// URL
set "CURRENT_DIR=%~dp0"
set "DASHBOARD_FILE=%CURRENT_DIR%master-admin-dashboard.html"

REM Convert backslashes to forward slashes for URL
set "DASHBOARD_FILE=%DASHBOARD_FILE:\=/%"

REM Create proper file:// URL
set "FILE_URL=file:///%DASHBOARD_FILE%"

echo File URL: %FILE_URL%
echo.

REM Try to open with default browser using file:// protocol
start "" "%FILE_URL%"

echo ✅ Master Dashboard launched successfully!
echo.
echo 💡 Master Dashboard Features:
echo    🚀 Complete system overview and control
echo    💾 Smart Storage System management
echo    🔍 Search Engine administration
echo    🖥️ Backend Server control
echo    📥 AI Model Manager
echo    🌐 Admin Device Network
echo    📊 System Monitor & Reports
echo.
echo 🔧 Quick Access from Master Dashboard:
echo    - Smart Storage Dashboard
echo    - Search Engine Interface
echo    - Server Status & Control
echo    - AI Model Management
echo    - Admin Device Control
echo    - System Monitoring
echo.
echo ⌨️ Keyboard Shortcuts:
echo    - Refresh: Ctrl+R
echo    - Open Search: Ctrl+S
echo    - Open Storage: Ctrl+A
echo.
echo 🚀 Control all SHMRY systems from one central dashboard!
echo.

pause
