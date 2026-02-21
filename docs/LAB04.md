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
     - Custom App (port 8000) - Open to internet
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

## 3. Pulumi Implementation

### Pulumi version and language used

python 3.12
pulumi v3.223.0

## How code differs from Terraform

1. Programming Language vs DSL

- `Terraform`: Uses HCL (HashiCorp Configuration Language) - declarative, domain-specific
- `Pulumi`: Uses general-purpose languages (Python) - full programming capabilities

2. Resource Declaration

- `Terraform`: resource "yandex_vpc_network" "network" { ... }
- `Pulumi`: network = VpcNetwork("network", ...) - object-oriented approach

3. Configuration Management

- `Terraform`: Separate variables.tf and terraform.tfvars files
- `Pulumi`: Unified Config object with stack-specific config files

4. Documentation

- `Terraform`: comprehansive docs
- `Pulumi`: for yandex case is [github repo](https://github.com/pulumi/pulumi-yandex/blob/master/sdk/python/pulumi_yandex/vpc_network.py)

## Advantages you discovered

- Familiar Programming Constructs
- Stronger Type Checking 

### Terminal outputs

Check this [file](/terraform/docs/terminal_outputs.md)

## 4. Terraform vs Pulumi Comparison

### Ease of Learning: Which was easier to learn and why?

Pulumi was easier to learn because I could use familiar Python syntax instead of learning HCL from scratch. The ability to leverage existing programming knowledge made the learning curve much gentler compared to Terraform's domain-specific language.


### Code Readability: Which is more readable for you?

Terraform is more readable for infrastructure-only code due to its declarative nature and clean HCL syntax. However, Pulumi becomes more readable when implementing complex logic that would require awkward workarounds in Terraform.

### Debugging: Which was easier to debug when things went wrong?

Pulumi was easier to debug because Python provides meaningful error messages with stack traces, while Terraform errors can be cryptic. The ability to use print statements and standard Python debugging tools made troubleshooting significantly faster.

### Documentation: Which has better docs and examples?

Terraform has better documentation with more comprehensive examples, community resources, and mature provider documentation. Pulumi's docs are good but smaller in scope, often requiring more trial and error to find correct syntax.

### Use Case: When would you use Terraform? When Pulumi?

Use Terraform for pure infrastructure provisioning in multi-cloud environments with teams already familiar with HCL. Use Pulumi when infrastructure code needs complex logic, when working with developers who know general-purpose languages, or when building reusable infrastructure libraries.


## 5. Lab 5 Preparation & Cleanup

### Are you keeping your VM for Lab 5? (Yes/No)

Yes

### If yes: Which VM (Terraform or Pulumi created)?

Terraform

### Cleanup Status

Check this [file](/terraform/docs/terminal_outputs.md)
