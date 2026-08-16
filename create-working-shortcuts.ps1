# Create Working SHMRY Desktop Shortcuts
Write-Host "🚀 Create Working SHMRY Desktop Shortcuts" -ForegroundColor Green
Write-Host ""

# Get current directory and desktop directory
$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = [Environment]::GetFolderPath("Desktop")

Write-Host "Current Directory: $CurrentDir" -ForegroundColor Yellow
Write-Host "Desktop Directory: $DesktopDir" -ForegroundColor Yellow
Write-Host ""

Write-Host "📍 Creating desktop shortcuts that will definitely work..." -ForegroundColor Cyan
Write-Host ""

# Function to create shortcut
function Create-Shortcut {
    param(
        [string]$TargetFile,
        [string]$ShortcutName,
        [string]$Description
    )
    
    $ShortcutPath = Join-Path $DesktopDir $ShortcutName
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = $TargetFile
        $Shortcut.WorkingDirectory = $CurrentDir
        $Shortcut.Description = $Description
        $Shortcut.Save()
        
        if (Test-Path $ShortcutPath) {
            Write-Host "✅ $ShortcutName created successfully!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ Failed to create $ShortcutName" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error creating $ShortcutName : $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Create Master Admin Dashboard shortcut
Write-Host "🎛️ Creating Master Admin Dashboard shortcut..." -ForegroundColor Cyan
$MasterFile = Join-Path $CurrentDir "master-admin-dashboard.html"
$Success1 = Create-Shortcut -TargetFile $MasterFile -ShortcutName "SHMRY Master Dashboard.lnk" -Description "SHMRY Master Admin Dashboard"

Write-Host ""

# Create Smart Storage Dashboard shortcut
Write-Host "💾 Creating Smart Storage Dashboard shortcut..." -ForegroundColor Cyan
$StorageFile = Join-Path $CurrentDir "admin-dashboard.html"
$Success2 = Create-Shortcut -TargetFile $StorageFile -ShortcutName "SHMRY Storage Dashboard.lnk" -Description "SHMRY Smart Storage Dashboard"

Write-Host ""

# Create Search Engine shortcut
Write-Host "🔍 Creating Search Engine shortcut..." -ForegroundColor Cyan
$SearchFile = Join-Path $CurrentDir "search\index.html"
$Success3 = Create-Shortcut -TargetFile $SearchFile -ShortcutName "SHMRY Search Engine.lnk" -Description "SHMRY AI Search Engine"

Write-Host ""

# Create Main Launcher shortcut
Write-Host "🚀 Creating Main Launcher shortcut..." -ForegroundColor Cyan
$LauncherFile = Join-Path $CurrentDir "SHMRY-MAIN.html"
$Success4 = Create-Shortcut -TargetFile $LauncherFile -ShortcutName "SHMRY Main Launcher.lnk" -Description "SHMRY Main Dashboard Launcher"

Write-Host ""

# Summary
if ($Success1 -and $Success2 -and $Success3 -and $Success4) {
    Write-Host "🎉 All shortcuts created successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some shortcuts may not have been created. Check the errors above." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 Your new desktop shortcuts:" -ForegroundColor Cyan
Write-Host "   🎛️ SHMRY Master Dashboard" -ForegroundColor White
Write-Host "   💾 SHMRY Storage Dashboard" -ForegroundColor White
Write-Host "   🔍 SHMRY Search Engine" -ForegroundColor White
Write-Host "   🚀 SHMRY Main Launcher" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Double-click any shortcut to test!" -ForegroundColor Green
Write-Host ""

# Show file paths for verification
Write-Host "📁 File paths for verification:" -ForegroundColor Yellow
Write-Host "Master Dashboard: $MasterFile" -ForegroundColor White
Write-Host "Storage Dashboard: $StorageFile" -ForegroundColor White
Write-Host "Search Engine: $SearchFile" -ForegroundColor White
Write-Host "Main Launcher: $LauncherFile" -ForegroundColor White

Write-Host ""
Read-Host "Press Enter to exit"
