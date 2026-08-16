# Shmry Edge Computing Device Management System

## Overview

Shmry's edge computing infrastructure is powered by two types of connected devices:

1. **Admin Devices** - Your static IP devices (10-15 devices) that serve as core infrastructure
2. **Subscriber Devices** - Volunteer edge computing partners who earn money by contributing resources

## 1. Admin Device Management

### Access URL
**https://www.shmry.com/admin/devices**

### Features
- **Device Registration**: Add new admin devices with specifications
- **Resource Monitoring**: Track computing power, memory, storage, and status
- **Integration Links**: Generate links for existing devices to connect automatically
- **Real-time Statistics**: Monitor total devices, online status, and resource utilization

### How to Add Your 10-15 Additional Devices

1. **Navigate to Admin Dashboard**: Visit `https://www.shmry.com/admin/devices`
2. **Add New Device**: Use the "Add New Admin Device" form
3. **Fill Device Details**:
   - Device Name (e.g., "Admin-Server-01")
   - Static IP Address
   - Device Type (Server, Workstation, NAS, GPU Server, Edge Node)
   - Computing Power (vCPU)
   - Memory (GB)
   - Storage (TB)
   - Location
   - Description

4. **Integration for Existing Devices**: Use the integration link provided:
   ```
   https://www.shmry.com/admin/integrate?token=ADMIN_DEVICE_TOKEN&type=static_ip
   ```

### Admin Device Benefits
- Full control over device allocation
- Priority task assignment
- Core infrastructure status
- Centralized management dashboard

## 2. Subscriber Device Management

### Access URL
**https://www.shmry.com/admin/subscribers**

### Features
- **Integration Options**: Two types of device integration
- **Revenue Tracking**: Monitor total subscribers and earnings
- **Link Generation**: Create integration links for subscribers

### Integration Options

#### Option 1: Full Device Surrender
- **URL**: `https://www.shmry.com/subscribe/surrender?token=FULL_SURRENDER_TOKEN&type=complete`
- **Benefits**:
  - Shmry manages device optimally
  - Maximum resource utilization
  - Higher revenue potential
  - Automated maintenance
  - Priority task allocation
  - 90% revenue sharing

#### Option 2: Customized Allocation
- **URL**: `https://www.shmry.com/subscribe/customize?token=CUSTOMIZED_TOKEN&type=flexible`
- **Benefits**:
  - Custom resource allocation
  - Flexible scheduling
  - Personal device control
  - Selective task acceptance
  - Manual maintenance control
  - 90% revenue sharing

## 3. Subscriber Device Integration

### Access URL
**https://www.shmry.com/subscribe/integrate**

### Features
- **Integration Selection**: Choose between full surrender or customized allocation
- **Device Setup Form**: Configure device specifications
- **Installation Steps**: Step-by-step setup instructions
- **Earnings Calculator**: Estimate monthly and yearly revenue

### Integration Process

1. **Choose Integration Type**:
   - Full Device Surrender (🔒)
   - Customized Allocation (⚙️)

2. **Device Configuration**:
   - Device Name
   - Device Type (Desktop, Laptop, Server, etc.)
   - Computing Power (vCPU)
   - Memory (GB)
   - Storage (TB)
   - Location
   - Expected Uptime

3. **Installation Steps**:
   - Download Shmry Agent
   - Install and Configure
   - Start Earning

4. **Earnings Calculation**:
   - Real-time earnings estimates
   - Monthly and yearly projections
   - Resource-based calculations

## 4. Revenue Sharing Model

### Structure
- **90% to Device Owners**: Direct revenue sharing
- **10% to Platform**: Covers costs, maintenance, and development

### Earnings Calculation
- **Computing**: $2.50 per vCPU per month
- **Memory**: $0.50 per GB per month
- **Storage**: $3.00 per TB per month
- **Uptime Multiplier**: Based on device availability

### Example Calculation
```
Device: 8 vCPU, 16 GB RAM, 1 TB Storage, 100% uptime
Monthly Earnings: (8 × $2.50) + (16 × $0.50) + (1 × $3.00) = $20 + $8 + $3 = $31.00
Yearly Earnings: $31.00 × 12 = $372.00
Device Owner Receives: $372.00 × 0.90 = $334.80
```

## 5. Technical Implementation

### Admin Dashboard
- **URL**: `/admin/devices`
- **Purpose**: Manage core infrastructure devices
- **Features**: Device registration, monitoring, integration

### Subscriber Management
- **URL**: `/admin/subscribers`
- **Purpose**: Monitor volunteer devices and revenue
- **Features**: Integration options, statistics, link generation

### Device Integration
- **URL**: `/subscribe/integrate`
- **Purpose**: Onboard new subscriber devices
- **Features**: Setup forms, installation guides, earnings calculator

## 6. Security and Authentication

### Admin Access
- Restricted to authorized administrators
- Device management capabilities
- Integration link generation

### Subscriber Access
- Public integration page
- Device setup and configuration
- Earnings calculation tools

## 7. Monitoring and Analytics

### Real-time Metrics
- Device status (online/offline)
- Resource utilization
- Revenue generation
- Network performance

### Dashboard Features
- Total device counts
- Online/offline status
- Computing and storage totals
- Revenue tracking

## 8. Next Steps

### For Admin Devices
1. Visit `https://www.shmry.com/admin/devices`
2. Add your 10-15 additional devices
3. Use integration links for existing devices
4. Monitor device status and performance

### For Subscriber Recruitment
1. Share integration links with potential volunteers
2. Direct them to `https://www.shmry.com/subscribe/integrate`
3. Monitor subscriber growth and revenue
4. Optimize integration process based on feedback

### For Platform Development
1. Implement real-time device monitoring
2. Add automated maintenance features
3. Develop advanced earnings algorithms
4. Create mobile applications for device management

## 9. Support and Documentation

### Admin Support
- Device integration assistance
- Performance optimization
- Troubleshooting guides

### Subscriber Support
- Setup assistance
- Earnings questions
- Technical support

### Platform Documentation
- API documentation
- Integration guides
- Best practices
- FAQ and troubleshooting

---

**Shmry Edge Computing Infrastructure** - Building the future of distributed computing, one device at a time.
