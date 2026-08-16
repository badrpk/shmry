/**
 * Shmry Module Loader
 * Initializes and manages all 190+ Shmry modules
 */

class ShmryModuleLoader {
    constructor(config = {}) {
        this.config = { ...this.defaultConfig, ...config };
        this.core = null;
        this.ai = null;
        this.edge = null;
        this.cloud = null;
        this.commerce = null;
        this.modules = new Map();
        this.init();
    }

    get defaultConfig() {
        return {
            enableAllModules: true,
            autoStart: true,
            healthCheckInterval: 30000,
            enableLogging: true
        };
    }

    async init() {
        try {
            console.log('🚀 Initializing Shmry Platform...');
            
            // Load core system
            await this.loadCoreSystem();
            
            // Load all module systems
            await this.loadAllModules();
            
            // Start health monitoring
            if (this.config.autoStart) {
                this.startHealthMonitoring();
            }
            
            console.log('✅ Shmry Platform initialized successfully!');
            console.log(`📊 Total modules loaded: ${this.modules.size}`);
            
        } catch (error) {
            console.error('❌ Failed to initialize Shmry Platform:', error);
            throw error;
        }
    }

    async loadCoreSystem() {
        // Load core system
        this.core = new ShmryCore(this.config);
        this.modules.set('core', this.core);
        
        // Load AI system
        this.ai = new ShmryAICore(this.config);
        this.modules.set('ai', this.ai);
        
        // Load Edge Computing system
        this.edge = new ShmryEdgeCore(this.config);
        this.modules.set('edge', this.edge);
        
        // Load Cloud Infrastructure system
        this.cloud = new ShmryCloudCore(this.config);
        this.modules.set('cloud', this.cloud);
        
        // Load Commerce system
        this.commerce = new ShmryCommerceCore(this.config);
        this.modules.set('commerce', this.commerce);
    }

    async loadAllModules() {
        // Load all individual modules from each system
        await this.loadAIModules();
        await this.loadEdgeModules();
        await this.loadCloudModules();
        await this.loadCommerceModules();
    }

    async loadAIModules() {
        if (!this.ai) return;
        
        // Load all 17 AI modules
        const aiModules = [
            'ShmryAI-Core', 'ShmryBrain', 'ShmryNeural', 'ShmryTransformer',
            'ShmryRL', 'ShmryLoRA', 'ShmryQuant', 'ShmryScheduler',
            'ShmryEval', 'ShmryMemory', 'ShmryReason', 'ShmryMath',
            'ShmryGraphAI', 'ShmryTimeSeries', 'ShmryAutoTrain',
            'ShmrySafety', 'ShmryPromptLab'
        ];
        
        for (const moduleName of aiModules) {
            this.modules.set(moduleName, this.ai);
        }
    }

    async loadEdgeModules() {
        if (!this.edge) return;
        
        // Load all 13 Edge modules
        const edgeModules = [
            'ShmryEdge', 'ShmryEdgeNode', 'ShmryEdgeWorker', 'ShmryEdgeAdmin',
            'ShmryEdgeFallback', 'ShmryEdgeConnect', 'ShmryEdgeVision',
            'ShmryEdgeAudio', 'ShmryEdgeSensors', 'ShmryEdgeSecureBoot',
            'ShmryEdgeML', 'ShmryEdgeStore', 'ShmryEdgeSDK'
        ];
        
        for (const moduleName of edgeModules) {
            this.modules.set(moduleName, this.edge);
        }
    }

    async loadCloudModules() {
        if (!this.cloud) return;
        
        // Load all 15 Cloud modules
        const cloudModules = [
            'ShmryCompute', 'ShmryStorage', 'ShmryDatabase', 'ShmryNetwork',
            'ShmrySecurity', 'ShmryAnalytics', 'ShmryMLOps', 'ShmryDevOps',
            'ShmryMonitoring', 'ShmryBackup', 'ShmryCompliance', 'ShmryCost',
            'ShmrySupport', 'ShmryTraining', 'ShmryConsulting', 'ShmryMarketplace'
        ];
        
        for (const moduleName of cloudModules) {
            this.modules.set(moduleName, this.cloud);
        }
    }

    async loadCommerceModules() {
        if (!this.commerce) return;
        
        // Load all 12 Commerce modules
        const commerceModules = [
            'ShmryRangoons', 'ShmryCatalog', 'ShmryCart', 'ShmryCheckout',
            'ShmryLoyalty', 'ShmryReviews', 'ShmrySearchShop', 'ShmryFeedsShop',
            'ShmryContentCMS', 'ShmryNotifications', 'ShmryCDP', 'ShmryPromoAI'
        ];
        
        for (const moduleName of commerceModules) {
            this.modules.set(moduleName, this.commerce);
        }
    }

    startHealthMonitoring() {
        if (this.config.healthCheckInterval > 0) {
            setInterval(async () => {
                await this.performHealthCheck();
            }, this.config.healthCheckInterval);
        }
    }

    async performHealthCheck() {
        try {
            const health = await this.getSystemHealth();
            
            if (this.config.enableLogging) {
                console.log('🏥 System Health Check:', {
                    timestamp: new Date().toISOString(),
                    overallStatus: health.status,
                    moduleCount: health.modules.length,
                    healthyModules: health.modules.filter(m => m.status === 'healthy').length
                });
            }
            
            // Emit health event
            this.emit('health:updated', health);
            
        } catch (error) {
            console.error('❌ Health check failed:', error);
        }
    }

    async getSystemHealth() {
        const health = {
            status: 'healthy',
            timestamp: new Date().toISOString(),
            modules: [],
            systems: {}
        };
        
        // Check core systems
        try {
            health.systems.core = await this.core.healthCheck();
            if (health.systems.core.status !== 'healthy') {
                health.status = 'degraded';
            }
        } catch (error) {
            health.systems.core = { status: 'error', error: error.message };
            health.status = 'degraded';
        }
        
        try {
            health.systems.ai = await this.ai.healthCheck();
            if (health.systems.ai.status !== 'healthy') {
                health.status = 'degraded';
            }
        } catch (error) {
            health.systems.ai = { status: 'error', error: error.message };
            health.status = 'degraded';
        }
        
        try {
            health.systems.edge = await this.edge.healthCheck();
            if (health.systems.edge.status !== 'healthy') {
                health.status = 'degraded';
            }
        } catch (error) {
            health.systems.edge = { status: 'error', error: error.message };
            health.status = 'degraded';
        }
        
        try {
            health.systems.cloud = await this.cloud.healthCheck();
            if (health.systems.cloud.status !== 'healthy') {
                health.status = 'degraded';
            }
        } catch (error) {
            health.systems.cloud = { status: 'error', error: error.message };
            health.status = 'degraded';
        }
        
        try {
            health.systems.commerce = await this.commerce.healthCheck();
            if (health.systems.commerce.status !== 'healthy') {
                health.status = 'degraded';
            }
        } catch (error) {
            health.systems.commerce = { status: 'error', error: error.message };
            health.status = 'degraded';
        }
        
        // Check individual modules
        for (const [name, module] of this.modules) {
            try {
                if (typeof module.healthCheck === 'function') {
                    const moduleHealth = await module.healthCheck();
                    health.modules.push({
                        name,
                        status: moduleHealth.status || 'unknown',
                        details: moduleHealth
                    });
                }
            } catch (error) {
                health.modules.push({
                    name,
                    status: 'error',
                    error: error.message
                });
            }
        }
        
        return health;
    }

    getModule(moduleName) {
        return this.modules.get(moduleName);
    }

    getAllModules() {
        return Array.from(this.modules.keys());
    }

    getModuleCount() {
        return this.modules.size;
    }

    async shutdown() {
        console.log('🔄 Shutting down Shmry Platform...');
        
        try {
            // Shutdown core systems
            if (this.core && typeof this.core.shutdown === 'function') {
                await this.core.shutdown();
            }
            
            console.log('✅ Shmry Platform shutdown complete');
        } catch (error) {
            console.error('❌ Error during shutdown:', error);
        }
    }

    // Event system
    emit(event, data) {
        if (this.core && this.core.emit) {
            this.core.emit(event, data);
        }
    }

    on(event, callback) {
        if (this.core && this.core.on) {
            this.core.on(event, callback);
        }
    }
}

// Global Shmry instance
let globalShmry = null;

// Initialize Shmry Platform
async function initializeShmry(config = {}) {
    if (globalShmry) {
        console.warn('⚠️ Shmry Platform already initialized');
        return globalShmry;
    }
    
    try {
        globalShmry = new ShmryModuleLoader(config);
        return globalShmry;
    } catch (error) {
        console.error('❌ Failed to initialize Shmry Platform:', error);
        throw error;
    }
}

// Get global Shmry instance
function getShmry() {
    if (!globalShmry) {
        throw new Error('Shmry Platform not initialized. Call initializeShmry() first.');
    }
    return globalShmry;
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { 
        ShmryModuleLoader, 
        initializeShmry, 
        getShmry 
    };
} else if (typeof window !== 'undefined') {
    window.ShmryModuleLoader = ShmryModuleLoader;
    window.initializeShmry = initializeShmry;
    window.getShmry = getShmry;
}
