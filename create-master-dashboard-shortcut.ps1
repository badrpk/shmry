# SHMRY Master Admin Dashboard Desktop Shortcut Creator
Write-Host "Creating SHMRY Master Admin Dashboard Desktop Shortcut..." -ForegroundColor Green
Write-Host ""

# Get current directory and dashboard path
$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$MasterDashboardPath = Join-Path $CurrentDir "master-admin-dashboard.html"

# Get desktop path
$DesktopPath = [Environment]::GetFolderPath("Desktop")

Write-Host "Current Directory: $CurrentDir" -ForegroundColor Yellow
Write-Host "Master Dashboard Path: $MasterDashboardPath" -ForegroundColor Yellow
Write-Host "Desktop Path: $DesktopPath" -ForegroundColor Yellow
Write-Host ""

# Check if dashboard file exists
if (-not (Test-Path $MasterDashboardPath)) {
    Write-Host "Error: master-admin-dashboard.html not found!" -ForegroundColor Red
    Write-Host "Please run this script from the same directory as master-admin-dashboard.html" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Master Dashboard file found!" -ForegroundColor Green
Write-Host ""

# Create the shortcut
try {
    $ShortcutPath = Join-Path $DesktopPath "SHMRY Master Admin Dashboard.lnk"
    
    # Create WScript Shell object
    $WScriptShell = New-Object -ComObject WScript.Shell
    
    # Create shortcut object
    $Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
    
    # Set shortcut properties
    $Shortcut.TargetPath = "C:\Program Files\Internet Explorer\iexplore.exe"
    $Shortcut.Arguments = $MasterDashboardPath
    $Shortcut.WorkingDirectory = $CurrentDir
    $Shortcut.Description = "SHMRY Master Admin Dashboard - Complete System Control Center"
    $Shortcut.IconLocation = "C:\Program Files\Internet Explorer\iexplore.exe,0"
    $Shortcut.WindowStyle = 1
    
    # Save the shortcut
    $Shortcut.Save()
    
    Write-Host "Master Dashboard shortcut created successfully!" -ForegroundColor Green
    Write-Host "Location: $ShortcutPath" -ForegroundColor Yellow
    Write-Host ""
    
    # Create batch file for compatibility
    $BatchPath = Join-Path $DesktopPath "SHMRY Master Admin Dashboard.bat"
    $BatchContent = "@echo off`ntitle SHMRY Master Admin Dashboard`necho Opening SHMRY Master Admin Dashboard...`nstart "" `"$MasterDashboardPath`"`npause"
    
    $BatchContent | Out-File -FilePath $BatchPath -Encoding ASCII
    
    Write-Host "Batch file also created for compatibility" -ForegroundColor Green
    Write-Host "Batch Location: $BatchPath" -ForegroundColor Yellow
    Write-Host ""
    
    # Create a modern shortcut using PowerShell
    $ModernShortcutPath = Join-Path $DesktopPath "SHMRY Master Admin Dashboard (Modern).lnk"
    
    # Try to use modern browser if available
    $ModernBrowsers = @(
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "C:\Program Files\Mozilla Firefox\firefox.exe",
        "C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    )
    
    $BrowserPath = $null
    foreach ($browser in $ModernBrowsers) {
        if (Test-Path $browser) {
            $BrowserPath = $browser
            break
        }
    }
    
    if ($BrowserPath) {
        $ModernShortcut = $WScriptShell.CreateShortcut($ModernShortcutPath)
        $ModernShortcut.TargetPath = $BrowserPath
        $ModernShortcut.Arguments = $MasterDashboardPath
        $ModernShortcut.WorkingDirectory = $CurrentDir
        $ModernShortcut.Description = "SHMRY Master Admin Dashboard - Modern Browser Version"
        $ModernShortcut.IconLocation = $BrowserPath + ",0"
        $ModernShortcut.WindowStyle = 1
        $ModernShortcut.Save()
        
        Write-Host "Modern browser shortcut created!" -ForegroundColor Green
        Write-Host "Modern Location: $ModernShortcutPath" -ForegroundColor Yellow
        Write-Host ""
    }
    
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
Write-Host "1. Double-click 'SHMRY Master Admin Dashboard.lnk' on your desktop" -ForegroundColor White
Write-Host "2. Or use the batch file for compatibility" -ForegroundColor White
Write-Host "3. Or use the modern browser version if available" -ForegroundColor White
Write-Host ""
Write-Host "Master Dashboard Features:" -ForegroundColor Cyan
Write-Host "- Complete system overview and control" -ForegroundColor White
Write-Host "- Smart Storage System management" -ForegroundColor White
Write-Host "- Search Engine administration" -ForegroundColor White
Write-Host "- Backend Server control" -ForegroundColor White
Write-Host "- AI Model Manager" -ForegroundColor White
Write-Host "- Admin Device Network" -ForegroundColor White
Write-Host "- System Monitor & Reports" -ForegroundColor White
Write-Host ""
Write-Host "Additional options:" -ForegroundColor Cyan
Write-Host "- Right-click shortcut to Pin to Start Menu" -ForegroundColor White
Write-Host "- Drag shortcut to taskbar for quick access" -ForegroundColor White
Write-Host ""
Write-Host "Your SHMRY Master Admin Dashboard is ready!" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to exit"
