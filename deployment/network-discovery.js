const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const app = express();
const PORT = 3003;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Network discovery data
let discoveredDevices = [];
let linuxServer = null;

// ==================== NETWORK DISCOVERY ROUTES ====================

// Main network discovery page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../network-discovery.html'));
});

// API endpoint to scan network
app.get('/api/scan-network', (req, res) => {
    console.log('🔍 Scanning network for devices...');
    
    // Scan local network for devices
    scanNetwork()
        .then(devices => {
            discoveredDevices = devices;
            res.json({
                success: true,
                devices: devices,
                message: `Found ${devices.length} devices on network`
            });
        })
        .catch(error => {
            console.error('Network scan error:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        });
});

// API endpoint to connect to Linux server
app.post('/api/connect-linux', (req, res) => {
    const { ip, port = 22, username = 'shmry' } = req.body;
    
    if (!ip) {
        return res.status(400).json({
            success: false,
            error: 'IP address is required'
        });
    }
    
    console.log(`🔗 Attempting to connect to Linux server at ${ip}:${port}...`);
    
    // Test connection to Linux server
    testLinuxConnection(ip, port, username)
        .then(result => {
            linuxServer = {
                ip: ip,
                port: port,
                username: username,
                status: 'connected',
                lastSeen: new Date().toISOString(),
                capabilities: result.capabilities
            };
            
            res.json({
                success: true,
                server: linuxServer,
                message: 'Successfully connected to Linux server'
            });
        })
        .catch(error => {
            console.error('Linux connection error:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        });
});

// API endpoint to get network status
app.get('/api/network-status', (req, res) => {
    res.json({
        discoveredDevices: discoveredDevices,
        linuxServer: linuxServer,
        totalDevices: discoveredDevices.length + (linuxServer ? 1 : 0)
    });
});

// ==================== NETWORK FUNCTIONS ====================

// Scan local network for devices
function scanNetwork() {
    return new Promise((resolve, reject) => {
        // Get local IP address
        getLocalIP()
            .then(localIP => {
                const networkPrefix = localIP.substring(0, localIP.lastIndexOf('.'));
                console.log(`🔍 Scanning network: ${networkPrefix}.0/24`);
                
                const devices = [];
                
                // Scan common ports and IPs
                for (let i = 1; i <= 254; i++) {
                    const ip = `${networkPrefix}.${i}`;
                    
                    // Skip local IP
                    if (ip === localIP) {
                        devices.push({
                            ip: ip,
                            hostname: 'Local SHMRY Server',
                            type: 'Windows Server',
                            status: 'online',
                            ports: [3000, 3001, 3002, 3003],
                            services: ['Website', 'Admin', 'Master', 'Network Discovery']
                        });
                        continue;
                    }
                    
                    // Test common ports
                    testPort(ip, 22)  // SSH
                        .then(sshOpen => {
                            if (sshOpen) {
                                devices.push({
                                    ip: ip,
                                    hostname: `Device-${i}`,
                                    type: 'Linux Server',
                                    status: 'online',
                                    ports: [22],
                                    services: ['SSH']
                                });
                            }
                        });
                    
                    testPort(ip, 80)  // HTTP
                        .then(httpOpen => {
                            if (httpOpen) {
                                devices.push({
                                    ip: ip,
                                    hostname: `Web-${i}`,
                                    type: 'Web Server',
                                    status: 'online',
                                    ports: [80],
                                    services: ['HTTP']
                                });
                            }
                        });
                }
                
                // Wait a bit for scans to complete
                setTimeout(() => {
                    resolve(devices);
                }, 5000);
            })
            .catch(reject);
    });
}

// Get local IP address
function getLocalIP() {
    return new Promise((resolve, reject) => {
        const { networkInterfaces } = require('os');
        const nets = networkInterfaces();
        
        for (const name of Object.keys(nets)) {
            for (const net of nets[name]) {
                if (net.family === 'IPv4' && !net.internal) {
                    resolve(net.address);
                    return;
                }
            }
        }
        reject(new Error('No local IP found'));
    });
}

// Test if a port is open
function testPort(ip, port) {
    return new Promise((resolve) => {
        const net = require('net');
        const socket = new net.Socket();
        
        socket.setTimeout(1000);
        
        socket.on('connect', () => {
            socket.destroy();
            resolve(true);
        });
        
        socket.on('timeout', () => {
            socket.destroy();
            resolve(false);
        });
        
        socket.on('error', () => {
            socket.destroy();
            resolve(false);
        });
        
        socket.connect(port, ip);
    });
}

// Test connection to Linux server
function testLinuxConnection(ip, port, username) {
    return new Promise((resolve, reject) => {
        // For now, simulate connection test
        // In production, you'd use SSH or other protocols
        
        setTimeout(() => {
            if (Math.random() > 0.1) { // 90% success rate for demo
                resolve({
                    capabilities: {
                        cpu: '8 cores',
                        memory: '16GB RAM',
                        storage: '1TB SSD',
                        os: 'Ubuntu 22.04 LTS',
                        services: ['SSH', 'Docker', 'Node.js', 'Python'],
                        aiModels: ['GPT-3', 'Llama-2', 'Mistral'],
                        status: 'ready'
                    }
                });
            } else {
                reject(new Error('Connection failed - server may be offline'));
            }
        }, 2000);
    });
}

// Start server
app.listen(PORT, () => {
    console.log('🔍 SHMRY Network Discovery Server is running!');
    console.log(`🔍 Server URL: http://localhost:${PORT}`);
    console.log('📱 Available endpoints:');
    console.log(`   • Network Discovery: http://localhost:${PORT}/`);
    console.log(`   • Scan Network: http://localhost:${PORT}/api/scan-network`);
    console.log(`   • Network Status: http://localhost:${PORT}/api/network-status`);
    console.log('');
    console.log('Press Ctrl+C to stop the server');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down SHMRY Network Discovery Server...');
    process.exit(0);
});
