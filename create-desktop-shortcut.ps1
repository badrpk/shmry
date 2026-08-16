# SHMRY Admin Dashboard Desktop Shortcut Creator
Write-Host "Creating SHMRY Admin Dashboard Desktop Shortcut..." -ForegroundColor Green
Write-Host ""

# Get current directory and dashboard path
$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DashboardPath = Join-Path $CurrentDir "admin-dashboard.html"

# Get desktop path
$DesktopPath = [Environment]::GetFolderPath("Desktop")

Write-Host "Current Directory: $CurrentDir" -ForegroundColor Yellow
Write-Host "Dashboard Path: $DashboardPath" -ForegroundColor Yellow
Write-Host "Desktop Path: $DesktopPath" -ForegroundColor Yellow
Write-Host ""

# Check if dashboard file exists
if (-not (Test-Path $DashboardPath)) {
    Write-Host "Error: admin-dashboard.html not found!" -ForegroundColor Red
    Write-Host "Please run this script from the same directory as admin-dashboard.html" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Dashboard file found!" -ForegroundColor Green
Write-Host ""

# Create the shortcut
try {
    $ShortcutPath = Join-Path $DesktopPath "SHMRY Admin Dashboard.lnk"
    
    # Create WScript Shell object
    $WScriptShell = New-Object -ComObject WScript.Shell
    
    # Create shortcut object
    $Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
    
    # Set shortcut properties
    $Shortcut.TargetPath = "C:\Program Files\Internet Explorer\iexplore.exe"
    $Shortcut.Arguments = $DashboardPath
    $Shortcut.WorkingDirectory = $CurrentDir
    $Shortcut.Description = "SHMRY Admin Dashboard - Smart Storage Management"
    $Shortcut.IconLocation = "C:\Program Files\Internet Explorer\iexplore.exe,0"
    $Shortcut.WindowStyle = 1
    
    # Save the shortcut
    $Shortcut.Save()
    
    Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
    Write-Host "Location: $ShortcutPath" -ForegroundColor Yellow
    Write-Host ""
    
    # Create batch file for compatibility
    $BatchPath = Join-Path $DesktopPath "SHMRY Admin Dashboard.bat"
    $BatchContent = "@echo off`ntitle SHMRY Admin Dashboard`necho Opening SHMRY Admin Dashboard...`nstart "" `"$DashboardPath`"`npause"
    
    $BatchContent | Out-File -FilePath $BatchPath -Encoding ASCII
    
    Write-Host "Batch file also created for compatibility" -ForegroundColor Green
    Write-Host "Batch Location: $BatchPath" -ForegroundColor Yellow
    Write-Host ""
    
    # Clean up COM objects
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($WScriptShell) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    
} catch {
    Write-Host "Error creating shortcut: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "All shortcuts created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "How to use:" -ForegroundColor Cyan
Write-Host "1. Double-click 'SHMRY Admin Dashboard.lnk' on your desktop" -ForegroundColor White
Write-Host "2. Or use the batch file for compatibility" -ForegroundColor White
Write-Host ""
Write-Host "Additional options:" -ForegroundColor Cyan
Write-Host "- Right-click shortcut to Pin to Start Menu" -ForegroundColor White
Write-Host "- Drag shortcut to taskbar for quick access" -ForegroundColor White
Write-Host ""
Write-Host "Your SHMRY Admin Dashboard is ready!" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
