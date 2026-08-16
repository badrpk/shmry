# SHMRY Main Dashboard Opener
Write-Host "🚀 SHMRY Main Dashboard Opener" -ForegroundColor Green
Write-Host ""

# Get current directory
$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Current Directory: $CurrentDir" -ForegroundColor Yellow
Write-Host ""

Write-Host "📍 Opening SHMRY Main Dashboard..." -ForegroundColor Cyan
Write-Host ""

$filePath = Join-Path $CurrentDir "SHMRY-MAIN.html"

if (Test-Path $filePath) {
    Write-Host "✅ File found: $filePath" -ForegroundColor Green
    Write-Host "🌐 Opening in default browser..." -ForegroundColor Yellow
    
    # Use Start-Process to open the file
    Start-Process $filePath
    
    Write-Host "✅ Main Dashboard opened successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 Available Options:" -ForegroundColor Cyan
    Write-Host "   🎛️ Master Admin Dashboard" -ForegroundColor White
    Write-Host "   💾 Smart Storage Dashboard" -ForegroundColor White
    Write-Host "   🔍 AI Search Engine" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Click any dashboard button to get started!" -ForegroundColor Green
} else {
    Write-Host "❌ File not found: $filePath" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Alternative solutions:" -ForegroundColor Yellow
    Write-Host "1. Double-click SHMRY-MAIN.html directly" -ForegroundColor White
    Write-Host "2. Right-click → Open with → Choose your browser" -ForegroundColor White
    Write-Host "3. Drag SHMRY-MAIN.html into your browser window" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"
