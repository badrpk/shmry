# Create Desktop Shortcut for SHMRY Server
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\SHMRY Server.lnk")
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/k `"cd /d `"$PWD\deployment`" && node server.js`""
$Shortcut.WorkingDirectory = "$PWD\deployment"
$Shortcut.Description = "Start SHMRY Platform Server"
$Shortcut.IconLocation = "$PWD\deployment\server.js,0"
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
Write-Host "Location: $env:USERPROFILE\Desktop\SHMRY Server.lnk" -ForegroundColor Cyan
Write-Host "Double-click to start your server" -ForegroundColor Yellow
