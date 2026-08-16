const express = require('express');
const path = require('path');

const app = express();
const PORT = 3001;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the project root
app.use(express.static(path.join(__dirname, '..')));

// ==================== ADMIN ROUTES ====================

// Admin Dashboard
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../admin-dashboard.html'));
});

app.get('/admin-dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, '../admin-dashboard.html'));
});

app.get('/admin-dashboard.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../admin-dashboard.html'));
});

// Admin Device Manager
app.get('/admin-device-manager', (req, res) => {
    res.sendFile(path.join(__dirname, '../admin-device-manager.html'));
});

app.get('/admin-device-manager.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../admin-device-manager.html'));
});

// Server Status Dashboard
app.get('/server-status', (req, res) => {
    res.sendFile(path.join(__dirname, '../server-status-dashboard.html'));
});

app.get('/server-status-dashboard.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../server-status-dashboard.html'));
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).send(`
        <html>
            <head><title>404 - Admin Page Not Found</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>404 - Admin Page Not Found</h1>
                <p>The admin page you're looking for doesn't exist.</p>
                <p>Requested URL: ${req.originalUrl}</p>
                <a href="/" style="color: #1e3c72;">Go to Admin Dashboard</a>
            </body>
        </html>
    `);
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log('⚙️ SHMRY Admin Server is running!');
    console.log(`⚙️ Server URL: http://localhost:${PORT}`);
    console.log(`⚙️ External URL: http://154.57.212.38:${PORT}`);
    console.log('📱 Available admin pages:');
    console.log(`   • Admin Dashboard: http://localhost:${PORT}/`);
    console.log(`   • Admin Device Manager: http://localhost:${PORT}/admin-device-manager`);
    console.log(`   • Server Status: http://localhost:${PORT}/server-status`);
    console.log('');
    console.log('🚀 Ready for production deployment!');
    console.log('Press Ctrl+C to stop the server');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down SHMRY Admin Server...');
    process.exit(0);
});
