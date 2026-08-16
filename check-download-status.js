// Check Background Download Status
// Run this script to see the current status of AI model downloads

const fs = require('fs');
const path = require('path');

console.log('📊 SHMRY AI Model Download Status');
console.log('=====================================');

const downloadPath = path.join(__dirname, 'AI-Models');
const logPath = path.join(downloadPath, 'download-log.json');

if (fs.existsSync(logPath)) {
    try {
        const logData = JSON.parse(fs.readFileSync(logPath, 'utf8'));
        
        const totalDownloads = logData.length;
        const completedDownloads = logData.filter(log => log.status === 'completed').length;
        const failedDownloads = logData.filter(log => log.status === 'failed').length;
        
        console.log(`📥 Total Downloads: ${totalDownloads}`);
        console.log(`✅ Completed: ${completedDownloads}`);
        console.log(`❌ Failed: ${failedDownloads}`);
        console.log(`⏳ In Progress: ${totalDownloads - completedDownloads - failedDownloads}`);
        
        if (completedDownloads > 0) {
            console.log('\n🎉 Recently Completed Models:');
            const recent = logData
                .filter(log => log.status === 'completed')
                .slice(-5)
                .reverse();
            
            recent.forEach(log => {
                const timestamp = new Date(log.timestamp).toLocaleString();
                console.log(`   ${log.model} (${log.size}) - ${timestamp}`);
            });
        }
        
        if (failedDownloads > 0) {
            console.log('\n❌ Failed Downloads:');
            const failed = logData.filter(log => log.status === 'failed');
            failed.forEach(log => {
                console.log(`   ${log.model} (${log.size})`);
            });
        }
        
    } catch (error) {
        console.error('❌ Error reading download log:', error.message);
    }
} else {
    console.log('📁 No download log found. Downloads may not have started yet.');
}

console.log('\n💡 To start background downloads, run: node start-background-downloads.js');
console.log('🛑 To stop downloads, find the downloader process and stop it');
console.log('📱 Downloads run in background - you can continue working on SHMRY!');
