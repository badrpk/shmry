@echo off
title Create Working SHMRY Desktop Shortcuts
color 0A

echo.
echo  ███████╗██╗  ██╗███╗   ███╗██████╗ ██╗   ██╗
echo  ██╔════╝██║  ██║████╗ ████║██╔══██╗╚██╗ ██╔╝
echo  ███████╗███████║██╔████╔██║██████╔╝ ╚████╔╝ 
echo  ╚════██║██╔══██║██║╚██╔╝██║██╔══██╗  ╚██╔╝  
echo  ███████║██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
echo  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
echo.
echo  🚀 Creating Working Desktop Shortcuts
echo.

echo 📍 Creating desktop shortcuts that will definitely work...
echo.

REM Get current directory
set "CURRENT_DIR=%~dp0"
set "DESKTOP_DIR=%USERPROFILE%\Desktop"

echo Current Directory: %CURRENT_DIR%
echo Desktop Directory: %DESKTOP_DIR%
echo.

REM Create Master Admin Dashboard shortcut
echo 🎛️ Creating Master Admin Dashboard shortcut...
set "MASTER_FILE=%CURRENT_DIR%master-admin-dashboard.html"
set "MASTER_SHORTCUT=%DESKTOP_DIR%\SHMRY Master Dashboard.lnk"

echo File: %MASTER_FILE%
echo Shortcut: %MASTER_SHORTCUT%

REM Create shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%MASTER_SHORTCUT%'); $Shortcut.TargetPath = '%MASTER_FILE%'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'SHMRY Master Admin Dashboard'; $Shortcut.IconLocation = '%CURRENT_DIR%favicon.ico,0'; $Shortcut.Save()}"

if exist "%MASTER_SHORTCUT%" (
    echo ✅ Master Dashboard shortcut created successfully!
) else (
    echo ❌ Failed to create Master Dashboard shortcut
)

echo.

REM Create Smart Storage Dashboard shortcut
echo 💾 Creating Smart Storage Dashboard shortcut...
set "STORAGE_FILE=%CURRENT_DIR%admin-dashboard.html"
set "STORAGE_SHORTCUT=%DESKTOP_DIR%\SHMRY Storage Dashboard.lnk"

echo File: %STORAGE_FILE%
echo Shortcut: %STORAGE_SHORTCUT%

REM Create shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STORAGE_SHORTCUT%'); $Shortcut.TargetPath = '%STORAGE_FILE%'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'SHMRY Smart Storage Dashboard'; $Shortcut.IconLocation = '%CURRENT_DIR%favicon.ico,0'; $Shortcut.Save()}"

if exist "%STORAGE_SHORTCUT%" (
    echo ✅ Storage Dashboard shortcut created successfully!
) else (
    echo ❌ Failed to create Storage Dashboard shortcut
)

echo.

REM Create Search Engine shortcut
echo 🔍 Creating Search Engine shortcut...
set "SEARCH_FILE=%CURRENT_DIR%search\index.html"
set "SEARCH_SHORTCUT=%DESKTOP_DIR%\SHMRY Search Engine.lnk"

echo File: %SEARCH_FILE%
echo Shortcut: %SEARCH_SHORTCUT%

REM Create shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SEARCH_SHORTCUT%'); $Shortcut.TargetPath = '%SEARCH_FILE%'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'SHMRY AI Search Engine'; $Shortcut.IconLocation = '%CURRENT_DIR%favicon.ico,0'; $Shortcut.Save()}"

if exist "%SEARCH_SHORTCUT%" (
    echo ✅ Search Engine shortcut created successfully!
) else (
    echo ❌ Failed to create Search Engine shortcut
)

echo.

REM Create Main Launcher shortcut
echo 🚀 Creating Main Launcher shortcut...
set "LAUNCHER_FILE=%CURRENT_DIR%SHMRY-MAIN.html"
set "LAUNCHER_SHORTCUT=%DESKTOP_DIR%\SHMRY Main Launcher.lnk"

echo File: %LAUNCHER_FILE%
echo Shortcut: %LAUNCHER_SHORTCUT%

REM Create shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%LAUNCHER_SHORTCUT%'); $Shortcut.TargetPath = '%LAUNCHER_FILE%'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'SHMRY Main Dashboard Launcher'; $Shortcut.IconLocation = '%CURRENT_DIR%favicon.ico,0'; $Shortcut.Save()}"

if exist "%LAUNCHER_SHORTCUT%" (
    echo ✅ Main Launcher shortcut created successfully!
) else (
    echo ❌ Failed to create Main Launcher shortcut
)

echo.
echo 🎉 All shortcuts created!
echo.
echo 💡 Your new desktop shortcuts:
echo    🎛️ SHMRY Master Dashboard
echo    💾 SHMRY Storage Dashboard  
echo    🔍 SHMRY Search Engine
echo    🚀 SHMRY Main Launcher
echo.
echo 🚀 Double-click any shortcut to test!
echo.
pause
