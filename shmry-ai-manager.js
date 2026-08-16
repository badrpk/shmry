// SHMRY AI Model Manager - Edge Computing AI Integration
// Manages AI models across all devices in the SHMRY network

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

class ShmryAIModelManager {
    constructor() {
        this.models = new Map();
        this.devices = new Map();
        this.modelRegistry = new Map();
        this.edgeNodes = new Set();
        this.initializeModelRegistry();
    }

    // Initialize the AI model registry with common model types
    initializeModelRegistry() {
        // Language Models
        this.modelRegistry.set('llama2', {
            name: 'Llama 2',
            type: 'language',
            variants: ['7b', '7b-chat', '13b', '13b-chat', '70b', '70b-chat'],
            capabilities: ['text-generation', 'chat', 'code-generation', 'reasoning'],
            requirements: { ram: '8GB', vram: '4GB', storage: '4GB' }
        });

        this.modelRegistry.set('mistral', {
            name: 'Mistral AI',
            type: 'language',
            variants: ['7b', '7b-instruct', '8x7b', 'large'],
            capabilities: ['text-generation', 'instruction-following', 'reasoning'],
            requirements: { ram: '8GB', vram: '4GB', storage: '4GB' }
        });

        this.modelRegistry.set('deepseek', {
            name: 'DeepSeek',
            type: 'language',
            variants: ['r1:8b', 'r1:67b', 'coder:33b', 'coder:6.7b'],
            capabilities: ['text-generation', 'code-generation', 'reasoning'],
            requirements: { ram: '8GB', vram: '4GB', storage: '4GB' }
        });

        this.modelRegistry.set('qwen', {
            name: 'Qwen',
            type: 'language',
            variants: ['1.5:7b', '1.5:14b', '1.5:32b', '2:7b', '2:14b'],
            capabilities: ['text-generation', 'multilingual', 'reasoning'],
            requirements: { ram: '8GB', vram: '4GB', storage: '4GB' }
        });

        this.modelRegistry.set('phi', {
            name: 'Microsoft Phi',
            type: 'language',
            variants: ['2', '3', '3.5'],
            capabilities: ['text-generation', 'code-generation', 'reasoning'],
            requirements: { ram: '4GB', vram: '2GB', storage: '2GB' }
        });

        // Code Models
        this.modelRegistry.set('codellama', {
            name: 'Code Llama',
            type: 'code',
            variants: ['7b', '13b', '34b', 'python', 'instruct'],
            capabilities: ['code-generation', 'code-completion', 'debugging'],
            requirements: { ram: '8GB', vram: '4GB', storage: '4GB' }
        });

        // Vision Models
        this.modelRegistry.set('llava', {
            name: 'LLaVA',
            type: 'vision',
            variants: ['1.5:7b', '1.5:13b', '2:7b', '2:13b'],
            capabilities: ['image-understanding', 'visual-reasoning', 'image-description'],
            requirements: { ram: '8GB', vram: '6GB', storage: '4GB' }
        });

        // Speech Models
        this.modelRegistry.set('whisper', {
            name: 'OpenAI Whisper',
            type: 'speech',
            variants: ['tiny', 'base', 'small', 'medium', 'large'],
            capabilities: ['speech-to-text', 'transcription', 'multilingual'],
            requirements: { ram: '4GB', vram: '2GB', storage: '1GB' }
        });

        // Stable Diffusion Models
        this.modelRegistry.set('stable-diffusion', {
            name: 'Stable Diffusion',
            type: 'image-generation',
            variants: ['1.5', '2.1', 'xl', 'turbo'],
            capabilities: ['text-to-image', 'image-to-image', 'inpainting'],
            requirements: { ram: '8GB', vram: '8GB', storage: '4GB' }
        });

        console.log('✅ SHMRY AI Model Registry initialized');
    }

    // Discover AI models across all devices
    async discoverModels() {
        console.log('🔍 Discovering AI models across SHMRY network...');
        
        // Check local device
        await this.scanLocalDevice();
        
        // Check network devices
        await this.scanNetworkDevices();
        
        // Check cloud storage
        await this.scanCloudStorage();
        
        console.log(`✅ Discovery complete: ${this.models.size} models found`);
        return this.models;
    }

    // Scan local device for AI models
    async scanLocalDevice() {
        const localDevice = {
            id: 'local-device',
            name: 'SHMRY-Edge-01',
            type: 'edge-node',
            location: 'local',
            capabilities: ['ai-inference', 'edge-computing', 'local-storage']
        };

        this.devices.set('local-device', localDevice);

        // Common model locations to scan
        const modelPaths = [
            'C:\\Users\\HP 250 G10\\.ollama\\models',
            'C:\\Users\\HP 250 G10\\Downloads\\AI-Models',
            'C:\\Users\\HP 250 G10\\Documents\\AI-Models',
            'D:\\AI-Models',
            'D:\\shmry-edge-computing\\AI-Models'
        ];

        for (const modelPath of modelPaths) {
            if (fs.existsSync(modelPath)) {
                await this.scanDirectoryForModels(modelPath, 'local-device');
            }
        }
    }

    // Scan network devices
    async scanNetworkDevices() {
        // This would integrate with SHMRY's device discovery system
        // For now, we'll simulate network discovery
        const networkDevices = [
            {
                id: 'edge-node-01',
                name: 'SHMRY-Edge-02',
                type: 'edge-node',
                location: 'network',
                ip: '192.168.1.100',
                capabilities: ['ai-inference', 'edge-computing']
            },
            {
                id: 'edge-node-02',
                name: 'SHMRY-Edge-03',
                type: 'edge-node',
                location: 'network',
                ip: '192.168.1.101',
                capabilities: ['ai-inference', 'edge-computing']
            }
        ];

        networkDevices.forEach(device => {
            this.devices.set(device.id, device);
            this.edgeNodes.add(device.id);
        });
    }

    // Scan cloud storage
    async scanCloudStorage() {
        // This would integrate with SHMRY's cloud storage system
        console.log('☁️ Scanning SHMRY cloud storage for AI models...');
    }

    // Scan directory for AI models
    async scanDirectoryForModels(directoryPath, deviceId) {
        try {
            const items = fs.readdirSync(directoryPath, { withFileTypes: true });
            
            for (const item of items) {
                if (item.isDirectory()) {
                    // Check if it's a model directory
                    const modelInfo = this.identifyModelDirectory(item.name);
                    if (modelInfo) {
                        const modelPath = path.join(directoryPath, item.name);
                        const modelSize = await this.calculateDirectorySize(modelPath);
                        
                        const model = {
                            id: `${deviceId}-${item.name}`,
                            name: item.name,
                            type: modelInfo.type,
                            variant: modelInfo.variant,
                            capabilities: modelInfo.capabilities,
                            path: modelPath,
                            size: modelSize,
                            device: deviceId,
                            status: 'available',
                            lastAccessed: new Date().toISOString()
                        };
                        
                        this.models.set(model.id, model);
                        console.log(`📦 Found model: ${model.name} (${model.type}) - ${this.formatBytes(modelSize)}`);
                    }
                }
            }
        } catch (error) {
            console.warn(`⚠️ Error scanning directory ${directoryPath}:`, error.message);
        }
    }

    // Identify if a directory contains an AI model
    identifyModelDirectory(dirName) {
        const lowerName = dirName.toLowerCase();
        
        // Check for known model patterns
        for (const [modelKey, modelInfo] of this.modelRegistry) {
            if (lowerName.includes(modelKey)) {
                // Find variant
                let variant = 'default';
                for (const variantName of modelInfo.variants) {
                    if (lowerName.includes(variantName.replace(':', '-'))) {
                        variant = variantName;
                        break;
                    }
                }
                
                return {
                    type: modelInfo.type,
                    variant: variant,
                    capabilities: modelInfo.capabilities
                };
            }
        }
        
        return null;
    }

    // Calculate directory size
    async calculateDirectorySize(dirPath) {
        try {
            let totalSize = 0;
            const items = fs.readdirSync(dirPath, { withFileTypes: true });
            
            for (const item of items) {
                const itemPath = path.join(dirPath, item.name);
                if (item.isFile()) {
                    const stats = fs.statSync(itemPath);
                    totalSize += stats.size;
                } else if (item.isDirectory()) {
                    totalSize += await this.calculateDirectorySize(itemPath);
                }
            }
            
            return totalSize;
        } catch (error) {
            return 0;
        }
    }

    // Format bytes to human readable format
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Get model information
    getModelInfo(modelId) {
        return this.models.get(modelId);
    }

    // Get all models
    getAllModels() {
        return Array.from(this.models.values());
    }

    // Get models by type
    getModelsByType(type) {
        return Array.from(this.models.values()).filter(model => model.type === type);
    }

    // Get models by device
    getModelsByDevice(deviceId) {
        return Array.from(this.models.values()).filter(model => model.device === deviceId);
    }

    // Get available capabilities
    getAvailableCapabilities() {
        const capabilities = new Set();
        this.models.forEach(model => {
            model.capabilities.forEach(cap => capabilities.add(cap));
        });
        return Array.from(capabilities);
    }

    // Get system requirements for a model
    getModelRequirements(modelId) {
        const model = this.models.get(modelId);
        if (!model) return null;
        
        // Find registry info
        for (const [modelKey, modelInfo] of this.modelRegistry) {
            if (model.name.toLowerCase().includes(modelKey)) {
                return modelInfo.requirements;
            }
        }
        
        return { ram: '8GB', vram: '4GB', storage: '4GB' };
    }

    // Check if model can run on current device
    canRunModel(modelId) {
        const requirements = this.getModelRequirements(modelId);
        if (!requirements) return false;
        
        // This would check actual system resources
        // For now, return true as a placeholder
        return true;
    }

    // Get model statistics
    getModelStats() {
        const stats = {
            totalModels: this.models.size,
            totalSize: 0,
            byType: {},
            byDevice: {},
            capabilities: this.getAvailableCapabilities()
        };
        
        this.models.forEach(model => {
            stats.totalSize += model.size;
            
            // Count by type
            if (!stats.byType[model.type]) stats.byType[model.type] = 0;
            stats.byType[model.type]++;
            
            // Count by device
            if (!stats.byDevice[model.device]) stats.byDevice[model.device] = 0;
            stats.byDevice[model.device]++;
        });
        
        stats.totalSizeFormatted = this.formatBytes(stats.totalSize);
        return stats;
    }

    // Export model list for SHMRY integration
    exportForShmry() {
        return {
            models: this.getAllModels(),
            devices: Array.from(this.devices.values()),
            stats: this.getModelStats(),
            timestamp: new Date().toISOString()
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ShmryAIModelManager;
} else {
    // Browser environment
    window.ShmryAIModelManager = ShmryAIModelManager;
}
