// Start Smart Storage Management System
// Manages storage and automatically redirects downloads to admin devices

const ShmryStorageManager = require('./shmry-storage-manager');
const ShmrySmartDownloader = require('./shmry-smart-downloader');

console.log('🚀 Starting SHMRY Smart Storage Management System...');
console.log('💡 This system automatically manages storage and redirects downloads');
console.log('🌐 Uses admin devices when local storage gets low');
console.log('');

// Initialize storage manager
console.log('💾 Initializing Storage Manager...');
const storageManager = new ShmryStorageManager();

// Initialize smart downloader
console.log('📥 Initializing Smart Downloader...');
const smartDownloader = new ShmrySmartDownloader();

console.log('');
console.log('✅ Smart Storage Management System started successfully!');
console.log('💡 Features:');
console.log('   📊 Continuous storage monitoring (every 30 seconds)');
console.log('   🚨 Automatic warnings at 70% and 80% storage usage');
console.log('   🔄 Smart download location selection');
console.log('   📦 Automatic model relocation to admin devices');
console.log('   🌐 Admin device discovery and management');
console.log('   🧹 Emergency cleanup when needed');
console.log('');

// Set up periodic status reports
setInterval(() => {
    console.log('\n📊 SYSTEM STATUS UPDATE');
    console.log('========================');
    
    // Storage status
    const storageStats = storageManager.getStorageStats();
    if (storageStats.currentUsage) {
        console.log(`💾 Storage: ${storageStats.currentUsage.localUsage.toFixed(1)}% used`);
        console.log(`📊 Status: ${storageStats.currentUsage.status}`);
    }
    
    // Download status
    const downloadStats = smartDownloader.getDownloadStats();
    console.log(`📥 Downloads: ${downloadStats.activeDownloads} active, ${downloadStats.completedDownloads} completed`);
    console.log(`📍 Locations: ${downloadStats.localDownloads} local, ${downloadStats.adminDownloads} admin`);
    
    // Admin devices
    if (storageStats.adminDevices.length > 0) {
        console.log(`🌐 Admin Devices: ${storageStats.adminDevices.filter(d => d.status === 'online').length} online`);
    }
    
    console.log('========================');
}, 120000); // Every 2 minutes

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down Smart Storage Management System...');
    console.log('💾 Saving all logs and configurations...');
    console.log('✅ System shutdown complete');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Received SIGTERM, shutting down...');
    console.log('✅ System shutdown complete');
    process.exit(0);
});

console.log('🛑 Press Ctrl+C to stop the system');
console.log('💡 The system will continue running in the background');
console.log('📱 You can work on other SHMRY features while it manages storage');
console.log('');

// Keep the process running
console.log('🚀 System is now running and monitoring storage...');
