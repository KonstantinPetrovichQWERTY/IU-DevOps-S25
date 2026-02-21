# Lab 04: Infrastructure as Code with Terraform on Yandex Cloud

## 1. Cloud Provider & Infrastructure

### Cloud Provider Choice: Yandex Cloud

**Rationale for choosing Yandex Cloud:**
- **Free Tier Availability**: Yandex Cloud offers a generous free tier 
- **Regional Presence**: Data centers in Russia
- **Comprehensive Documentation**: Well-documented API and Terraform provider
- **Integration with Ecosystem**: Seamless integration with other Yandex services

### Instance Type and Configuration

**Instance Details:**
- **CPUs**: 2 
- **RAM**: 1GB
- **Core Fraction**: 20%
- **Disk**: 10GB HDD (network-hdd)
- **OS**: Ubuntu 20.04 LTS

**Why this configuration?**
Its free

### Region/Zone Selection

**Selected Zone: ru-central1-b**

### Cost Analysis

3 Russian rubles hourly

### Resources Created

The following infrastructure components were provisioned:

1. **VPC Network**
   - Name: `iu-devops-network`
   - Purpose: Isolated network environment for VM

2. **VPC Subnet**
   - Name: `iu-devops-subnet`
   - CIDR Block: `192.168.1.0/24`
   - Zone: `ru-central1-b`

3. **Security Group**
   - Name: `iu-devops-security-group`
   - Inbound Rules:
     - SSH (port 22) - Restricted to specific IP
     - HTTP (port 80) - Open to internet
     - Custom App (port 5000) - Open to internet
   - Outbound Rules: All traffic allowed

4. **Compute Instance (VM)**
   - Name: `iu-devops-vm`
   - OS: Ubuntu 20.04 LTS

## 2. Terraform Implementation

### Terraform Version Information

Terraform v1.10.5

### Key Configuration Decisions
1. Security First Approach

- SSH access restricted to specific IP address
- Security groups used instead of simpler firewall rules
- All sensitive values stored in variables

2. Free Tier Optimization

- Selected smallest instance type within free tier limits
- Used HDD instead of SSD to stay within free tier
- Configured `core_fraction` to 20% for CPU guarantee

3. Best Practices

- Proper tagging for resource identification
- Separate files for different concerns
- Descriptive resource naming conventions

### Terminal outputs

Check this [file](/terraform/docs/terminal_outputs.md)
