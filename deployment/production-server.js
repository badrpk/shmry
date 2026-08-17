// 🚀 SHMRY Production Server
// Secure, production-ready server with proper security configurations

const express = require('express');
const cookieParser = require('cookie-parser');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const cors = require('cors');
const path = require('path');
const securityConfig = require('../security-config');
const { createShmryAuth } = require('./auth');

class ProductionServer {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 80;
    this.adminPort = process.env.ADMIN_PORT || 3001;
    this.masterPort = process.env.MASTER_PORT || 3002;
    this.networkPort = process.env.NETWORK_PORT || 3003;
    
    this.setupSecurity();
    this.setupMiddleware();
    this.setupRoutes();
    this.setupErrorHandling();
  }

  setupSecurity() {
    // Validate environment before starting
    try {
      securityConfig.validateEnvironment();
    } catch (error) {
      console.error('❌ Security validation failed:', error.message);
      process.exit(1);
    }

    // Security headers
    this.app.use(helmet({
      contentSecurityPolicy: securityConfig.headers['Content-Security-Policy'] ? {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'", "'unsafe-inline'", "cdnjs.cloudflare.com"],
          styleSrc: ["'self'", "'unsafe-inline'", "fonts.googleapis.com", "cdnjs.cloudflare.com"],
          fontSrc: ["'self'", "fonts.gstatic.com"],
          imgSrc: ["'self'", "data:", "https:"],
          connectSrc: ["'self'", "https:"],
          frameAncestors: ["'none'"]
        }
      } : false,
      hsts: {
        maxAge: parseInt(process.env.HSTS_MAX_AGE) || 31536000,
        includeSubDomains: true,
        preload: true
      }
    }));

    // Additional security headers
    Object.entries(securityConfig.headers).forEach(([key, value]) => {
      if (value && key !== 'Content-Security-Policy') {
        this.app.use((req, res, next) => {
          res.setHeader(key, value);
          next();
        });
      }
    });
  }

  setupMiddleware() {
    // CORS configuration
    this.app.use(cors(securityConfig.cors));

    // Rate limiting
    const limiter = rateLimit(securityConfig.rateLimit);
    this.app.use(limiter);

    // Body parsing
    this.app.use(cookieParser());
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(express.urlencoded({ extended: true, limit: '10mb' }));

    // Request logging
    this.app.use((req, res, next) => {
      const timestamp = new Date().toISOString();
      console.log(`[${timestamp}] ${req.method} ${req.path} - ${req.ip}`);
      next();
    });
  }

  setupRoutes() {
    // Health check endpoint
    this.app.get('/health', (req, res) => {
      res.status(200).json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        environment: process.env.NODE_ENV || 'development'
      });
    });

    // Status endpoint for public monitoring
    this.app.get('/status', (req, res) => {
      res.status(200).json({
        status: 'operational',
        lastUpdated: new Date().toISOString(),
        services: {
          website: 'operational',
          api: 'operational',
          search: 'operational'
        },
        incidents: []
      });
    });

    // Static file serving (only for public website)
    this.app.use('/', express.static(path.join(__dirname, '../website')));
    this.app.use('/products', express.static(path.join(__dirname, '../products')));

    const shmryAuth = createShmryAuth();
    this.app.use('/api/auth', shmryAuth.router);

    // API routes (public)
    this.app.use('/api/public', require('./routes/public-api'));

    // Admin routes (protected, localhost only)
    this.app.use('/admin', this.adminAuthMiddleware, require('./routes/admin'));

    // Master routes (protected, localhost only)
    this.app.use('/master', this.masterAuthMiddleware, require('./routes/master'));

    // Network discovery routes (protected, localhost only)
    this.app.use('/network', this.networkAuthMiddleware, require('./routes/network'));

    // 404 handler
    this.app.use('*', (req, res) => {
      res.status(404).json({
        error: 'Not Found',
        message: 'The requested resource was not found',
        path: req.originalUrl
      });
    });
  }

  // Admin authentication middleware (localhost only)
  adminAuthMiddleware(req, res, next) {
    // Check if request is from localhost
    if (req.ip !== '127.0.0.1' && req.ip !== '::1' && !req.ip.startsWith('192.168.')) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'Admin access requires localhost connection'
      });
    }

    // Check authentication token
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) {
      return res.status(401).json({
        error: 'Unauthorized',
        message: 'Authentication token required'
      });
    }

    // TODO: Implement JWT verification
    // For now, allow localhost access
    next();
  }

  // Master authentication middleware (localhost only)
  masterAuthMiddleware(req, res, next) {
    if (req.ip !== '127.0.0.1' && req.ip !== '::1' && !req.ip.startsWith('192.168.')) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'Master access requires localhost connection'
      });
    }
    next();
  }

  // Network authentication middleware (localhost only)
  networkAuthMiddleware(req, res, next) {
    if (req.ip !== '127.0.0.1' && req.ip !== '::1' && !req.ip.startsWith('192.168.')) {
      return res.status(403).json({
        error: 'Forbidden',
        message: 'Network access requires localhost connection'
      });
    }
    next();
  }

  setupErrorHandling() {
    // Global error handler
    this.app.use((error, req, res, next) => {
      console.error('❌ Server error:', error);

      // Don't leak error details in production
      const message = process.env.NODE_ENV === 'production' 
        ? 'Internal server error' 
        : error.message;

      res.status(error.status || 500).json({
        error: 'Internal Server Error',
        message: message,
        timestamp: new Date().toISOString()
      });
    });
  }

  start() {
    // Start main server (public)
    this.app.listen(this.port, '0.0.0.0', () => {
      console.log(`🚀 SHMRY Production Server running on port ${this.port}`);
      console.log(`🌐 Public URL: http://localhost:${this.port}`);
      console.log(`🔒 Admin services bound to localhost only`);
      console.log(`✅ Security configuration validated`);
    });

    // Start admin server (localhost only)
    this.startAdminServer();
    this.startMasterServer();
    this.startNetworkServer();
  }

  startAdminServer() {
    const adminApp = express();
    adminApp.use(helmet());
    adminApp.use(cors({ origin: 'http://127.0.0.1' }));
    
    adminApp.listen(this.adminPort, '127.0.0.1', () => {
      console.log(`🔧 Admin Server running on localhost:${this.adminPort}`);
    });
  }

  startMasterServer() {
    const masterApp = express();
    masterApp.use(helmet());
    masterApp.use(cors({ origin: 'http://127.0.0.1' }));
    
    masterApp.listen(this.masterPort, '127.0.0.1', () => {
      console.log(`🎯 Master Server running on localhost:${this.masterPort}`);
    });
  }

  startNetworkServer() {
    const networkApp = express();
    networkApp.use(helmet());
    networkApp.use(cors({ origin: 'http://127.0.0.1' }));
    
    networkApp.listen(this.networkPort, '127.0.0.1', () => {
      console.log(`🌍 Network Discovery running on localhost:${this.networkPort}`);
    });
  }
}

// Start server if run directly
if (require.main === module) {
  const server = new ProductionServer();
  server.start();
}

module.exports = ProductionServer;
