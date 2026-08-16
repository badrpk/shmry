const express = require('express');
const path = require('path');

const app = express();
const PORT = 3002;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the project root
app.use(express.static(path.join(__dirname, '..')));

// ==================== MASTER ROUTES ====================

// Master Dashboard
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../master-dashboard.html'));
});

app.get('/master-dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, '../master-dashboard.html'));
});

app.get('/master-dashboard.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../master-dashboard.html'));
});

// Master Admin Dashboard
app.get('/master-admin', (req, res) => {
    res.sendFile(path.join(__dirname, '../master-admin-dashboard.html'));
});

app.get('/master-admin-dashboard.html', (req, res) => {
    res.sendFile(path.join(__dirname, '../master-admin-dashboard.html'));
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).send(`
        <html>
            <head><title>404 - Master Page Not Found</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>404 - Master Page Not Found</h1>
                <p>The master page you're looking for doesn't exist.</p>
                <p>Requested URL: ${req.originalUrl}</p>
                <a href="/" style="color: #1e3c72;">Go to Master Dashboard</a>
            </body>
        </html>
    `);
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log('🏠 SHMRY Master Server is running!');
    console.log(`🏠 Server URL: http://localhost:${PORT}`);
    console.log(`🏠 External URL: http://154.57.212.38:${PORT}`);
    console.log('📱 Available master pages:');
    console.log(`   • Master Dashboard: http://localhost:${PORT}/`);
    console.log(`   • Master Admin Dashboard: http://localhost:${PORT}/master-admin`);
    console.log('');
    console.log('🚀 Ready for production deployment!');
    console.log('Press Ctrl+C to stop the server');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down SHMRY Master Server...');
    process.exit(0);
});
