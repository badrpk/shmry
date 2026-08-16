@echo off
title Shmry Edge Computing System Launcher
color 0A

echo.
echo ========================================
echo    SHMRY EDGE COMPUTING SYSTEM
echo ========================================
echo.
echo Welcome to Shmry Edge Computing!
echo Your enterprise edge computing platform
echo for millions of devices worldwide.
echo.

echo Starting Shmry Components...
echo.

echo 🌐 Opening Shmry Website...
start "" "D:\shmry-edge-computing\website\shmry-website.html"

echo.
echo 📊 Opening Shmry Dashboard...
start "" "D:\shmry-edge-computing\dashboard\shmry-edge-computing.html"

echo.
echo 🚀 Opening Shmry Deployment Guide...
start "" "D:\shmry-edge-computing\deployment\SHMRY_DEPLOYMENT_GUIDE.md"

echo.
echo ========================================
echo    SHMRY SYSTEM LAUNCHED!
echo ========================================
echo.
echo ✅ Shmry Website: Professional landing page
echo ✅ Shmry Dashboard: Edge computing cluster
echo ✅ Deployment Guide: Vercel setup instructions
echo.
echo Your Shmry Edge Computing System is now
echo running from D:\shmry-edge-computing\
echo.
echo To deploy to www.shmry.com:
echo 1. Run deploy-vercel.bat in deployment folder
echo 2. Follow the deployment guide
echo.
echo Press any key to close this launcher...
pause > nul
