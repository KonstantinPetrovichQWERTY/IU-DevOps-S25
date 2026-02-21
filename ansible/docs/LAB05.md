# Lab 05

## 1. Architecture Overview

### Ansible version used
ansible 2.10.8

### Target VM OS and version
Ubuntu 22.04

### Structure

```text
ansible/
├── inventory/
│   └── hosts.ini              # Static inventory
├── roles/
│   ├── common/                # Common system tasks
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   └── defaults/
│   │       └── main.yml
│   ├── docker/                # Docker installation
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   └── defaults/
│   │       └── main.yml
│   └── app_deploy/            # Application deployment
│       ├── tasks/
│       │   └── main.yml
│       ├── handlers/
│       │   └── main.yml
│       └── defaults/
│           └── main.yml
├── playbooks/
│   ├── site.yml               # Main playbook
│   ├── provision.yml          # System provisioning
│   └── deploy.yml             # App deployment
├── group_vars/
│   └── all.yml               # Encrypted variables (Vault)
├── ansible.cfg               # Ansible configuration
└── docs/
    └── LAB05.md              # Your documentation
```

## 2. Roles Documentation

### Common Role
**Purpose**: 
- Sets up the base system with essential packages and configurations required by all servers.

**Variables**:
- `common_packages`: List of essential packages (python3-pip, curl, git, vim, htop, etc.)

**Handlers**: None

**Dependencies**: None

### Docker Role
**Purpose**: 

- Installs and configures Docker CE on the target system, adds user to docker group.

**Variables**:

- docker_user: User to add to docker group (default: ubuntu)

**Handlers**:

- restart docker: Restarts Docker service when configuration changes

**Dependencies**: 

- Common role (implicitly, for prerequisites)

### App_Deploy Role
**Purpose**: Deploys the containerized Python application from Docker Hub.

**Variables**:

- app_port: Container port (8000)

- app_host_port: Host port (8000)

- app_restart_policy: Container restart policy (unless-stopped)

- app_environment: Environment variables for the app

- health_check_timeout: Timeout for health checks (60s)

**Handlers**:

- restart application: Restarts the application container

**Dependencies**: 

- Docker role


## 3. Idempotency Demonstration

### Terminal outputs 
Check this [file](/ansible/docs/terminal_outputs.md)

### Analysis: What changed first time? What didn't change second time?

First run changes: All system modifications occurred - apt cache updated, packages installed, Docker configured, user added to group.

Second run changes: No changes needed because all desired states were already achieved.


### Explanation: What makes your roles idempotent?

- Stateful modules (apt, service, user) check current state before making changes
- Conditional execution based on facts and register variables
- Handlers only trigger when notified by actual changes
- Declarative syntax describes desired state, not procedural steps

## 4. Ansible Vault Usage
### How Credentials Are Stored Securely:

```bash
$ ansible-vault create group_vars/all.yml
New Vault password: 
Confirm New Vault password: 
```

### Encrypted File Content (showing encryption):

```bash
$ANSIBLE_VAULT;1.1;AES256
306132393365653333303039393966313165623537...
```
(encrypted content, not human-readable)

### Why Ansible Vault Is Important:
Ansible Vault encrypts sensitive data like passwords, API keys, and certificates so they can be safely stored in version control. Without it, secrets would be exposed in plaintext, creating severe security vulnerabilities. Vault ensures that only authorized users with the password can decrypt and use these secrets during deployment.

## 6. Key Decisions
### Why use roles instead of plain playbooks?
Roles provide modular organization with clear separation of concerns, making the codebase maintainable and reusable. Each role encapsulates specific functionality (common setup, Docker, app deployment) with its own tasks, variables, and handlers.

## How do roles improve reusability?
Roles can be easily shared across different playbooks and projects by simply including them in the playbook's roles section. They also support parameterization through variables, allowing the same role to behave differently in various environments.

## What makes a task idempotent?
A task is idempotent when it checks the current state before making changes and only acts when the desired state differs from the current state. This ensures that running the task multiple times produces the same result without unintended side effects.

## How do handlers improve efficiency?
Handlers run only when notified by tasks that actually made changes, preventing unnecessary service restarts. They also run only once at the end of the play, even if notified multiple times, avoiding redundant operations.

## Why is Ansible Vault necessary?
Ansible Vault is essential for securely managing secrets in infrastructure-as-code. It allows sensitive data like passwords and API keys to be encrypted in version control, preventing credential exposure while maintaining automation capabilities.
