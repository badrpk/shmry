# 🚀 SHMRY Edge Computing Platform

**Production-Ready Hybrid Architecture: Vercel Frontend + Local Node.js Backend**

## 🏗️ **Architecture**

- **Frontend**: Vercel (www.shmry.com) - Fast global CDN
- **Backend**: Local Node.js servers (154.57.212.38) - Secure data control
- **Data**: Local storage for privacy and security

## 🚀 **Quick Start**

### **1. Start All Services**
```bash
.\start-shmry-production.bat
```

### **2. Deploy Frontend Updates**
```bash
.\deploy-vercel.bat
```

## 🌐 **Access URLs**

- **Live Website**: https://www.shmry.com
- **Local Website**: http://154.57.212.38:80
- **Admin Dashboard**: http://154.57.212.38:3001
- **Master Dashboard**: http://154.57.212.38:3002
- **Network Discovery**: http://154.57.212.38:3003

## 📁 **Essential Files**

- `website/shmry-website.html` - Main website
- `products/` - Product pages
- `admin-device-manager.html` - Admin interface
- `master-dashboard.html` - Master control panel
- `deployment/` - Node.js servers
- `vercel.json` - Vercel configuration
- `.vercel/` - Vercel project configuration (auto-generated)
- `security-config.js` - Security configuration
- `env.template` - Environment variables template
- `SECURITY_README.md` - Security implementation guide

## 🔧 **Production Commands**

- **Start Secure Services**: `.\start-secure-production.bat`
- **Start Legacy Services**: `.\start-shmry-production.bat`
- **Deploy Frontend**: `.\deploy-vercel.bat`
- **Check Status**: Visit local URLs above

## 🔐 **Security Features**

- **Admin services isolated** to localhost only
- **Rate limiting** and CORS protection
- **Security headers** and HSTS enabled
- **Environment validation** required
- **Credential management** via environment variables

## 📋 **Project Structure**

### **Vercel Integration**
- `.vercel/` - Contains Vercel project configuration
  - `project.json` - Project ID and organization ID
  - `README.txt` - Vercel folder explanation
- **Note**: `.vercel/` folder is auto-generated and should not be manually modified

### **Core Application**
- `website/` - Main website files
- `products/` - Product-specific pages
- `deployment/` - Node.js backend servers
- `*.html` - Standalone HTML pages

## ✨ **Features**

- AI-powered search system
- Custom @shmry.com email services
- Edge computing infrastructure
- Admin device management
- Network discovery
- Hybrid frontend/backend architecture

---

**SHMRY Technologies** | Built for the future of edge computing
