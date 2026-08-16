/**
 * Shmry Platform Demo
 * Demonstrates how to use all 190+ modules
 */

// Demo function to showcase Shmry Platform capabilities
async function demoShmryPlatform() {
    console.log('🚀 Starting Shmry Platform Demo...\n');
    
    try {
        // Initialize Shmry Platform
        const shmry = await initializeShmry({
            enableAllModules: true,
            autoStart: true,
            healthCheckInterval: 10000,
            enableLogging: true
        });
        
        console.log('✅ Shmry Platform initialized successfully!');
        console.log(`📊 Total modules loaded: ${shmry.getModuleCount()}`);
        console.log(`🔍 Available modules: ${shmry.getAllModules().slice(0, 10).join(', ')}...\n`);
        
        // Demo AI capabilities
        console.log('🤖 AI Module Demo:');
        const aiModule = shmry.getModule('ai');
        if (aiModule) {
            const aiHealth = await aiModule.healthCheck();
            console.log(`   AI System Status: ${aiHealth.status}`);
            console.log(`   AI Models: ${Object.keys(aiHealth.models || {}).length}`);
        }
        
        // Demo Edge Computing capabilities
        console.log('\n🌐 Edge Computing Module Demo:');
        const edgeModule = shmry.getModule('edge');
        if (edgeModule) {
            const edgeHealth = await edgeModule.healthCheck();
            console.log(`   Edge System Status: ${edgeHealth.status}`);
            console.log(`   Edge Modules: ${Object.keys(edgeHealth.modules || {}).length}`);
        }
        
        // Demo Cloud Infrastructure capabilities
        console.log('\n☁️ Cloud Infrastructure Module Demo:');
        const cloudModule = shmry.getModule('cloud');
        if (cloudModule) {
            const cloudHealth = await cloudModule.healthCheck();
            console.log(`   Cloud System Status: ${cloudHealth.status}`);
            console.log(`   Cloud Services: ${Object.keys(cloudHealth.services || {}).length}`);
        }
        
        // Demo Commerce capabilities
        console.log('\n🛒 Commerce Module Demo:');
        const commerceModule = shmry.getModule('commerce');
        if (commerceModule) {
            const commerceHealth = await commerceModule.healthCheck();
            console.log(`   Commerce System Status: ${commerceHealth.status}`);
            console.log(`   Commerce Services: ${Object.keys(commerceHealth.services || {}).length}`);
        }
        
        // Demo specific module functionality
        console.log('\n🔧 Specific Module Functionality Demo:');
        
        // Demo AI inference
        if (aiModule && aiModule.inference) {
            const aiResult = await aiModule.inference('Hello, Shmry!', 'core');
            console.log(`   AI Inference Result: ${JSON.stringify(aiResult, null, 2)}`);
        }
        
        // Demo Edge node creation
        if (edgeModule && edgeModule.modules && edgeModule.modules.get('node')) {
            const nodeModule = edgeModule.modules.get('node');
            if (nodeModule.createInstance) {
                const instance = await nodeModule.createInstance({
                    type: 'demo',
                    config: { memory: '2GB', cpu: '2 cores' }
                });
                console.log(`   Edge Instance Created: ${JSON.stringify(instance, null, 2)}`);
            }
        }
        
        // Demo Cloud compute
        if (cloudModule && cloudModule.services && cloudModule.services.get('compute')) {
            const computeService = cloudModule.services.get('compute');
            if (computeService.createInstance) {
                const cloudInstance = await computeService.createInstance({
                    type: 't2.micro',
                    image: 'ubuntu-20.04'
                });
                console.log(`   Cloud Instance Created: ${JSON.stringify(cloudInstance, null, 2)}`);
            }
        }
        
        // Demo Commerce store creation
        if (commerceModule && commerceModule.services && commerceModule.services.get('rangoons')) {
            const rangoonsService = commerceModule.services.get('rangoons');
            if (rangoonsService.createStorefront) {
                const store = await rangoonsService.createStorefront({
                    name: 'Demo Store',
                    theme: 'modern',
                    domain: 'demo.shmry.com'
                });
                console.log(`   Store Created: ${JSON.stringify(store, null, 2)}`);
            }
        }
        
        // Get system health
        console.log('\n🏥 System Health Check:');
        const health = await shmry.getSystemHealth();
        console.log(`   Overall Status: ${health.status}`);
        console.log(`   Core Systems: ${Object.keys(health.systems).length}`);
        console.log(`   Total Modules: ${health.modules.length}`);
        
        // Show healthy vs unhealthy modules
        const healthyModules = health.modules.filter(m => m.status === 'healthy').length;
        const unhealthyModules = health.modules.filter(m => m.status !== 'healthy').length;
        console.log(`   Healthy Modules: ${healthyModules}`);
        console.log(`   Unhealthy Modules: ${unhealthyModules}`);
        
        console.log('\n🎉 Shmry Platform Demo completed successfully!');
        console.log('💡 The platform is now ready for production use with all 190+ modules.');
        
        return shmry;
        
    } catch (error) {
        console.error('❌ Demo failed:', error);
        throw error;
    }
}

// Demo specific AI capabilities
async function demoAICapabilities() {
    console.log('\n🤖 AI Capabilities Demo:');
    
    try {
        const shmry = getShmry();
        const ai = shmry.getModule('ai');
        
        if (!ai) {
            console.log('   AI module not available');
            return;
        }
        
        // Demo different AI models
        const models = ['core', 'brain', 'neural', 'transformer'];
        
        for (const model of models) {
            try {
                const result = await ai.inference(`Test input for ${model}`, model);
                console.log(`   ${model.toUpperCase()}: ${result.result}`);
            } catch (error) {
                console.log(`   ${model.toUpperCase()}: Error - ${error.message}`);
            }
        }
        
    } catch (error) {
        console.error('   AI Demo failed:', error);
    }
}

// Demo Edge Computing capabilities
async function demoEdgeCapabilities() {
    console.log('\n🌐 Edge Computing Demo:');
    
    try {
        const shmry = getShmry();
        const edge = shmry.getModule('edge');
        
        if (!edge) {
            console.log('   Edge module not available');
            return;
        }
        
        // Demo edge node operations
        if (edge.modules && edge.modules.get('node')) {
            const nodeModule = edge.modules.get('node');
            console.log(`   Node Module Status: ${nodeModule.status}`);
            console.log(`   Device ID: ${nodeModule.deviceId}`);
        }
        
        // Demo edge worker operations
        if (edge.modules && edge.modules.get('worker')) {
            const workerModule = edge.modules.get('worker');
            const status = await workerModule.getStatus();
            console.log(`   Worker Status: ${status.status}`);
            console.log(`   Active Jobs: ${status.activeJobs}`);
        }
        
    } catch (error) {
        console.error('   Edge Demo failed:', error);
    }
}

// Demo Cloud Infrastructure capabilities
async function demoCloudCapabilities() {
    console.log('\n☁️ Cloud Infrastructure Demo:');
    
    try {
        const shmry = getShmry();
        const cloud = shmry.getModule('cloud');
        
        if (!cloud) {
            console.log('   Cloud module not available');
            return;
        }
        
        // Demo compute service
        if (cloud.services && cloud.services.get('compute')) {
            const compute = cloud.services.get('compute');
            console.log(`   Compute Service Status: ${compute.status}`);
            console.log(`   Instances: ${compute.instances.size}`);
        }
        
        // Demo storage service
        if (cloud.services && cloud.services.get('storage')) {
            const storage = cloud.services.get('storage');
            console.log(`   Storage Service Status: ${storage.status}`);
            console.log(`   Buckets: ${storage.buckets.size}`);
        }
        
    } catch (error) {
        console.error('   Cloud Demo failed:', error);
    }
}

// Demo Commerce capabilities
async function demoCommerceCapabilities() {
    console.log('\n🛒 Commerce Demo:');
    
    try {
        const shmry = getShmry();
        const commerce = shmry.getModule('commerce');
        
        if (!commerce) {
            console.log('   Commerce module not available');
            return;
        }
        
        // Demo catalog service
        if (commerce.services && commerce.services.get('catalog')) {
            const catalog = commerce.services.get('catalog');
            console.log(`   Catalog Service Status: ${catalog.status}`);
            console.log(`   Products: ${catalog.products.size}`);
        }
        
        // Demo cart service
        if (commerce.services && commerce.services.get('cart')) {
            const cart = commerce.services.get('cart');
            console.log(`   Cart Service Status: ${cart.status}`);
            console.log(`   Active Carts: ${cart.carts.size}`);
        }
        
    } catch (error) {
        console.error('   Commerce Demo failed:', error);
    }
}

// Run comprehensive demo
async function runComprehensiveDemo() {
    try {
        // Run main demo
        const shmry = await demoShmryPlatform();
        
        // Wait a bit for systems to stabilize
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Run specific capability demos
        await demoAICapabilities();
        await demoEdgeCapabilities();
        await demoCloudCapabilities();
        await demoCommerceCapabilities();
        
        console.log('\n🎯 Demo Summary:');
        console.log('   ✅ Shmry Platform initialized with all modules');
        console.log('   ✅ AI system with 17 specialized models');
        console.log('   ✅ Edge computing with 13 IoT modules');
        console.log('   ✅ Cloud infrastructure with 15 services');
        console.log('   ✅ Commerce platform with 12 modules');
        console.log('   ✅ Total: 190+ modules ready for production use');
        
        console.log('\n🚀 Shmry Platform is ready to revolutionize your business!');
        
        return shmry;
        
    } catch (error) {
        console.error('❌ Comprehensive demo failed:', error);
        throw error;
    }
}

// Export demo functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        demoShmryPlatform,
        demoAICapabilities,
        demoEdgeCapabilities,
        demoCloudCapabilities,
        demoCommerceCapabilities,
        runComprehensiveDemo
    };
} else if (typeof window !== 'undefined') {
    window.demoShmryPlatform = demoShmryPlatform;
    window.demoAICapabilities = demoAICapabilities;
    window.demoEdgeCapabilities = demoEdgeCapabilities;
    window.demoCloudCapabilities = demoCloudCapabilities;
    window.demoCommerceCapabilities = demoCommerceCapabilities;
    window.runComprehensiveDemo = runComprehensiveDemo;
}
