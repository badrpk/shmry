const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 80; // Use port 80 for production or environment variable

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Security headers
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    next();
});

// Serve static files from the project root
app.use(express.static(path.join(__dirname, '..')));

// ==================== WEBSITE ROUTES ====================

// Homepage
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../website/shmry-website.html'));
});

// Products Overview Page
app.get('/products', (req, res) => {
    res.sendFile(path.join(__dirname, '../products/index.html'));
});

// Custom Email Product Page
app.get('/products/custom-email', (req, res) => {
    res.sendFile(path.join(__dirname, '../products/custom-email/index.html'));
});

// Website Builder Product Page
app.get('/products/website-builder', (req, res) => {
    res.sendFile(path.join(__dirname, '../products/website-builder/index.html'));
});

// Mobile App Builder Product Page
app.get('/products/mobile-app-builder', (req, res) => {
    res.sendFile(path.join(__dirname, '../products/mobile-app-builder/index.html'));
});

// Edge Computing Product Page
app.get('/products/edge-computing', (req, res) => {
    res.sendFile(path.join(__dirname, '../products/edge-computing/index.html'));
});

// About Page
app.get('/about', (req, res) => {
    res.sendFile(path.join(__dirname, '../about/index.html'));
});

// Careers Page
app.get('/careers', (req, res) => {
    res.sendFile(path.join(__dirname, '../careers/index.html'));
});

// Search Page
app.get('/search', (req, res) => {
    res.sendFile(path.join(__dirname, '../search/index.html'));
});

// Search Test Page
app.get('/test-search', (req, res) => {
    res.sendFile(path.join(__dirname, '../test-search.html'));
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).send(`
        <html>
            <head><title>404 - Page Not Found</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>404 - Page Not Found</h1>
                <p>The page you're looking for doesn't exist.</p>
                <p>Requested URL: ${req.originalUrl}</p>
                <a href="/" style="color: #1e3c72;">Go to Homepage</a>
            </body>
        </html>
    `);
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log('🌐 SHMRY Website Server is running!');
    console.log(`🌐 Server URL: http://localhost:${PORT}`);
    console.log(`🌐 External URL: http://0.0.0.0:${PORT}`);
    console.log('📱 Available pages:');
    console.log(`   • Homepage: http://localhost:${PORT}/`);
    console.log(`   • Products: http://localhost:${PORT}/products`);
    console.log(`   • Custom Email: http://localhost:${PORT}/products/custom-email`);
    console.log(`   • Search: http://localhost:${PORT}/search`);
    console.log('');
    console.log('🚀 Ready for production deployment!');
    console.log('Press Ctrl+C to stop the server');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down SHMRY Website Server...');
    process.exit(0);
});
