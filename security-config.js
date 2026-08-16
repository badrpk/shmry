// 🔐 SHMRY Security Configuration
// Production-ready security settings for all services

const securityConfig = {
  // =============================================================================
  // AUTHENTICATION & SESSION SECURITY
  // =============================================================================
  auth: {
    // Session configuration
    sessionSecret: process.env.ADMIN_SESSION_SECRET || 'CHANGE_THIS_IN_PRODUCTION',
    sessionDuration: 24 * 60 * 60 * 1000, // 24 hours in milliseconds
    maxLoginAttempts: 5,
    lockoutDuration: 15 * 60 * 1000, // 15 minutes
    
    // OTP configuration
    otpExpiry: 10 * 60 * 1000, // 10 minutes
    otpLength: 6,
    otpRateLimit: {
      maxAttempts: 3,
      windowMs: 10 * 60 * 1000, // 10 minutes
      maxSends: 3,
      sendWindowMs: 10 * 60 * 1000 // 10 minutes
    }
  },

  // =============================================================================
  // RATE LIMITING
  // =============================================================================
  rateLimit: {
    windowMs: 15 * 60 * 1000, // 15 minutes
    maxRequests: 100, // requests per windowMs
    message: 'Too many requests from this IP, please try again later.',
    standardHeaders: true,
    legacyHeaders: false,
    
    // Specific endpoint limits
    endpoints: {
      '/api/auth/login': { maxRequests: 5, windowMs: 15 * 60 * 1000 },
      '/api/auth/otp': { maxRequests: 3, windowMs: 10 * 60 * 1000 },
      '/api/admin/*': { maxRequests: 50, windowMs: 15 * 60 * 1000 },
      '/api/master/*': { maxRequests: 50, windowMs: 15 * 60 * 1000 }
    }
  },

  // =============================================================================
  // CORS & SECURITY HEADERS
  // =============================================================================
  cors: {
    origin: process.env.CORS_ORIGIN || 'https://www.shmry.com',
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
    exposedHeaders: ['X-Total-Count', 'X-Page-Count'],
    maxAge: 86400 // 24 hours
  },

  headers: {
    // Security headers
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
    
    // HSTS (HTTPS Strict Transport Security)
    'Strict-Transport-Security': `max-age=${process.env.HSTS_MAX_AGE || 31536000}; includeSubDomains; preload`,
    
    // Content Security Policy
    'Content-Security-Policy': process.env.CSP_ENABLED === 'true' ? 
      "default-src 'self'; script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com cdnjs.cloudflare.com; font-src 'self' fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https:; frame-ancestors 'none';" : 
      undefined
  },

  // =============================================================================
  // ENCRYPTION & HASHING
  // =============================================================================
  crypto: {
    algorithm: 'aes-256-gcm',
    keyLength: 32,
    ivLength: 16,
    saltRounds: 12, // for bcrypt
    jwtAlgorithm: 'HS256',
    jwtExpiry: '24h'
  },

  // =============================================================================
  // BACKUP & RECOVERY SECURITY
  // =============================================================================
  backup: {
    encryption: process.env.BACKUP_ENCRYPTION_ENABLED === 'true',
    retentionDays: parseInt(process.env.BACKUP_RETENTION_DAYS) || 30,
    integrityCheck: true,
    checksumAlgorithm: 'sha256',
    compression: true
  },

  // =============================================================================
  // AI MODEL SECURITY
  // =============================================================================
  aiModels: {
    downloadEnabled: process.env.AI_MODEL_DOWNLOAD_ENABLED === 'true',
    storageQuotaGB: parseInt(process.env.AI_MODEL_STORAGE_QUOTA_GB) || 100,
    workerNodeUrl: process.env.AI_MODEL_WORKER_NODE_URL || 'https://worker.shmry.com',
    licenseValidation: true,
    checksumVerification: true,
    sizeLimits: {
      small: 1 * 1024 * 1024 * 1024,    // 1GB
      medium: 10 * 1024 * 1024 * 1024,  // 10GB
      large: 100 * 1024 * 1024 * 1024   // 100GB
    }
  },

  // =============================================================================
  // MONITORING & AUDIT
  // =============================================================================
  monitoring: {
    enabled: process.env.MONITORING_ENABLED === 'true',
    logLevel: process.env.LOG_LEVEL || 'info',
    auditLogging: process.env.AUDIT_LOGGING_ENABLED === 'true',
    performanceMetrics: true,
    securityEvents: true,
    alertThresholds: {
      cpu: 80,      // 80% CPU usage
      memory: 85,   // 85% memory usage
      disk: 90,     // 90% disk usage
      responseTime: 2000 // 2 seconds
    }
  },

  // =============================================================================
  // NETWORK SECURITY
  // =============================================================================
  network: {
    // Bind to localhost for admin services
    bindAddress: '127.0.0.1',
    publicPort: 443, // Only expose HTTPS
    adminPorts: [3001, 3002, 3003], // Internal only
    allowedIPs: [], // Empty for localhost only
    vpnRequired: true, // Admin access requires VPN
    zeroTrust: true   // Use Zero-Trust access control
  },

  // =============================================================================
  // ENVIRONMENT VALIDATION
  // =============================================================================
  validateEnvironment() {
    const required = [
      'ADMIN_SESSION_SECRET',
      'JWT_SECRET',
      'ENCRYPTION_KEY'
    ];
    
    const missing = required.filter(key => !process.env[key]);
    
    if (missing.length > 0) {
      throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    }
    
    if (process.env.NODE_ENV === 'production') {
      if (process.env.ADMIN_SESSION_SECRET === 'CHANGE_THIS_IN_PRODUCTION') {
        throw new Error('ADMIN_SESSION_SECRET must be changed in production');
      }
    }
    
    return true;
  }
};

// Export configuration
module.exports = securityConfig;

// Validate on load
if (require.main === module) {
  try {
    securityConfig.validateEnvironment();
    console.log('✅ Security configuration validated successfully');
  } catch (error) {
    console.error('❌ Security configuration validation failed:', error.message);
    process.exit(1);
  }
}
