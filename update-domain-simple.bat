@echo off
echo.
echo ========================================
echo 🚀 SHMRY Domain Update to Node.js Server
echo ========================================
echo.
echo This script will help you point www.shmry.com
echo to your Node.js server at 154.57.212.38
echo.

echo 📡 Checking current Vercel configuration...
vercel project ls

echo.
echo 🔄 Removing domain from Vercel...
vercel domains remove www.shmry.com --yes

echo.
echo ✅ Domain removed from Vercel successfully!
echo.
echo 🎯 Next Steps:
echo ===============
echo 1. Go to your domain registrar (where you bought www.shmry.com)
echo 2. Update DNS settings:
echo    • Type: A Record
echo    • Name: www
echo    • Value: 154.57.212.38
echo    • TTL: 300 (or default)
echo.
echo 3. Wait for DNS propagation (5-30 minutes)
echo.
echo 4. Test your domain:
echo    • Main Website: http://www.shmry.com (port 80)
echo    • Admin Dashboard: http://www.shmry.com:3001
echo    • Master Dashboard: http://www.shmry.com:3002
echo    • Network Discovery: http://www.shmry.com:3003
echo.
echo ✅ Your Node.js server will then be accessible via www.shmry.com!
echo.
pause
