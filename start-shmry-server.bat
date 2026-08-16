@echo off
title SHMRY Server - Auto Start
color 0B

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 Starting SHMRY Server Automatically
echo.

cd /d "%~dp0deployment"
echo 📍 Starting server from: %CD%
echo 🌐 Server will be available at: http://localhost:3000
echo 🌍 Product pages will be accessible
echo.
echo 💡 Keep this window open to keep the server running
echo 💡 Close this window to stop the server
echo.

node server.js

pause
