@echo off
title SHMRY Admin Device Manager
color 0A

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🖥️  ADMIN DEVICE MANAGER - Add/Remove Devices
echo  ================================================
echo.

REM Check if server is running
netstat -an | findstr :3000 >nul
if %errorlevel% neq 0 (
    echo ❌ SHMRY Server is not running!
    echo.
    echo 📋 Starting server now...
    echo.
    start "SHMRY Server" cmd /k "cd /d "%~dp0deployment" && node server.js"
    echo ⏳ Waiting for server to start...
    timeout /t 3 /nobreak >nul
)

echo ✅ Opening Admin Device Manager...
echo.
echo 🌐 URL: http://localhost:3000/admin-device-manager.html
echo.

REM Open the admin device manager in default browser
start http://localhost:3000/admin-device-manager.html

echo 🎯 Admin Device Manager opened in your browser!
echo.
echo 💡 You can now:
echo    • Add new admin devices
echo    • Delete existing devices  
echo    • Monitor device status
echo    • View system statistics
echo.
echo Press any key to close this window...
pause >nul
