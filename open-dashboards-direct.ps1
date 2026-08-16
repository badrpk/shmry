# SHMRY Direct Dashboard Opener
Write-Host "🚀 SHMRY Direct Dashboard Opener" -ForegroundColor Green
Write-Host ""

# Get current directory
$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Current Directory: $CurrentDir" -ForegroundColor Yellow
Write-Host ""

Write-Host "📍 Choose your dashboard:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 🎛️ Master Admin Dashboard" -ForegroundColor White
Write-Host "2. 💾 Smart Storage Dashboard" -ForegroundColor White
Write-Host "3. 🔍 Search Engine" -ForegroundColor White
Write-Host "4. 🎨 HTML Launcher Page" -ForegroundColor White
Write-Host "5. ❌ Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🎛️ Opening Master Admin Dashboard..." -ForegroundColor Green
        $filePath = Join-Path $CurrentDir "master-admin-dashboard.html"
        if (Test-Path $filePath) {
            # Use Start-Process with the file path directly
            Start-Process $filePath
            Write-Host "✅ Master Dashboard opened successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ File not found: $filePath" -ForegroundColor Red
        }
    }
    "2" {
        Write-Host ""
        Write-Host "💾 Opening Smart Storage Dashboard..." -ForegroundColor Green
        $filePath = Join-Path $CurrentDir "admin-dashboard.html"
        if (Test-Path $filePath) {
            Start-Process $filePath
            Write-Host "✅ Storage Dashboard opened successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ File not found: $filePath" -ForegroundColor Red
        }
    }
    "3" {
        Write-Host ""
        Write-Host "🔍 Opening Search Engine..." -ForegroundColor Green
        $filePath = Join-Path $CurrentDir "search\index.html"
        if (Test-Path $filePath) {
            Start-Process $filePath
            Write-Host "✅ Search Engine opened successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ File not found: $filePath" -ForegroundColor Red
        }
    }
    "4" {
        Write-Host ""
        Write-Host "🎨 Opening HTML Launcher Page..." -ForegroundColor Green
        $filePath = Join-Path $CurrentDir "open-dashboards.html"
        if (Test-Path $filePath) {
            Start-Process $filePath
            Write-Host "✅ HTML Launcher opened successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ File not found: $filePath" -ForegroundColor Red
        }
    }
    "5" {
        Write-Host ""
        Write-Host "👋 Goodbye!" -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host ""
        Write-Host "❌ Invalid choice. Please enter 1-5." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "💡 If dashboards still don't work properly:" -ForegroundColor Yellow
Write-Host "1. Try the local server: start-local-server.bat" -ForegroundColor White
Write-Host "2. Check your browser settings" -ForegroundColor White
Write-Host "3. Try a different browser" -ForegroundColor White
Write-Host ""
Write-Host "💡 You can now use your SHMRY systems" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
