#!/usr/bin/env node

// SHMRY AI Model Discovery Script
// Comprehensive discovery of AI models across all devices and formats

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

class ShmryAIModelDiscovery {
    constructor() {
        this.discoveredModels = [];
        this.searchPaths = [];
        this.modelFormats = new Set();
        this.initializeSearchPaths();
    }

    // Initialize search paths for AI models
    initializeSearchPaths() {
        // Common AI model locations
        this.searchPaths = [
            // User directories
            'C:\\Users\\HP 250 G10\\Downloads',
            'C:\\Users\\HP 250 G10\\Documents',
            'C:\\Users\\HP 250 G10\\Desktop',
            
            // Drive directories
            'D:\\',
            'D:\\AI-Models',
            'D:\\shmry-edge-computing',
            'D:\\shmry-edge-computing\\AI-Models',
            
            // Program files
            'C:\\Program Files',
            'C:\\Program Files (x86)',
            
            // Python packages
            'C:\\Python313\\Lib\\site-packages',
            'C:\\Users\\HP 250 G10\\AppData\\Local\\Programs\\Python',
            
            // Common model directories
            'C:\\Users\\HP 250 G10\\.cache',
            'C:\\Users\\HP 250 G10\\AppData\\Local',
            'C:\\Users\\HP 250 G10\\AppData\\Roaming'
        ];
    }

    // Main discovery process
    async discoverAllModels() {
        console.log('🚀 SHMRY AI Model Discovery Starting...\n');
        
        try {
            // Step 1: Search for model files
            console.log('📡 Step 1: Searching for AI model files...');
            await this.searchForModelFiles();
            
            // Step 2: Search for model directories
            console.log('\n📁 Step 2: Searching for AI model directories...');
            await this.searchForModelDirectories();
            
            // Step 3: Search for Python AI packages
            console.log('\n🐍 Step 3: Searching for Python AI packages...');
            await this.searchForPythonAIPackages();
            
            // Step 4: Search for executable AI tools
            console.log('\n⚙️ Step 4: Searching for executable AI tools...');
            await this.searchForExecutableAITools();
            
            // Step 5: Generate discovery report
            console.log('\n📊 Step 5: Generating discovery report...');
            await this.generateDiscoveryReport();
            
            console.log('\n✅ SHMRY AI Model Discovery Complete!');
            console.log(`🎯 Found ${this.discoveredModels.length} potential AI models/tools!`);
            
        } catch (error) {
            console.error('\n❌ Discovery failed:', error.message);
            process.exit(1);
        }
    }

    // Search for model files
    async searchForModelFiles() {
        const modelFileExtensions = [
            '.bin', '.safetensors', '.ckpt', '.pth', '.pt', '.onnx', '.pb',
            '.tflite', '.h5', '.model', '.weights', '.gguf', '.ggml'
        ];

        for (const searchPath of this.searchPaths) {
            if (fs.existsSync(searchPath)) {
                try {
                    await this.searchDirectoryForModelFiles(searchPath, modelFileExtensions);
                } catch (error) {
                    console.warn(`⚠️ Error searching ${searchPath}:`, error.message);
                }
            }
        }
    }

    // Search directory for model files
    async searchDirectoryForModelFiles(dirPath, extensions, depth = 0) {
        if (depth > 3) return; // Limit recursion depth
        
        try {
            const items = fs.readdirSync(dirPath, { withFileTypes: true });
            
            for (const item of items) {
                const itemPath = path.join(dirPath, item.name);
                
                if (item.isFile()) {
                    // Check if file is a model file
                    const ext = path.extname(item.name).toLowerCase();
                    if (extensions.includes(ext)) {
                        const fileSize = fs.statSync(itemPath).size;
                        if (fileSize > 1024 * 1024) { // Only files larger than 1MB
                            const model = {
                                name: item.name,
                                path: itemPath,
                                type: 'model-file',
                                format: ext,
                                size: fileSize,
                                sizeFormatted: this.formatBytes(fileSize),
                                discoveredAt: new Date().toISOString()
                            };
                            
                            this.discoveredModels.push(model);
                            console.log(`📦 Found model file: ${item.name} (${model.sizeFormatted}) - ${ext}`);
                        }
                    }
                } else if (item.isDirectory() && !item.name.startsWith('.')) {
                    // Recursively search subdirectories
                    await this.searchDirectoryForModelFiles(itemPath, extensions, depth + 1);
                }
            }
        } catch (error) {
            // Skip directories we can't access
        }
    }

    // Search for model directories
    async searchForModelDirectories() {
        const modelDirectoryPatterns = [
            'models', 'ai-models', 'ai_models', 'llm', 'llms', 'transformers',
            'huggingface', 'torch', 'tensorflow', 'onnx', 'openai', 'anthropic',
            'llama', 'mistral', 'deepseek', 'qwen', 'phi', 'codellama',
            'stable-diffusion', 'whisper', 'llava', 'gpt', 'bert', 'roberta'
        ];

        for (const searchPath of this.searchPaths) {
            if (fs.existsSync(searchPath)) {
                try {
                    await this.searchDirectoryForModelDirectories(searchPath, modelDirectoryPatterns);
                } catch (error) {
                    console.warn(`⚠️ Error searching ${searchPath}:`, error.message);
                }
            }
        }
    }

    // Search directory for model directories
    async searchDirectoryForModelDirectories(dirPath, patterns, depth = 0) {
        if (depth > 2) return; // Limit recursion depth
        
        try {
            const items = fs.readdirSync(dirPath, { withFileTypes: true });
            
            for (const item of items) {
                if (item.isDirectory()) {
                    const itemPath = path.join(dirPath, item.name);
                    const lowerName = item.name.toLowerCase();
                    
                    // Check if directory matches model patterns
                    const isModelDir = patterns.some(pattern => 
                        lowerName.includes(pattern) || 
                        lowerName.includes(pattern.replace('-', '')) ||
                        lowerName.includes(pattern.replace('_', ''))
                    );
                    
                    if (isModelDir) {
                        try {
                            const dirSize = await this.calculateDirectorySize(itemPath);
                            const model = {
                                name: item.name,
                                path: itemPath,
                                type: 'model-directory',
                                format: 'directory',
                                size: dirSize,
                                sizeFormatted: this.formatBytes(dirSize),
                                discoveredAt: new Date().toISOString()
                            };
                            
                            this.discoveredModels.push(model);
                            console.log(`📁 Found model directory: ${item.name} (${model.sizeFormatted})`);
                        } catch (error) {
                            console.warn(`⚠️ Could not calculate size for ${itemPath}:`, error.message);
                        }
                    }
                    
                    // Recursively search subdirectories
                    await this.searchDirectoryForModelDirectories(itemPath, patterns, depth + 1);
                }
            }
        } catch (error) {
            // Skip directories we can't access
        }
    }

    // Search for Python AI packages
    async searchForPythonAIPackages() {
        const pythonPaths = [
            'C:\\Python313\\Lib\\site-packages',
            'C:\\Users\\HP 250 G10\\AppData\\Local\\Programs\\Python',
            'C:\\Users\\HP 250 G10\\AppData\\Roaming\\Python'
        ];

        const aiPackagePatterns = [
            'torch', 'tensorflow', 'transformers', 'huggingface', 'openai',
            'anthropic', 'langchain', 'llama', 'mistral', 'deepseek',
            'stable-diffusion', 'whisper', 'llava', 'qwen', 'phi'
        ];

        for (const pythonPath of pythonPaths) {
            if (fs.existsSync(pythonPath)) {
                try {
                    await this.searchDirectoryForPythonPackages(pythonPath, aiPackagePatterns);
                } catch (error) {
                    console.warn(`⚠️ Error searching Python path ${pythonPath}:`, error.message);
                }
            }
        }
    }

    // Search directory for Python packages
    async searchDirectoryForPythonPackages(dirPath, patterns) {
        try {
            const items = fs.readdirSync(dirPath, { withFileTypes: true });
            
            for (const item of items) {
                if (item.isDirectory()) {
                    const lowerName = item.name.toLowerCase();
                    
                    // Check if directory matches AI package patterns
                    const isAIPackage = patterns.some(pattern => 
                        lowerName.includes(pattern) || 
                        lowerName.includes(pattern.replace('-', '')) ||
                        lowerName.includes(pattern.replace('_', ''))
                    );
                    
                    if (isAIPackage) {
                        const itemPath = path.join(dirPath, item.name);
                        try {
                            const dirSize = await this.calculateDirectorySize(itemPath);
                            const model = {
                                name: item.name,
                                path: itemPath,
                                type: 'python-ai-package',
                                format: 'python-package',
                                size: dirSize,
                                sizeFormatted: this.formatBytes(dirSize),
                                discoveredAt: new Date().toISOString()
                            };
                            
                            this.discoveredModels.push(model);
                            console.log(`🐍 Found Python AI package: ${item.name} (${model.sizeFormatted})`);
                        } catch (error) {
                            console.warn(`⚠️ Could not calculate size for ${itemPath}:`, error.message);
                        }
                    }
                }
            }
        } catch (error) {
            // Skip directories we can't access
        }
    }

    // Search for executable AI tools
    async searchForExecutableAITools() {
        const executablePaths = [
            'C:\\Program Files',
            'C:\\Program Files (x86)',
            'C:\\Users\\HP 250 G10\\AppData\\Local\\Programs',
            'C:\\Users\\HP 250 G10\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs'
        ];

        const aiToolPatterns = [
            'ollama', 'llama', 'mistral', 'deepseek', 'qwen', 'phi',
            'stable-diffusion', 'whisper', 'llava', 'gpt', 'bert',
            'tensorflow', 'pytorch', 'huggingface', 'openai', 'anthropic'
        ];

        for (const execPath of executablePaths) {
            if (fs.existsSync(execPath)) {
                try {
                    await this.searchDirectoryForExecutableTools(execPath, aiToolPatterns);
                } catch (error) {
                    console.warn(`⚠️ Error searching executable path ${execPath}:`, error.message);
                }
            }
        }
    }

    // Search directory for executable tools
    async searchDirectoryForExecutableTools(dirPath, patterns, depth = 0) {
        if (depth > 2) return; // Limit recursion depth
        
        try {
            const items = fs.readdirSync(dirPath, { withFileTypes: true });
            
            for (const item of items) {
                const itemPath = path.join(dirPath, item.name);
                
                if (item.isDirectory()) {
                    const lowerName = item.name.toLowerCase();
                    
                    // Check if directory matches AI tool patterns
                    const isAITool = patterns.some(pattern => 
                        lowerName.includes(pattern) || 
                        lowerName.includes(pattern.replace('-', '')) ||
                        lowerName.includes(pattern.replace('_', ''))
                    );
                    
                    if (isAITool) {
                        try {
                            const dirSize = await this.calculateDirectorySize(itemPath);
                            const model = {
                                name: item.name,
                                path: itemPath,
                                type: 'executable-ai-tool',
                                format: 'executable',
                                size: dirSize,
                                sizeFormatted: this.formatBytes(dirSize),
                                discoveredAt: new Date().toISOString()
                            };
                            
                            this.discoveredModels.push(model);
                            console.log(`⚙️ Found executable AI tool: ${item.name} (${model.sizeFormatted})`);
                        } catch (error) {
                            console.warn(`⚠️ Could not calculate size for ${itemPath}:`, error.message);
                        }
                    }
                    
                    // Recursively search subdirectories
                    await this.searchDirectoryForExecutableTools(itemPath, patterns, depth + 1);
                }
            }
        } catch (error) {
            // Skip directories we can't access
        }
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

    // Format bytes helper
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Generate discovery report
    async generateDiscoveryReport() {
        console.log('📊 Generating discovery report...');
        
        // Group models by type
        const modelsByType = {};
        this.discoveredModels.forEach(model => {
            if (!modelsByType[model.type]) {
                modelsByType[model.type] = [];
            }
            modelsByType[model.type].push(model);
        });
        
        // Calculate statistics
        const totalSize = this.discoveredModels.reduce((sum, model) => sum + model.size, 0);
        const stats = {
            totalModels: this.discoveredModels.length,
            totalSize: totalSize,
            totalSizeFormatted: this.formatBytes(totalSize),
            byType: Object.keys(modelsByType).map(type => ({
                type: type,
                count: modelsByType[type].length,
                totalSize: modelsByType[type].reduce((sum, model) => sum + model.size, 0)
            }))
        };
        
        // Display summary
        console.log('\n📋 SHMRY AI Model Discovery Summary:');
        console.log(`   • Total Items Found: ${stats.totalModels}`);
        console.log(`   • Total Size: ${stats.totalSizeFormatted}`);
        console.log(`   • By Type:`);
        
        stats.byType.forEach(typeInfo => {
            const typeSize = this.formatBytes(typeInfo.totalSize);
            console.log(`     - ${typeInfo.type}: ${typeInfo.count} items (${typeSize})`);
        });
        
        // Save detailed report
        const report = {
            timestamp: new Date().toISOString(),
            summary: stats,
            models: this.discoveredModels,
            searchPaths: this.searchPaths
        };
        
        const reportPath = path.join(__dirname, 'shmry-ai-discovery-report.json');
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        
        console.log(`\n📄 Detailed discovery report saved to: ${reportPath}`);
        
        // Display top models by size
        const topModels = this.discoveredModels
            .sort((a, b) => b.size - a.size)
            .slice(0, 10);
        
        console.log('\n🏆 Top 10 Largest AI Models/Tools:');
        topModels.forEach((model, index) => {
            console.log(`   ${index + 1}. ${model.name} - ${model.sizeFormatted} (${model.type})`);
        });
    }
}

// Main execution
async function main() {
    const discovery = new ShmryAIModelDiscovery();
    await discovery.discoverAllModels();
}

// Run if called directly
if (require.main === module) {
    main().catch(error => {
        console.error('❌ Discovery failed:', error);
        process.exit(1);
    });
}

module.exports = ShmryAIModelDiscovery;
