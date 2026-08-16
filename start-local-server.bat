@echo off
title SHMRY Local Server
color 0B

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 Starting Local Web Server
echo.

echo 📍 Starting local web server...
echo 💡 This will serve your dashboards properly
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python found! Starting server...
    echo.
    echo 🌐 Server will be available at: http://localhost:8000
    echo 📱 Dashboards will open automatically
    echo.
    echo 💡 Press Ctrl+C to stop the server
    echo.
    
    REM Start Python server and open dashboards
    start "" "http://localhost:8000/open-dashboards.html"
    python -m http.server 8000
    goto :end
)

REM Check if Node.js is available
node --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Node.js found! Starting server...
    echo.
    echo 🌐 Server will be available at: http://localhost:3000
    echo 📱 Dashboards will open automatically
    echo.
    echo 💡 Press Ctrl+C to stop the server
    echo.
    
    REM Start Node.js server and open dashboards
    start "" "http://localhost:3000/open-dashboards.html"
    npx http-server -p 3000
    goto :end
)

REM If neither Python nor Node.js is available
echo ❌ Neither Python nor Node.js found!
echo.
echo 💡 Installing Python (recommended):
echo    1. Go to https://python.org/downloads
echo    2. Download and install Python 3.x
echo    3. Make sure to check "Add to PATH"
echo    4. Restart this script
echo.
echo 💡 Or install Node.js:
echo    1. Go to https://nodejs.org
echo    2. Download and install Node.js LTS
echo    3. Restart this script
echo.
echo 🔧 Alternative: Use the simple launcher
echo    Double-click: launch-shmry-simple.bat
echo.

:end
pause
