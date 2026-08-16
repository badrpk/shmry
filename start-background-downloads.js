// Start Background AI Model Downloads
// Run this script to start downloading additional AI models in the background

const ShmryModelDownloader = require('./shmry-model-downloader');

console.log('🚀 Starting SHMRY AI Model Background Downloader...');
console.log('💡 This will download additional AI models while you work on other features');
console.log('📱 Downloads will run in the background - you can continue working!');
console.log('');

const downloader = new ShmryModelDownloader();

// Start background downloads
downloader.startBackgroundDownloads();

// Keep the process running
console.log('✅ Background downloader started successfully!');
console.log('💡 You can now work on other SHMRY features');
console.log('📊 Download status will be reported every minute');
console.log('🛑 Press Ctrl+C to stop the downloader');
console.log('');

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Stopping background downloader...');
    downloader.stopDownloads();
    console.log('✅ Downloader stopped. Progress saved.');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Received SIGTERM, stopping downloader...');
    downloader.stopDownloads();
    console.log('✅ Downloader stopped. Progress saved.');
    process.exit(0);
});
