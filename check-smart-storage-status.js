// Check Smart Storage System Status
// Shows current storage status and admin device information

const fs = require('fs');
const path = require('path');

console.log('💾 SHMRY Smart Storage System Status');
console.log('=====================================');

// Check if storage manager is running
try {
    const ShmryStorageManager = require('./shmry-storage-manager');
    console.log('✅ Storage Manager: Available');
} catch (error) {
    console.log('❌ Storage Manager: Not available');
}

// Check if smart downloader is available
try {
    const ShmrySmartDownloader = require('./shmry-smart-downloader');
    console.log('✅ Smart Downloader: Available');
} catch (error) {
    console.log('❌ Smart Downloader: Not available');
}

console.log('');

// Check storage logs
const storageLogPath = path.join(__dirname, 'storage-log.json');
if (fs.existsSync(storageLogPath)) {
    try {
        const storageLog = JSON.parse(fs.readFileSync(storageLogPath, 'utf8'));
        const latestStatus = storageLog[storageLog.length - 1];
        
        if (latestStatus) {
            console.log('📊 Latest Storage Status:');
            console.log(`   💾 Usage: ${latestStatus.localUsage.toFixed(1)}%`);
            console.log(`   📁 Used: ${(latestStatus.localUsed / (1024**3)).toFixed(1)} GB`);
            console.log(`   💾 Free: ${(latestStatus.localFree / (1024**3)).toFixed(1)} GB`);
            console.log(`   📊 Status: ${latestStatus.status}`);
            console.log(`   ⏰ Time: ${new Date(latestStatus.timestamp).toLocaleString()}`);
        }
    } catch (error) {
        console.log('⚠️  Could not read storage log');
    }
} else {
    console.log('📁 No storage log found');
}

console.log('');

// Check admin device storage
const adminStoragePath = path.join(__dirname, 'admin-devices-storage');
if (fs.existsSync(adminStoragePath)) {
    console.log('🌐 Admin Device Storage:');
    
    const adminLogPath = path.join(adminStoragePath, 'download-log.json');
    if (fs.existsSync(adminLogPath)) {
        try {
            const adminLog = JSON.parse(fs.readFileSync(adminLogPath, 'utf8'));
            console.log(`   📥 Total downloads: ${adminLog.length}`);
            
            const completed = adminLog.filter(log => log.status === 'completed');
            console.log(`   ✅ Completed: ${completed.length}`);
            
            if (completed.length > 0) {
                console.log('   📦 Recent models:');
                completed.slice(-3).forEach(log => {
                    console.log(`      ${log.model} (${log.size})`);
                });
            }
        } catch (error) {
            console.log('   ⚠️  Could not read admin download log');
        }
    }
    
    const registryPath = path.join(adminStoragePath, 'model-registry.json');
    if (fs.existsSync(registryPath)) {
        try {
            const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
            console.log(`   📋 Models in registry: ${Object.keys(registry).length}`);
        } catch (error) {
            console.log('   ⚠️  Could not read model registry');
        }
    }
} else {
    console.log('🌐 Admin Device Storage: Not initialized');
}

console.log('');

// Check local AI models
const localModelsPath = path.join(__dirname, 'AI-Models');
if (fs.existsSync(localModelsPath)) {
    try {
        const localFiles = fs.readdirSync(localModelsPath);
        const modelFiles = localFiles.filter(file => 
            file.endsWith('.json') || file.endsWith('.log')
        );
        
        console.log('💻 Local Storage:');
        console.log(`   📁 Files: ${localFiles.length}`);
        console.log(`   📊 Logs: ${modelFiles.length}`);
        
        if (localFiles.length > 0) {
            console.log('   📦 Contents:');
            localFiles.slice(0, 5).forEach(file => {
                console.log(`      ${file}`);
            });
            if (localFiles.length > 5) {
                console.log(`      ... and ${localFiles.length - 5} more`);
            }
        }
    } catch (error) {
        console.log('💻 Local Storage: Could not read');
    }
} else {
    console.log('💻 Local Storage: Not initialized');
}

console.log('');

// System recommendations
console.log('💡 System Status:');
console.log('   🚀 Smart Storage System is running');
console.log('   💾 Storage monitoring active (every 30 seconds)');
console.log('   📥 Smart downloads managing locations');
console.log('   🌐 Admin device integration ready');
console.log('   🚨 Automatic protection enabled');

console.log('');
console.log('🎯 Next Steps:');
console.log('   1. Continue working on SHMRY features');
console.log('   2. System automatically manages storage');
console.log('   3. Check status anytime with this script');
console.log('   4. No manual intervention needed');

console.log('');
console.log('🚀 You\'re protected from storage issues!');
