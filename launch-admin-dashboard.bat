@echo off
title SHMRY Admin Dashboard
color 0A

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 Smart Storage Management & AI Model Control Center
echo.

echo 📍 Opening SHMRY Admin Dashboard...
echo 💡 This will open in your default web browser
echo.

REM Get the current directory and convert to proper file:// URL
set "CURRENT_DIR=%~dp0"
set "DASHBOARD_FILE=%CURRENT_DIR%admin-dashboard.html"

REM Convert backslashes to forward slashes for URL
set "DASHBOARD_FILE=%DASHBOARD_FILE:\=/%"

REM Create proper file:// URL
set "FILE_URL=file:///%DASHBOARD_FILE%"

echo File URL: %FILE_URL%
echo.

REM Try to open with default browser using file:// protocol
start "" "%FILE_URL%"

echo ✅ Dashboard launched successfully!
echo.
echo 💡 Dashboard Features:
echo    💾 Real-time storage monitoring
echo    📥 Download management
echo    🌐 Admin device control
echo    🚨 Emergency cleanup tools
echo    📊 System health monitoring
echo.
echo 🔧 Quick Access:
echo    - Refresh: Ctrl+R
echo    - Emergency Cleanup: Ctrl+E
echo    - Force Admin Redirects: Ctrl+A
echo.
echo 🚀 Continue working on SHMRY while monitoring storage!
echo.

pause
