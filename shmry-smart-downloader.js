// SHMRY Smart Downloader
// Automatically redirects downloads to admin devices when local storage is low

const fs = require('fs');
const path = require('path');
const ShmryStorageManager = require('./shmry-storage-manager');

class ShmrySmartDownloader {
    constructor() {
        this.storageManager = new ShmryStorageManager();
        this.downloadQueue = [];
        this.activeDownloads = new Map();
        this.downloadedModels = new Set();
        this.maxConcurrentDownloads = 3;
        this.downloadLog = [];
        
        this.localDownloadPath = path.join(__dirname, 'AI-Models');
        this.adminDownloadPath = 'admin-devices-storage';
        
        this.loadDownloadQueue();
        this.startSmartDownloads();
    }

    // Load comprehensive model download queue
    loadDownloadQueue() {
        this.downloadQueue = [
            // Large Language Models (LLMs)
            {
                name: 'Llama 3 70B',
                url: 'https://huggingface.co/meta-llama/Llama-3-70B-Instruct',
                type: 'llm',
                size: '140GB',
                priority: 'high',
                description: 'Meta\'s latest large language model with 70B parameters',
                preferredLocation: 'local' // Prefer local if space available
            },
            {
                name: 'Mistral 7B Instruct',
                url: 'https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2',
                type: 'llm',
                size: '14GB',
                priority: 'high',
                description: 'High-performance 7B parameter instruction model',
                preferredLocation: 'local'
            },
            {
                name: 'DeepSeek Coder 33B',
                url: 'https://huggingface.co/deepseek-ai/deepseek-coder-33b-instruct',
                type: 'code',
                size: '66GB',
                priority: 'high',
                description: 'Advanced code generation and understanding model',
                preferredLocation: 'local'
            },
            {
                name: 'Qwen 2.5 72B',
                url: 'https://huggingface.co/Qwen/Qwen2.5-72B-Instruct',
                type: 'llm',
                size: '144GB',
                priority: 'medium',
                description: 'Alibaba\'s large multilingual model',
                preferredLocation: 'admin' // Large models go to admin devices
            },
            {
                name: 'Code Llama 70B',
                url: 'https://huggingface.co/codellama/CodeLlama-70b-Instruct-hf',
                type: 'code',
                size: '140GB',
                priority: 'medium',
                description: 'Meta\'s largest code generation model',
                preferredLocation: 'admin'
            },
            {
                name: 'LLaVA 1.6 34B',
                url: 'https://huggingface.co/llava-hf/llava-1.6-34b',
                type: 'vision',
                size: '68GB',
                priority: 'medium',
                description: 'Advanced vision-language model',
                preferredLocation: 'admin'
            },
            {
                name: 'Stable Diffusion XL',
                url: 'https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0',
                type: 'image',
                size: '6.9GB',
                priority: 'medium',
                description: 'High-quality image generation model',
                preferredLocation: 'local'
            },
            {
                name: 'Whisper Large V3',
                url: 'https://huggingface.co/openai/whisper-large-v3',
                type: 'speech',
                size: '1.5GB',
                priority: 'low',
                description: 'Advanced speech recognition model',
                preferredLocation: 'local'
            },
            {
                name: 'Gemma 2 27B',
                url: 'https://huggingface.co/google/gemma-2-27b-it',
                type: 'llm',
                size: '54GB',
                priority: 'medium',
                description: 'Google\'s efficient large language model',
                preferredLocation: 'admin'
            },
            {
                name: 'Phi 3.5 14B',
                url: 'https://huggingface.co/microsoft/Phi-3.5-14B-Instruct',
                type: 'llm',
                size: '28GB',
                priority: 'medium',
                description: 'Microsoft\'s efficient reasoning model',
                preferredLocation: 'local'
            },
            {
                name: 'Claude 3.5 Sonnet',
                url: 'https://huggingface.co/anthropic/claude-3.5-sonnet',
                type: 'llm',
                size: '28GB',
                priority: 'high',
                description: 'Anthropic\'s advanced reasoning model',
                preferredLocation: 'local'
            },
            {
                name: 'GPT-4o Mini',
                url: 'https://huggingface.co/openai/gpt-4o-mini',
                type: 'llm',
                size: '14GB',
                priority: 'high',
                description: 'OpenAI\'s efficient GPT-4 model',
                preferredLocation: 'local'
            },
            {
                name: 'Cohere Command R+',
                url: 'https://huggingface.co/CohereForAI/command-r-plus',
                type: 'llm',
                size: '104GB',
                priority: 'medium',
                description: 'Cohere\'s large language model',
                preferredLocation: 'admin'
            },
            {
                name: 'Yi 1.5 34B',
                url: 'https://huggingface.co/01-ai/Yi-1.5-34B-Chat',
                type: 'llm',
                size: '68GB',
                priority: 'medium',
                description: '01.AI\'s large language model',
                preferredLocation: 'admin'
            },
            {
                name: 'InternLM 2.5 20B',
                url: 'https://huggingface.co/internlm/internlm2.5-20b-chat',
                type: 'llm',
                size: '40GB',
                priority: 'low',
                description: 'Shanghai AI Lab\'s language model',
                preferredLocation: 'admin'
            }
        ];

        console.log(`📥 Loaded ${this.downloadQueue.length} models for smart download`);
    }

    // Start smart download process
    startSmartDownloads() {
        console.log('🚀 Starting SHMRY Smart Downloader...');
        console.log('💡 Automatically redirects downloads based on storage availability');
        
        this.processDownloadQueue();
        
        // Set up periodic queue processing
        setInterval(() => {
            this.processDownloadQueue();
        }, 30000); // Check every 30 seconds
        
        // Set up download status reporting
        setInterval(() => {
            this.reportDownloadStatus();
        }, 60000); // Report every minute
    }

    // Process download queue with smart location selection
    processDownloadQueue() {
        const activeCount = this.activeDownloads.size;
        const availableSlots = this.maxConcurrentDownloads - activeCount;
        
        if (availableSlots <= 0) return;
        
        // Get storage status
        const storageStats = this.storageManager.getStorageStats();
        const useAdminDevices = storageStats.currentUsage && 
                               storageStats.currentUsage.localUsage >= 70;
        
        // Sort by priority and start downloads
        const pendingModels = this.downloadQueue
            .filter(model => !this.activeDownloads.has(model.name) && !this.downloadedModels.has(model.name))
            .sort((a, b) => this.getPriorityScore(b.priority) - this.getPriorityScore(a.priority))
            .slice(0, availableSlots);
        
        pendingModels.forEach(model => {
            const downloadLocation = this.selectDownloadLocation(model, useAdminDevices);
            this.startDownload(model, downloadLocation);
        });
    }

    // Select optimal download location
    selectDownloadLocation(model, useAdminDevices) {
        // If storage is critical, prefer admin devices
        if (useAdminDevices) {
            if (model.preferredLocation === 'admin') {
                return 'admin';
            } else if (model.size.includes('GB') && parseInt(model.size) > 50) {
                return 'admin'; // Large models go to admin devices
            }
        }
        
        // Check if local storage has enough space
        const storageInfo = this.storageManager.getStorageInfo();
        const modelSizeBytes = this.parseModelSize(model.size);
        
        if (storageInfo.free > modelSizeBytes * 2) { // Need 2x space for safety
            return 'local';
        }
        
        // Default to admin devices if local storage is insufficient
        return 'admin';
    }

    // Parse model size string to bytes
    parseModelSize(sizeStr) {
        const size = parseFloat(sizeStr);
        if (sizeStr.includes('GB')) {
            return size * 1024 * 1024 * 1024;
        } else if (sizeStr.includes('MB')) {
            return size * 1024 * 1024;
        } else if (sizeStr.includes('KB')) {
            return size * 1024;
        }
        return size;
    }

    // Get priority score
    getPriorityScore(priority) {
        const scores = { 'high': 3, 'medium': 2, 'low': 1 };
        return scores[priority] || 1;
    }

    // Start download with specified location
    startDownload(model, location) {
        const locationText = location === 'admin' ? '🌐 Admin Device' : '💻 Local Storage';
        console.log(`📥 Starting download: ${model.name} (${model.size}) → ${locationText}`);
        
        this.activeDownloads.set(model.name, {
            model,
            location,
            startTime: Date.now(),
            progress: 0,
            status: 'downloading'
        });
        
        // Simulate download process
        this.simulateDownload(model, location);
    }

    // Simulate download process
    simulateDownload(model, location) {
        const downloadId = setInterval(() => {
            const download = this.activeDownloads.get(model.name);
            if (!download) return;
            
            download.progress += Math.random() * 15; // Simulate progress
            
            if (download.progress >= 100) {
                download.progress = 100;
                download.status = 'completed';
                download.endTime = Date.now();
                
                this.activeDownloads.delete(model.name);
                this.downloadedModels.add(model.name);
                
                clearInterval(downloadId);
                
                console.log(`✅ Download completed: ${model.name} → ${location === 'admin' ? '🌐 Admin Device' : '💻 Local Storage'}`);
                this.logDownload(model, 'completed', location);
                
                // Add to SHMRY Search Engine
                this.addModelToSearchEngine(model, location);
            }
        }, 2000); // Update every 2 seconds
    }

    // Log download activity
    logDownload(model, status, location) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            model: model.name,
            status,
            size: model.size,
            type: model.type,
            location: location,
            priority: model.priority
        };
        
        this.downloadLog.push(logEntry);
        
        // Save to appropriate location
        const logPath = location === 'admin' 
            ? path.join(this.adminDownloadPath, 'download-log.json')
            : path.join(this.localDownloadPath, 'download-log.json');
        
        try {
            const existingLogs = fs.existsSync(logPath) 
                ? JSON.parse(fs.readFileSync(logPath, 'utf8')) 
                : [];
            existingLogs.push(logEntry);
            fs.writeFileSync(logPath, JSON.stringify(existingLogs, null, 2));
        } catch (error) {
            console.error(`❌ Failed to save download log to ${location}:`, error.message);
        }
    }

    // Add downloaded model to SHMRY Search Engine
    addModelToSearchEngine(model, location) {
        try {
            console.log(`🔧 Adding ${model.name} to SHMRY Search Engine (${location})`);
            
            // Update model status in search engine
            // searchEngine.addAIModel(model, location);
            
        } catch (error) {
            console.error(`❌ Failed to add ${model.name} to search engine:`, error.message);
        }
    }

    // Report download status
    reportDownloadStatus() {
        const activeCount = this.activeDownloads.size;
        const completedCount = this.downloadedModels.size;
        const pendingCount = this.downloadQueue.length - completedCount - activeCount;
        
        // Get storage info
        const storageStats = this.storageManager.getStorageStats();
        const storageStatus = storageStats.currentUsage;
        
        console.log('\n📊 Smart Download Status Report:');
        console.log(`   Active Downloads: ${activeCount}`);
        console.log(`   Completed: ${completedCount}`);
        console.log(`   Pending: ${pendingCount}`);
        
        if (storageStatus) {
            console.log(`   💾 Storage: ${storageStatus.localUsage.toFixed(1)}% used`);
            console.log(`   📊 Status: ${storageStatus.status}`);
        }
        
        if (activeCount > 0) {
            console.log('\n🔄 Currently Downloading:');
            this.activeDownloads.forEach((download, name) => {
                const progress = Math.round(download.progress);
                const elapsed = Math.round((Date.now() - download.startTime) / 1000);
                const location = download.location === 'admin' ? '🌐 Admin' : '💻 Local';
                console.log(`   ${name}: ${progress}% (${elapsed}s) → ${location}`);
            });
        }
        
        if (completedCount > 0) {
            console.log('\n✅ Recently Completed:');
            const recent = this.downloadLog
                .filter(log => log.status === 'completed')
                .slice(-5);
            recent.forEach(log => {
                const location = log.location === 'admin' ? '🌐 Admin' : '💻 Local';
                console.log(`   ${log.model} (${log.size}) → ${location}`);
            });
        }
        
        // Show admin device status
        if (storageStats.adminDevices.length > 0) {
            console.log('\n🌐 Admin Devices Status:');
            storageStats.adminDevices.forEach(device => {
                const status = device.status === 'online' ? '🟢' : '🔴';
                console.log(`   ${status} ${device.name}: ${device.availableSpace} available`);
            });
        }
    }

    // Get download statistics
    getDownloadStats() {
        const localDownloads = this.downloadLog.filter(log => log.location === 'local');
        const adminDownloads = this.downloadLog.filter(log => log.location === 'admin');
        
        return {
            totalModels: this.downloadQueue.length,
            activeDownloads: this.activeDownloads.size,
            completedDownloads: this.downloadedModels.size,
            pendingDownloads: this.downloadQueue.length - this.downloadedModels.size - this.activeDownloads.size,
            localDownloads: localDownloads.length,
            adminDownloads: adminDownloads.length,
            downloadLog: this.downloadLog.slice(-20)
        };
    }

    // Force redirect all downloads to admin devices
    forceAdminRedirects() {
        console.log('🔄 Forcing all downloads to admin devices...');
        
        // Update storage manager threshold temporarily
        this.storageManager.storageThreshold = 50; // Lower threshold to force admin redirects
        
        // Update downloader configuration
        this.storageManager.updateDownloaderConfig({
            useAdminDevices: true,
            localStorageThreshold: 50,
            forceAdminRedirects: true
        });
        
        console.log('✅ All new downloads will go to admin devices');
    }

    // Resume local downloads when space is available
    resumeLocalDownloads() {
        console.log('🔄 Resuming local downloads...');
        
        // Restore normal threshold
        this.storageManager.storageThreshold = 80;
        
        // Update downloader configuration
        this.storageManager.updateDownloaderConfig({
            useAdminDevices: false,
            localStorageThreshold: 80,
            forceAdminRedirects: false
        });
        
        console.log('✅ Local downloads resumed');
    }

    // Emergency storage cleanup
    emergencyCleanup() {
        console.log('🚨 Emergency cleanup initiated...');
        this.storageManager.emergencyCleanup();
        console.log('✅ Emergency cleanup completed');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ShmrySmartDownloader;
}

// Auto-start if run directly
if (require.main === module) {
    const smartDownloader = new ShmrySmartDownloader();
    
    console.log('🚀 SHMRY Smart Downloader started');
    console.log('💡 Automatically manages download locations based on storage');
    console.log('🛑 Press Ctrl+C to stop');
    
    // Keep process running
    process.on('SIGINT', () => {
        console.log('\n🛑 Stopping smart downloader...');
        process.exit(0);
    });
}
