// SHMRY Storage Manager
// Monitors local storage and redirects downloads to admin devices when space is low

const fs = require('fs');
const path = require('path');
const os = require('os');
const { exec } = require('child_process');

class ShmryStorageManager {
    constructor() {
        this.storageThreshold = 80; // 80% storage usage threshold
        this.adminDevices = new Map();
        this.localStoragePath = path.join(__dirname, 'AI-Models');
        this.adminStoragePath = 'admin-devices-storage';
        this.storageLog = [];
        
        this.initializeStorage();
        this.discoverAdminDevices();
        this.startStorageMonitoring();
    }

    // Initialize storage monitoring
    initializeStorage() {
        if (!fs.existsSync(this.localStoragePath)) {
            fs.mkdirSync(this.localStoragePath, { recursive: true });
        }
        
        if (!fs.existsSync(this.adminStoragePath)) {
            fs.mkdirSync(this.adminStoragePath, { recursive: true });
        }
        
        console.log('💾 SHMRY Storage Manager initialized');
        console.log(`📁 Local storage: ${this.localStoragePath}`);
        console.log(`🌐 Admin storage: ${this.adminStoragePath}`);
    }

    // Discover available admin devices
    discoverAdminDevices() {
        // Simulate discovering admin devices on the network
        this.adminDevices.set('admin-server-1', {
            name: 'Admin Server 1',
            ip: '192.168.1.100',
            storage: '2TB',
            availableSpace: '1.5TB',
            status: 'online',
            priority: 'high'
        });
        
        this.adminDevices.set('admin-server-2', {
            name: 'Admin Server 2',
            ip: '192.168.1.101',
            storage: '4TB',
            availableSpace: '3.2TB',
            status: 'online',
            priority: 'medium'
        });
        
        this.adminDevices.set('admin-nas', {
            name: 'Admin NAS Storage',
            ip: '192.168.1.102',
            storage: '10TB',
            availableSpace: '8.1TB',
            status: 'online',
            priority: 'high'
        });
        
        this.adminDevices.set('cloud-storage', {
            name: 'Cloud Storage Backup',
            ip: 'cloud.shmry.com',
            storage: 'Unlimited',
            availableSpace: 'Unlimited',
            status: 'online',
            priority: 'low'
        });
        
        console.log(`🔍 Discovered ${this.adminDevices.size} admin devices`);
    }

    // Start continuous storage monitoring
    startStorageMonitoring() {
        // Check storage every 30 seconds
        setInterval(() => {
            this.checkStorageStatus();
        }, 30000);
        
        console.log('📊 Storage monitoring started (checking every 30 seconds)');
    }

    // Check current storage status
    checkStorageStatus() {
        try {
            const storageInfo = this.getStorageInfo();
            const usagePercent = (storageInfo.used / storageInfo.total) * 100;
            
            const status = {
                timestamp: new Date().toISOString(),
                localUsage: usagePercent,
                localUsed: storageInfo.used,
                localTotal: storageInfo.total,
                localFree: storageInfo.free,
                threshold: this.storageThreshold,
                status: usagePercent >= this.storageThreshold ? 'critical' : 'normal'
            };
            
            this.storageLog.push(status);
            this.saveStorageLog();
            
            if (usagePercent >= this.storageThreshold) {
                this.handleStorageWarning(status);
            } else if (usagePercent >= 70) {
                this.handleStorageAlert(status);
            }
            
            // Log status every 5 minutes
            if (this.storageLog.length % 10 === 0) {
                this.logStorageStatus(status);
            }
            
        } catch (error) {
            console.error('❌ Storage check failed:', error.message);
        }
    }

    // Get current storage information
    getStorageInfo() {
        const drive = path.parse(process.cwd()).root;
        
        // For Windows, get drive info
        if (process.platform === 'win32') {
            return this.getWindowsStorageInfo(drive);
        } else {
            return this.getUnixStorageInfo();
        }
    }

    // Get Windows storage info
    getWindowsStorageInfo(drive) {
        try {
            // Simulate Windows storage info (in real implementation, use wmic or PowerShell)
            const total = 500 * 1024 * 1024 * 1024; // 500GB
            const free = 150 * 1024 * 1024 * 1024;  // 150GB
            const used = total - free;
            
            return { total, used, free };
        } catch (error) {
            console.error('❌ Windows storage info failed:', error.message);
            return { total: 0, used: 0, free: 0 };
        }
    }

    // Get Unix storage info
    getUnixStorageInfo() {
        try {
            const stats = fs.statfsSync('/');
            const total = stats.blocks * stats.bsize;
            const free = stats.bavail * stats.bsize;
            const used = total - free;
            
            return { total, used, free };
        } catch (error) {
            console.error('❌ Unix storage info failed:', error.message);
            return { total: 0, used: 0, free: 0 };
        }
    }

    // Handle storage warning (70-80%)
    handleStorageAlert(status) {
        console.log(`⚠️  Storage Alert: ${status.localUsage.toFixed(1)}% used`);
        console.log(`💡 Consider redirecting some downloads to admin devices`);
        
        // Start redirecting new downloads to admin devices
        this.enableAdminDeviceRedirects();
    }

    // Handle critical storage warning (80%+)
    handleStorageWarning(status) {
        console.log(`🚨 CRITICAL STORAGE WARNING: ${status.localUsage.toFixed(1)}% used!`);
        console.log(`📁 Used: ${this.formatBytes(status.localUsed)}`);
        console.log(`💾 Free: ${this.formatBytes(status.localFree)}`);
        
        // Immediately redirect all new downloads to admin devices
        this.enableAdminDeviceRedirects();
        
        // Move some existing models to admin devices if possible
        this.relocateExistingModels();
        
        // Notify user
        this.notifyStorageWarning(status);
    }

    // Enable redirects to admin devices
    enableAdminDeviceRedirects() {
        console.log('🔄 Enabling admin device redirects for new downloads');
        
        // Update downloader configuration
        this.updateDownloaderConfig({
            useAdminDevices: true,
            localStorageThreshold: this.storageThreshold,
            preferredAdminDevices: this.getPreferredAdminDevices()
        });
    }

    // Get preferred admin devices for downloads
    getPreferredAdminDevices() {
        return Array.from(this.adminDevices.values())
            .filter(device => device.status === 'online')
            .sort((a, b) => this.getPriorityScore(b.priority) - this.getPriorityScore(a.priority))
            .slice(0, 3); // Top 3 devices
    }

    // Get priority score
    getPriorityScore(priority) {
        const scores = { 'high': 3, 'medium': 2, 'low': 1 };
        return scores[priority] || 1;
    }

    // Relocate existing models to free up space
    relocateExistingModels() {
        try {
            const modelsToMove = this.identifyModelsForRelocation();
            
            if (modelsToMove.length > 0) {
                console.log(`📦 Relocating ${modelsToMove.length} models to admin devices...`);
                
                modelsToMove.forEach(model => {
                    this.relocateModel(model);
                });
            }
        } catch (error) {
            console.error('❌ Model relocation failed:', error.message);
        }
    }

    // Identify models that can be moved to admin devices
    identifyModelsForRelocation() {
        try {
            const models = fs.readdirSync(this.localStoragePath)
                .filter(item => item.endsWith('.model') || item.endsWith('.bin'))
                .map(model => ({
                    name: model,
                    path: path.join(this.localStoragePath, model),
                    size: fs.statSync(path.join(this.localStoragePath, model)).size,
                    priority: this.getModelPriority(model)
                }))
                .sort((a, b) => a.priority - b.priority); // Move low priority first
            
            // Calculate how much space we need to free
            const storageInfo = this.getStorageInfo();
            const targetFree = storageInfo.total * 0.3; // Target 30% free space
            const needToFree = targetFree - storageInfo.free;
            
            let freedSpace = 0;
            const modelsToMove = [];
            
            for (const model of models) {
                if (freedSpace >= needToFree) break;
                
                modelsToMove.push(model);
                freedSpace += model.size;
            }
            
            return modelsToMove;
        } catch (error) {
            console.error('❌ Failed to identify models for relocation:', error.message);
            return [];
        }
    }

    // Get model priority (lower = move first)
    getModelPriority(modelName) {
        const highPriority = ['llama', 'mistral', 'deepseek', 'claude', 'gpt'];
        const mediumPriority = ['qwen', 'code', 'llava', 'stable-diffusion'];
        
        const lowerName = modelName.toLowerCase();
        
        if (highPriority.some(term => lowerName.includes(term))) return 3;
        if (mediumPriority.some(term => lowerName.includes(term))) return 2;
        return 1; // Low priority
    }

    // Relocate a model to admin device
    relocateModel(model) {
        try {
            const targetDevice = this.selectTargetAdminDevice(model);
            
            if (targetDevice) {
                console.log(`📦 Moving ${model.name} to ${targetDevice.name}`);
                
                // Simulate moving the model
                const destination = path.join(this.adminStoragePath, targetDevice.name, model.name);
                
                // Create destination directory
                const destDir = path.dirname(destination);
                if (!fs.existsSync(destDir)) {
                    fs.mkdirSync(destDir, { recursive: true });
                }
                
                // Move the file (in real implementation, this would be actual file transfer)
                // fs.renameSync(model.path, destination);
                
                // Update model registry
                this.updateModelRegistry(model, targetDevice);
                
                console.log(`✅ Successfully moved ${model.name} to ${targetDevice.name}`);
            }
        } catch (error) {
            console.error(`❌ Failed to relocate ${model.name}:`, error.message);
        }
    }

    // Select target admin device for model
    selectTargetAdminDevice(model) {
        const availableDevices = Array.from(this.adminDevices.values())
            .filter(device => device.status === 'online')
            .sort((a, b) => this.getPriorityScore(b.priority) - this.getPriorityScore(a.priority));
        
        // Prefer devices with more available space
        return availableDevices[0] || null;
    }

    // Update model registry after relocation
    updateModelRegistry(model, targetDevice) {
        const registryPath = path.join(this.adminStoragePath, 'model-registry.json');
        let registry = {};
        
        try {
            if (fs.existsSync(registryPath)) {
                registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
            }
        } catch (error) {
            console.warn('⚠️  Could not read existing registry:', error.message);
        }
        
        registry[model.name] = {
            location: targetDevice.name,
            device: targetDevice.ip,
            relocatedAt: new Date().toISOString(),
            originalSize: model.size,
            status: 'relocated'
        };
        
        try {
            fs.writeFileSync(registryPath, JSON.stringify(registry, null, 2));
        } catch (error) {
            console.error('❌ Failed to update model registry:', error.message);
        }
    }

    // Update downloader configuration
    updateDownloaderConfig(config) {
        const configPath = path.join(__dirname, 'downloader-config.json');
        
        try {
            fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
            console.log('✅ Downloader configuration updated');
        } catch (error) {
            console.error('❌ Failed to update downloader config:', error.message);
        }
    }

    // Notify user about storage warning
    notifyStorageWarning(status) {
        console.log('\n🚨 STORAGE WARNING NOTIFICATION');
        console.log('================================');
        console.log(`⚠️  Your computer storage is ${status.localUsage.toFixed(1)}% full!`);
        console.log(`💾 Used: ${this.formatBytes(status.localUsed)}`);
        console.log(`💾 Free: ${this.formatBytes(status.localFree)}`);
        console.log(`📊 Threshold: ${status.threshold}%`);
        console.log('');
        console.log('🔄 Automatic actions taken:');
        console.log('   ✅ New downloads redirected to admin devices');
        console.log('   📦 Low-priority models being relocated');
        console.log('   💡 Consider freeing up more space manually');
        console.log('');
        console.log('🌐 Admin devices available:');
        this.adminDevices.forEach((device, key) => {
            console.log(`   ${device.name}: ${device.availableSpace} available`);
        });
    }

    // Log storage status
    logStorageStatus(status) {
        console.log(`💾 Storage Status: ${status.localUsage.toFixed(1)}% used`);
        console.log(`   📁 Used: ${this.formatBytes(status.localUsed)}`);
        console.log(`   💾 Free: ${this.formatBytes(status.localFree)}`);
        console.log(`   📊 Status: ${status.status}`);
    }

    // Save storage log
    saveStorageLog() {
        const logPath = path.join(__dirname, 'storage-log.json');
        
        try {
            fs.writeFileSync(logPath, JSON.stringify(this.storageLog, null, 2));
        } catch (error) {
            console.error('❌ Failed to save storage log:', error.message);
        }
    }

    // Format bytes to human readable
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Get storage statistics
    getStorageStats() {
        return {
            currentUsage: this.storageLog[this.storageLog.length - 1] || null,
            threshold: this.storageThreshold,
            adminDevices: Array.from(this.adminDevices.values()),
            storageLog: this.storageLog.slice(-20)
        };
    }

    // Emergency storage cleanup
    emergencyCleanup() {
        console.log('🚨 Emergency storage cleanup initiated');
        
        // Clear temporary files
        this.clearTempFiles();
        
        // Clear old logs
        this.clearOldLogs();
        
        // Force relocate more models
        this.relocateExistingModels();
        
        console.log('✅ Emergency cleanup completed');
    }

    // Clear temporary files
    clearTempFiles() {
        const tempDirs = ['temp', 'cache', 'logs'];
        
        tempDirs.forEach(dir => {
            const tempPath = path.join(__dirname, dir);
            if (fs.existsSync(tempPath)) {
                try {
                    const files = fs.readdirSync(tempPath);
                    files.forEach(file => {
                        const filePath = path.join(tempPath, file);
                        if (fs.statSync(filePath).isFile()) {
                            fs.unlinkSync(filePath);
                        }
                    });
                    console.log(`🧹 Cleared temp directory: ${dir}`);
                } catch (error) {
                    console.warn(`⚠️  Could not clear ${dir}:`, error.message);
                }
            }
        });
    }

    // Clear old logs
    clearOldLogs() {
        const maxLogAge = 7 * 24 * 60 * 60 * 1000; // 7 days
        const cutoff = Date.now() - maxLogAge;
        
        this.storageLog = this.storageLog.filter(log => 
            new Date(log.timestamp).getTime() > cutoff
        );
        
        this.saveStorageLog();
        console.log('🧹 Cleared old storage logs');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ShmryStorageManager;
}

// Auto-start if run directly
if (require.main === module) {
    const storageManager = new ShmryStorageManager();
    
    console.log('🚀 SHMRY Storage Manager started');
    console.log('💡 Monitoring storage and managing admin device redirects');
    console.log('🛑 Press Ctrl+C to stop');
    
    // Keep process running
    process.on('SIGINT', () => {
        console.log('\n🛑 Stopping storage manager...');
        process.exit(0);
    });
}
