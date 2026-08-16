@echo off
echo.
echo ========================================
echo 🚀 SHMRY Production Server Startup
echo ========================================
echo.
echo Starting all essential SHMRY services...
echo.

echo 🌐 Starting Website Server (Port 80)...
start "SHMRY Website" cmd /k "node deployment/website-server.js"

echo 🔧 Starting Admin Server (Port 3001)...
start "SHMRY Admin" cmd /k "node deployment/admin-server.js"

echo 🎯 Starting Master Server (Port 3002)...
start "SHMRY Master" cmd /k "node deployment/master-server.js"

echo 🌍 Starting Network Discovery (Port 3003)...
start "SHMRY Network" cmd /k "node deployment/network-discovery.js"

echo.
echo ✅ All SHMRY services started successfully!
echo.
echo 🌐 Access URLs:
echo ===============
echo   • Main Website: http://154.57.212.38:80
echo   • Admin Dashboard: http://154.57.212.38:3001
echo   • Master Dashboard: http://154.57.212.38:3002
echo   • Network Discovery: http://154.57.212.38:3003
echo.
echo 🚀 Live Website: https://www.shmry.com
echo.
pause
