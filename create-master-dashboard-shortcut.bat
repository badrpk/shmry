@echo off
echo Creating SHMRY Master Admin Dashboard Desktop Shortcut...
echo.

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "MASTER_DASHBOARD_PATH=%CURRENT_DIR%master-admin-dashboard.html"

REM Get the desktop path
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul') do set "DESKTOP_PATH=%%b"

REM Create the shortcut
echo Creating shortcut on desktop...
echo @echo off > "%DESKTOP_PATH%\SHMRY Master Admin Dashboard.bat"
echo title SHMRY Master Admin Dashboard >> "%DESKTOP_PATH%\SHMRY Master Admin Dashboard.bat"
echo echo Opening SHMRY Master Admin Dashboard... >> "%DESKTOP_PATH%\SHMRY Master Admin Dashboard.bat"
echo start "" "%CURRENT_DIR%master-admin-dashboard.html" >> "%DESKTOP_PATH%\SHMRY Master Admin Dashboard.bat"
echo pause >> "%DESKTOP_PATH%\SHMRY Master Admin Dashboard.bat"

REM Create a VBS script for a proper shortcut with icon
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateMasterShortcut.vbs"
echo sLinkFile = "%DESKTOP_PATH%\SHMRY Master Admin Dashboard.lnk" >> "%TEMP%\CreateMasterShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateMasterShortcut.vbs"
echo oLink.TargetPath = "C:\Program Files\Internet Explorer\iexplore.exe" >> "%TEMP%\CreateMasterShortcut.vbs"
echo oLink.Arguments = "%CURRENT_DIR%master-admin-dashboard.html" >> "%TEMP%\CreateMasterShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateMasterShortcut.vbs"
echo oLink.Description = "SHMRY Master Admin Dashboard - Complete System Control Center" >> "%TEMP%\CreateMasterShortcut.vbs"
echo oLink.IconLocation = "C:\Program Files\Internet Explorer\iexplore.exe,0" >> "%TEMP%\CreateMasterShortcut.vbs"
echo oLink.WindowStyle = 1 >> "%TEMP%\CreateMasterShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateMasterShortcut.vbs"

REM Run the VBS script
cscript //nologo "%TEMP%\CreateMasterShortcut.vbs"

REM Clean up
del "%TEMP%\CreateMasterShortcut.vbs"

echo.
echo ✅ Master Dashboard shortcut created successfully!
echo 📍 Location: %DESKTOP_PATH%\SHMRY Master Admin Dashboard.lnk
echo 🚀 Double-click to open the master admin dashboard
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
echo 💡 You can also:
echo    - Right-click the shortcut to pin to Start Menu
echo    - Drag to taskbar for quick access
echo    - Use Windows + R and type: %CURRENT_DIR%master-admin-dashboard.html
echo.
pause
