#!/usr/bin/env node

// SHMRY AI Model Configuration Script
// Discovers and configures AI models across all devices for SHMRY Edge Computing

const ShmryAIModelManager = require('./shmry-ai-manager');
const ShmryAIInference = require('./shmry-ai-inference');
const fs = require('fs');
const path = require('path');

class ShmryAIConfigurator {
    constructor() {
        this.aiManager = new ShmryAIModelManager();
        this.aiInference = new ShmryAIInference(this.aiManager);
        this.configuration = {};
    }

    // Main configuration process
    async configureAllAIModels() {
        console.log('🚀 SHMRY AI Model Configuration Starting...\n');
        
        try {
            // Step 1: Discover all AI models
            console.log('📡 Step 1: Discovering AI models across all devices...');
            await this.discoverAllModels();
            
            // Step 2: Configure model capabilities
            console.log('\n⚙️ Step 2: Configuring model capabilities...');
            await this.configureModelCapabilities();
            
            // Step 3: Set up edge computing distribution
            console.log('\n🌐 Step 3: Setting up edge computing distribution...');
            await this.setupEdgeComputing();
            
            // Step 4: Test model integration
            console.log('\n🧪 Step 4: Testing model integration...');
            await this.testModelIntegration();
            
            // Step 5: Generate configuration report
            console.log('\n📊 Step 5: Generating configuration report...');
            await this.generateConfigurationReport();
            
            console.log('\n✅ SHMRY AI Model Configuration Complete!');
            console.log('🎯 Your AI models are now ready for edge computing!');
            
        } catch (error) {
            console.error('\n❌ Configuration failed:', error.message);
            process.exit(1);
        }
    }

    // Discover all AI models
    async discoverAllModels() {
        console.log('🔍 Scanning for AI models...');
        
        // Discover models using the AI Manager
        await this.aiManager.discoverModels();
        
        // Get discovered models
        const models = this.aiManager.getAllModels();
        const stats = this.aiManager.getModelStats();
        
        console.log(`📦 Found ${models.length} AI models:`);
        models.forEach(model => {
            console.log(`   • ${model.name} (${model.type}) - ${model.size ? this.formatBytes(model.size) : 'Unknown size'} - ${model.device}`);
        });
        
        console.log(`\n📊 Model Statistics:`);
        console.log(`   • Total Models: ${stats.totalModels}`);
        console.log(`   • Total Size: ${stats.totalSizeFormatted}`);
        console.log(`   • By Type: ${Object.entries(stats.byType).map(([type, count]) => `${type}: ${count}`).join(', ')}`);
        console.log(`   • By Device: ${Object.entries(stats.byDevice).map(([device, count]) => `${device}: ${count}`).join(', ')}`);
        
        this.configuration.models = models;
        this.configuration.stats = stats;
    }

    // Configure model capabilities
    async configureModelCapabilities() {
        console.log('⚙️ Configuring model capabilities...');
        
        const models = this.aiManager.getAllModels();
        const capabilities = this.aiManager.getAvailableCapabilities();
        
        console.log(`🎯 Available Capabilities: ${capabilities.join(', ')}`);
        
        // Configure each model
        for (const model of models) {
            console.log(`\n🔧 Configuring ${model.name}:`);
            
            // Get model requirements
            const requirements = this.aiManager.getModelRequirements(model.id);
            if (requirements) {
                console.log(`   • Requirements: RAM ${requirements.ram}, VRAM ${requirements.vram}, Storage ${requirements.storage}`);
            }
            
            // Check if model can run
            const canRun = this.aiManager.canRunModel(model.id);
            console.log(`   • Can Run: ${canRun ? '✅ Yes' : '❌ No'}`);
            
            // Update model status
            if (canRun) {
                model.status = 'configured';
                model.configuredAt = new Date().toISOString();
            } else {
                model.status = 'requirements-not-met';
                model.configuredAt = null;
            }
        }
        
        this.configuration.capabilities = capabilities;
    }

    // Setup edge computing distribution
    async setupEdgeComputing() {
        console.log('🌐 Setting up edge computing distribution...');
        
        const devices = Array.from(this.aiManager.devices.values());
        const edgeNodes = Array.from(this.aiManager.edgeNodes);
        
        console.log(`🏗️ Edge Computing Setup:`);
        console.log(`   • Total Devices: ${devices.length}`);
        console.log(`   • Edge Nodes: ${edgeNodes.length}`);
        
        // Configure edge computing for each device
        for (const device of devices) {
            console.log(`\n🖥️ Configuring ${device.name} (${device.type}):`);
            
            // Get models for this device
            const deviceModels = this.aiManager.getModelsByDevice(device.id);
            console.log(`   • AI Models: ${deviceModels.length}`);
            
            // Configure edge computing capabilities
            if (device.capabilities.includes('edge-computing')) {
                device.edgeComputing = {
                    enabled: true,
                    maxConcurrentInferences: 3,
                    loadBalancing: 'round-robin',
                    failover: true,
                    configuredAt: new Date().toISOString()
                };
                console.log(`   • Edge Computing: ✅ Enabled`);
            } else {
                device.edgeComputing = {
                    enabled: false,
                    reason: 'Device does not support edge computing'
                };
                console.log(`   • Edge Computing: ❌ Not Supported`);
            }
        }
        
        this.configuration.edgeComputing = {
            devices: devices,
            edgeNodes: edgeNodes,
            loadBalancing: 'round-robin',
            failover: true
        };
    }

    // Test model integration
    async testModelIntegration() {
        console.log('🧪 Testing model integration...');
        
        const availableModels = this.aiInference.getAvailableModels();
        console.log(`🎯 Testing ${availableModels.length} available models...`);
        
        let testResults = [];
        
        for (const model of availableModels.slice(0, 3)) { // Test first 3 models
            console.log(`\n🧪 Testing ${model.name}:`);
            
            try {
                // Submit a test inference
                const testInput = {
                    prompt: `Test prompt for ${model.name}`,
                    maxTokens: 100,
                    temperature: 0.7
                };
                
                const inference = this.aiInference.submitInference(
                    model.id,
                    testInput,
                    'language',
                    (error, result) => {
                        if (error) {
                            console.log(`   ❌ Test failed: ${error.message}`);
                        } else {
                            console.log(`   ✅ Test passed: ${result.response.substring(0, 100)}...`);
                        }
                    }
                );
                
                // Wait for completion
                await this.waitForInferenceCompletion(inference.id);
                
                const status = this.aiInference.getInferenceStatus(inference.id);
                if (status && status.status === 'completed') {
                    testResults.push({
                        model: model.name,
                        status: 'passed',
                        duration: status.duration
                    });
                } else {
                    testResults.push({
                        model: model.name,
                        status: 'failed',
                        error: status?.error || 'Unknown error'
                    });
                }
                
            } catch (error) {
                console.log(`   ❌ Test failed: ${error.message}`);
                testResults.push({
                    model: model.name,
                    status: 'failed',
                    error: error.message
                });
            }
        }
        
        // Wait a bit for any remaining inferences
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        const inferenceStats = this.aiInference.getInferenceStats();
        console.log(`\n📊 Test Results:`);
        console.log(`   • Tests Run: ${testResults.length}`);
        console.log(`   • Passed: ${testResults.filter(r => r.status === 'passed').length}`);
        console.log(`   • Failed: ${testResults.filter(r => r.status === 'failed').length}`);
        console.log(`   • Average Duration: ${Math.round(inferenceStats.averageDuration)}ms`);
        
        this.configuration.testResults = testResults;
        this.configuration.inferenceStats = inferenceStats;
    }

    // Wait for inference completion
    async waitForInferenceCompletion(inferenceId, timeout = 30000) {
        const startTime = Date.now();
        
        while (Date.now() - startTime < timeout) {
            const status = this.aiInference.getInferenceStatus(inferenceId);
            
            if (status && (status.status === 'completed' || status.status === 'failed')) {
                return status;
            }
            
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        throw new Error('Inference timeout');
    }

    // Generate configuration report
    async generateConfigurationReport() {
        console.log('📊 Generating configuration report...');
        
        const report = {
            timestamp: new Date().toISOString(),
            configuration: this.configuration,
            summary: {
                totalModels: this.configuration.stats.totalModels,
                totalSize: this.configuration.stats.totalSizeFormatted,
                availableCapabilities: this.configuration.capabilities,
                edgeComputingEnabled: this.configuration.edgeComputing.edgeNodes.length > 0,
                testResults: this.configuration.testResults
            }
        };
        
        // Save report to file
        const reportPath = path.join(__dirname, 'shmry-ai-configuration-report.json');
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
        
        console.log(`📄 Configuration report saved to: ${reportPath}`);
        
        // Display summary
        console.log('\n📋 SHMRY AI Configuration Summary:');
        console.log(`   • Total AI Models: ${report.summary.totalModels}`);
        console.log(`   • Total Storage: ${report.summary.totalSize}`);
        console.log(`   • Capabilities: ${report.summary.availableCapabilities.join(', ')}`);
        console.log(`   • Edge Computing: ${report.summary.edgeComputingEnabled ? '✅ Enabled' : '❌ Disabled'}`);
        console.log(`   • Test Results: ${report.summary.testResults.filter(r => r.status === 'passed').length}/${report.summary.testResults.length} passed`);
    }

    // Format bytes helper
    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Main execution
async function main() {
    const configurator = new ShmryAIConfigurator();
    await configurator.configureAllAIModels();
}

// Run if called directly
if (require.main === module) {
    main().catch(error => {
        console.error('❌ Configuration failed:', error);
        process.exit(1);
    });
}

module.exports = ShmryAIConfigurator;
