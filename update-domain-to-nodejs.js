const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const VERCEL_TOKEN = process.env.VERCEL_TOKEN;
const PROJECT_ID = 'shmry-edge-computing';
const DOMAIN = 'www.shmry.com';
const TARGET_IP = '154.57.212.38';

console.log('🚀 SHMRY Domain Update Script');
console.log('==============================');
console.log(`Domain: ${DOMAIN}`);
console.log(`Target IP: ${TARGET_IP}`);
console.log(`Project: ${PROJECT_ID}`);
console.log('');

// Check if Vercel token is available
if (!VERCEL_TOKEN) {
    console.log('❌ VERCEL_TOKEN environment variable not set');
    console.log('');
    console.log('To set it up:');
    console.log('1. Go to https://vercel.com/account/tokens');
    console.log('2. Create a new token');
    console.log('3. Set environment variable: set VERCEL_TOKEN=your_token_here');
    console.log('');
    console.log('Or run: vercel login');
    process.exit(1);
}

// Function to make HTTPS request
function makeRequest(options, data = null) {
    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let responseData = '';
            
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(responseData);
                    resolve({ status: res.statusCode, data: parsed });
                } catch (e) {
                    resolve({ status: res.statusCode, data: responseData });
                }
            });
        });
        
        req.on('error', (error) => {
            reject(error);
        });
        
        if (data) {
            req.write(JSON.stringify(data));
        }
        
        req.end();
    });
}

// Function to get project domains
async function getProjectDomains() {
    console.log('📡 Fetching current domain configuration...');
    
    const options = {
        hostname: 'api.vercel.com',
        path: `/v9/projects/${PROJECT_ID}/domains`,
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${VERCEL_TOKEN}`,
            'Content-Type': 'application/json'
        }
    };
    
    try {
        const response = await makeRequest(options);
        console.log(`✅ Domain status: ${response.status}`);
        
        if (response.status === 200) {
            const domains = response.data;
            const targetDomain = domains.find(d => d.name === DOMAIN);
            
            if (targetDomain) {
                console.log(`📍 Current domain status: ${targetDomain.status}`);
                console.log(`📍 Current verification: ${targetDomain.verification?.status || 'N/A'}`);
                return targetDomain;
            } else {
                console.log(`❌ Domain ${DOMAIN} not found in project`);
                return null;
            }
        } else {
            console.log(`❌ Failed to fetch domains: ${response.status}`);
            console.log(response.data);
            return null;
        }
    } catch (error) {
        console.log(`❌ Error fetching domains: ${error.message}`);
        return null;
    }
}

// Function to update domain configuration
async function updateDomainConfiguration() {
    console.log('');
    console.log('🔄 Updating domain configuration...');
    
    // First, we need to remove the current domain from Vercel
    console.log('🗑️ Removing domain from Vercel...');
    
    const removeOptions = {
        hostname: 'api.vercel.com',
        path: `/v9/projects/${PROJECT_ID}/domains/${DOMAIN}`,
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${VERCEL_TOKEN}`,
            'Content-Type': 'application/json'
        }
    };
    
    try {
        const removeResponse = await makeRequest(removeOptions);
        console.log(`✅ Domain removal status: ${removeResponse.status}`);
        
        if (removeResponse.status === 200 || removeResponse.status === 404) {
            console.log('✅ Domain removed from Vercel successfully');
        } else {
            console.log(`⚠️ Domain removal response: ${removeResponse.status}`);
        }
    } catch (error) {
        console.log(`⚠️ Error removing domain: ${error.message}`);
    }
    
    console.log('');
    console.log('🎯 Next Steps:');
    console.log('===============');
    console.log('1. Go to your domain registrar (where you bought www.shmry.com)');
    console.log('2. Update DNS settings:');
    console.log(`   • Type: A Record`);
    console.log(`   • Name: www`);
    console.log(`   • Value: ${TARGET_IP}`);
    console.log(`   • TTL: 300 (or default)`);
    console.log('');
    console.log('3. Wait for DNS propagation (5-30 minutes)');
    console.log('');
    console.log('4. Test your domain:');
    console.log(`   • Main Website: http://${DOMAIN} (port 80)`);
    console.log(`   • Admin Dashboard: http://${DOMAIN}:3001`);
    console.log(`   • Master Dashboard: http://${DOMAIN}:3002`);
    console.log(`   • Network Discovery: http://${DOMAIN}:3003`);
    console.log('');
    console.log('✅ Your Node.js server will then be accessible via www.shmry.com!');
}

// Main execution
async function main() {
    try {
        const currentDomain = await getProjectDomains();
        
        if (currentDomain) {
            console.log('');
            console.log('📋 Current Domain Information:');
            console.log(`   Name: ${currentDomain.name}`);
            console.log(`   Status: ${currentDomain.status}`);
            console.log(`   Created: ${currentDomain.createdAt}`);
            console.log(`   Updated: ${currentDomain.updatedAt}`);
        }
        
        await updateDomainConfiguration();
        
    } catch (error) {
        console.log(`❌ Script execution failed: ${error.message}`);
        process.exit(1);
    }
}

// Run the script
main();
