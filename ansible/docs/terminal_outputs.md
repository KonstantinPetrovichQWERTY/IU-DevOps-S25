# Terminal outputs


```bash
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible all -m ping
iu-devops-vm | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible all -i inventory/hosts.ini -m ping
Command 'nsible' not found, did you mean:
  command 'ansible' from deb ansible-core (2.12.0-1ubuntu0.1)
  command 'ansible' from deb ansible (2.10.7+merged+base+2.10.8+dfsg-1)
Try: sudo apt install <deb name>
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible all -i inventory/hosts.ini -m ping
iu-devops-vm | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible webservers -i inventory/hosts.ini -a "uptime"
iu-devops-vm | CHANGED | rc=0 >>
 20:27:19 up 16 min,  2 users,  load average: 0.00, 0.00, 0.00
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible all -m ping
iu-devops-vm | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible webservers -a "uname -a"
iu-devops-vm | CHANGED | rc=0 >>
Linux iu-devops-vm 5.15.0-170-generic #180-Ubuntu SMP Fri Jan 9 16:10:31 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
```


## Terminal output from FIRST provision.yml run
```bash
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible-playbook playbooks/provision.yml

PLAY [Provision web servers] ******************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [common : Update apt cache] **************************************************************************************************************************changed: [iu-devops-vm]

TASK [common : Install common packages] *******************************************************************************************************************changed: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************changed: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************changed: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************changed: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add user to docker group] ******************************************************************************************************************changed: [iu-devops-vm]

TASK [docker : Install Python Docker module] **************************************************************************************************************changed: [iu-devops-vm]

RUNNING HANDLER [docker : restart docker] *****************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=10   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

## Terminal output from SECOND provision.yml run

```bash
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible-playbook playbooks/provision.yml

PLAY [Provision web servers] ******************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [common : Update apt cache] **************************************************************************************************************************ok: [iu-devops-vm]

TASK [common : Install common packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add user to docker group] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Python Docker module] **************************************************************************************************************ok: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=9    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

## Terminal output from deploy.yml run
```bash
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible-playbook playbooks/deploy.yml --ask-vault-pass
Vault password: 

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [app_deploy : Log in to Docker Hub] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [app_deploy : Pull Docker image] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [app_deploy : Stop existing container (if running)] **************************************************************************************************[DEPRECATION WARNING]: The container_default_behavior option will change its default value from "compatibility" to "no_defaults" in community.general 
3.0.0. To remove this warning, please specify an explicit value for it now. This feature will be removed from community.general in version 3.0.0. 
Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
changed: [iu-devops-vm]

TASK [app_deploy : Remove old container (if exists)] ******************************************************************************************************changed: [iu-devops-vm]

TASK [app_deploy : Run new container] *********************************************************************************************************************changed: [iu-devops-vm]

TASK [app_deploy : Wait for application to be ready (port check)] *****************************************************************************************ok: [iu-devops-vm]

TASK [app_deploy : Verify health endpoint] ****************************************************************************************************************ok: [iu-devops-vm]

TASK [app_deploy : Display deployment status] *************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app deployed successfully!",
        "Container ID: 661efcc0612b",
        "Health check: 200 - {'status': 'healthy', 'timestamp': '2026-02-21T22:28:11.339297+00:00', 'uptime_seconds': 5}"
    ]
}

RUNNING HANDLER [app_deploy : restart app] ****************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=10   changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

## Container status: docker ps output
```bash
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible webservers -m shell -a "sudo docker ps -a" --ask-vault-password
Vault password: 
[WARNING]: Consider using 'become', 'become_method', and 'become_user' rather than running sudo
iu-devops-vm | CHANGED | rc=0 >>
CONTAINER ID   IMAGE                                      COMMAND                  CREATED         STATUS                     PORTS                    NAMES
29b8cfb54dd7   konstantinqwertin/devops-info-app:latest   "uvicorn app_python.…"   2 minutes ago   Up 2 minutes (unhealthy)   0.0.0.0:8000->8000/tcp   devops-info-app
```

