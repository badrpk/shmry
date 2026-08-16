@echo off
echo Creating SHMRY Admin Dashboard Desktop Shortcut...
echo.

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "DASHBOARD_PATH=%CURRENT_DIR%admin-dashboard.html"

REM Get the desktop path
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul') do set "DESKTOP_PATH=%%b"

REM Create the shortcut
echo Creating shortcut on desktop...
echo @echo off > "%DESKTOP_PATH%\SHMRY Admin Dashboard.bat"
echo start "" "%CURRENT_DIR%admin-dashboard.html" >> "%DESKTOP_PATH%\SHMRY Admin Dashboard.bat"

REM Create a VBS script for a proper shortcut with icon
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP_PATH%\SHMRY Admin Dashboard.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "C:\Program Files\Internet Explorer\iexplore.exe" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Arguments = "%CURRENT_DIR%admin-dashboard.html" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "SHMRY Admin Dashboard - Smart Storage Management" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "C:\Program Files\Internet Explorer\iexplore.exe,0" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WindowStyle = 1 >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

REM Run the VBS script
cscript //nologo "%TEMP%\CreateShortcut.vbs"

REM Clean up
del "%TEMP%\CreateShortcut.vbs"

echo.
echo ✅ Desktop shortcut created successfully!
echo 📍 Location: %DESKTOP_PATH%\SHMRY Admin Dashboard.lnk
echo 🚀 Double-click to open the admin dashboard
echo.
echo 💡 You can also:
echo    - Right-click the shortcut to pin to Start Menu
echo    - Drag to taskbar for quick access
echo    - Use Windows + R and type: %CURRENT_DIR%admin-dashboard.html
echo.
pause
