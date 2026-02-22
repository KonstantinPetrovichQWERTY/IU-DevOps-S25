# Terminal outputs


```bash
$ ansible all -m ping
iu-devops-vm | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

$ ansible all -i inventory/hosts.ini -m ping
Command 'nsible' not found, did you mean:
  command 'ansible' from deb ansible-core (2.12.0-1ubuntu0.1)
  command 'ansible' from deb ansible (2.10.7+merged+base+2.10.8+dfsg-1)
Try: sudo apt install <deb name>
$ ansible all -i inventory/hosts.ini -m ping
iu-devops-vm | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

$ ansible webservers -i inventory/hosts.ini -a "uptime"
iu-devops-vm | CHANGED | rc=0 >>
 20:27:19 up 16 min,  2 users,  load average: 0.00, 0.00, 0.00
$ ansible all -m ping
iu-devops-vm | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

$ ansible webservers -a "uname -a"
iu-devops-vm | CHANGED | rc=0 >>
Linux iu-devops-vm 5.15.0-170-generic #180-Ubuntu SMP Fri Jan 9 16:10:31 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
```


## Terminal output from FIRST provision.yml run
```bash
$ ansible-playbook playbooks/provision.yml

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
$ ansible-playbook playbooks/provision.yml

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
$ ansible-playbook playbooks/deploy.yml --ask-vault-pass
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
$ ansible webservers -m shell -a "sudo docker ps -a" --ask-vault-password
Vault password: 
[WARNING]: Consider using 'become', 'become_method', and 'become_user' rather than running sudo
iu-devops-vm | CHANGED | rc=0 >>
CONTAINER ID   IMAGE                                      COMMAND                  CREATED         STATUS                     PORTS                    NAMES
29b8cfb54dd7   konstantinqwertin/devops-info-app:latest   "uvicorn app_python.…"   2 minutes ago   Up 2 minutes (unhealthy)   0.0.0.0:8000->8000/tcp   devops-info-app
```

## Application

![app](/ansible/docs/screenshots/application.png)


## ansible-playbook playbooks/provision.yml --tags "docker"

```bash
$ ansible-playbook playbooks/provision.yml --tags "docker"

PLAY [Provision web servers] ******************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Verify Docker is running] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Display Docker version] ********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": "Docker installed: Docker version 29.2.1, build a5c7197"
}

TASK [docker : Add user to docker group] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Python Docker module] **************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Log Docker configuration status] ***********************************************************************************************************skipping: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=9    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

```

## ansible-playbook playbooks/provision.yml --skip-tags "common"

```bash
$ ansible-playbook playbooks/provision.yml --skip-tags "common"

PLAY [Provision web servers] ******************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Verify Docker is running] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Display Docker version] ********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": "Docker installed: Docker version 29.2.1, build a5c7197"
}

TASK [docker : Add user to docker group] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Python Docker module] **************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Log Docker configuration status] ***********************************************************************************************************skipping: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=9    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0  
```

## ansible-playbook playbooks/provision.yml --tags "packages"

```bash
$ ansible-playbook playbooks/provision.yml --tags "packages"

PLAY [Provision web servers] ******************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [common : Update apt cache] **************************************************************************************************************************ok: [iu-devops-vm]

TASK [common : Install common packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [common : Log package installation completion] *******************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

## ansible-playbook playbooks/provision.yml --tags "docker" --check

Skipped verification tasks due to the `--check` mode that does not run tasks.

```bash
$ ansible-playbook playbooks/provision.yml --tags "docker" --check

PLAY [Provision web servers] ******************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Verify Docker is running] ******************************************************************************************************************skipping: [iu-devops-vm]

TASK [docker : Display Docker version] ********************************************************************************************************************skipping: [iu-devops-vm]

TASK [docker : Add user to docker group] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Python Docker module] **************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Log Docker configuration status] ***********************************************************************************************************skipping: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=7    changed=0    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0 
```

## ansible-playbook playbooks/provision.yml --tags "docker_install"

```bash
$ ansible-playbook playbooks/provision.yml --tags "docker_install"

PLAY [Provision web servers] ******************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Verify Docker is running] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Display Docker version] ********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": "Docker installed: Docker version 29.2.1, build a5c7197"
}

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## ansible-playbook playbooks/deploy.yml --ask-vault-pass (after app_* -> web_app_* prefix change)

```bash 
$ ansible-vault create group_vars/all.yml
New Vault password: 
[2]+  Stopped                 ansible-vault create group_vars/all.yml
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible-vault decrypt group_vars/all.yml
Vault password: 
Decryption successful
serg@LAPTOP-2BCVD7LH:/mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible$ ansible-playbook playbooks/deploy.yml --ask-vault-pass
Vault password: 

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Log in to Docker Hub] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Pull Docker image] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Stop existing container (if running)] *****************************************************************************************************[DEPRECATION WARNING]: The container_default_behavior option will change its default value from "compatibility" to "no_defaults" in community.general 
3.0.0. To remove this warning, please specify an explicit value for it now. This feature will be removed from community.general in version 3.0.0. 
Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
changed: [iu-devops-vm]

TASK [web_app : Remove old container (if exists)] *********************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Run new container] ************************************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Wait for application to be ready (port check)] ********************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Verify health endpoint] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Display deployment status] ****************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app deployed successfully!",
        "Container ID: 76d4518c7320",
        "Health check: 200 - {'status': 'healthy', 'timestamp': '2026-02-22T10:14:07.557538+00:00', 'uptime_seconds': 5}"
    ]
}

RUNNING HANDLER [web_app : restart app] *******************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=10   changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

## ansible-playbook playbooks/deploy.yml (Full deploy with docker compose)

```bash
$ ansible-playbook playbooks/deploy.yml

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Verify Docker is running] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Display Docker version] ********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": "Docker installed: Docker version 29.2.1, build a5c7197"
}

TASK [docker : Add user to docker group] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Python Docker module] **************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Log Docker configuration status] ***********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Create application directory] *************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Check if Docker Hub login is needed] ******************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Log in to Docker Hub (if needed)] *********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Template docker-compose.yml file] *********************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Check if containers need update] **********************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Deploy with Docker Compose (if needed)] ***************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Get compose status] ***********************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Wait for application to be ready] *********************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Verify health endpoint] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Display deployment status] ****************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app deployed successfully with Docker Compose!",
        "Project directory: /opt/devops-info-app",
        "Services:",
        "  - devops-info-app:latest",
        "  - Port: 8000:8000",
        "Health check: 200"
    ]
}

TASK [web_app : Display no-change status] *****************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Log deployment attempt] *******************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=19   changed=3    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0   
```

## ansible-playbook playbooks/deploy.yml (Secound full deploy with docker compose)

```bash
$ ansible-playbook playbooks/deploy.yml

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Verify Docker is running] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Display Docker version] ********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": "Docker installed: Docker version 29.2.1, build a5c7197"
}

TASK [docker : Add user to docker group] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Python Docker module] **************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Log Docker configuration status] ***********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Create application directory] *************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Check if Docker Hub login is needed] ******************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Log in to Docker Hub (if needed)] *********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Template docker-compose.yml file] *********************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Check if containers need update] **********************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Deploy with Docker Compose (if needed)] ***************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Get compose status] ***********************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Wait for application to be ready] *********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Verify health endpoint] *******************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Display deployment status] ****************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Display no-change status] *****************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app is already up to date!",
        "No deployment changes needed."
    ]
}

TASK [web_app : Log deployment attempt] *******************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=16   changed=1    unreachable=0    failed=0    skipped=6    rescued=0    ignored=0   
```

## Application running and accessible

```bash
ubuntu@iu-devops-vm:/opt/devops-info-app$ docker ps -a
CONTAINER ID   IMAGE                                      COMMAND                  CREATED         STATUS         PORTS
     NAMES
4bb1b0a3690b   konstantinqwertin/devops-info-app:latest   "uvicorn app_python.…"   2 minutes ago   Up 2 minutes   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   devops-info-app
ubuntu@iu-devops-vm:/opt/devops-info-app$ docker-compose -f /opt/devops-app/docker-compose.yml ps
ERROR: .FileNotFoundError: [Errno 2] No such file or directory: '/opt/devops-app/docker-compose.yml'
ubuntu@iu-devops-vm:/opt/devops-info-app$ docker-compose -f /opt/devops-info-app/docker-compose.yml ps
     Name                    Command               State                    Ports
---------------------------------------------------------------------------------------------------
devops-info-app   uvicorn app_python.app:app ...   Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp
ubuntu@iu-devops-vm:/opt/devops-info-app$ curl http://localhost:8000
{"service":{"name":"devops-info-service","version":"1.0.0","description":"DevOps course info service","framework":"FastApi"},"system":{"hostname":"4bb1b0a3690b","platform":"Linux","platform_version":"#180-Ubuntu SMP Fri Jan 9 16:10:31 UTC 2026","architecture":"x86_64","cpu_count":2,"python_version":"3.12.12"},"runtime":{"uptime_seconds":190,"uptime_human":"0 hours, 3 minutes","current_time":"2026-02-22T12:09:34.833037+00:00","timezone":"UTC"},"request":{"client_ip":"172.18.0.1","user_agent":"curl/7.81.0","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Service information"},{"path":"/health","method":"GET","description":"Health check"}]}
```

## Contents of templated docker-compose.yml

```bash
ubuntu@iu-devops-vm:/opt/devops-info-app$ cat docker-compose.yml 
version: '3.8'

services:
  devops-info-app:
    image: konstantinqwertin/devops-info-app:latest
    container_name: devops-info-app
    restart: unless-stopped
    ports:
      - "8000:8000"
```

## Scenario 1: Normal deployment (wipe should NOT run)

```bash
$ ansible-playbook playbooks/deploy.yml --skip-tags "docker"

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Include wipe tasks] ***********************************************************************************************************************included: /mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible/roles/web_app/tasks/wipe.yml for iu-devops-vm

TASK [web_app : Check if application directory exists] ****************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Stop and remove containers with Docker Compose] *******************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove docker-compose.yml file] ***********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove application directory] *************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : List Docker images for the application] ***************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove Docker images] *********************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Log wipe completion] **********************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Write wipe to log file] *******************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Create application directory] *************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Check if Docker Hub login is needed] ******************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Log in to Docker Hub (if needed)] *********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Template docker-compose.yml file] *********************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Check if containers need update] **********************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Deploy with Docker Compose (if needed)] ***************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Get compose status] ***********************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Wait for application to be ready] *********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Verify health endpoint] *******************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Display deployment status] ****************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Display no-change status] *****************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app is already up to date!",
        "No deployment changes needed."
    ]
}

TASK [web_app : Log deployment attempt] *******************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=9    changed=1    unreachable=0    failed=0    skipped=13   rescued=0    ignored=0```
```

```bash
$ docker ps -a
CONTAINER ID   IMAGE                                      COMMAND                  CREATED         STATUS         PORTS
     NAMES
8efa839d1690   konstantinqwertin/devops-info-app:latest   "uvicorn app_python.…"   3 minutes ago   Up 3 minutes   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   devops-info-app
```

## Scenario 2: Wipe only (remove existing deployment)

```bash
$ ansible-playbook playbooks/deploy.yml   -e "web_app_wipe=true"   --tags web_app_wipe

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Include wipe tasks] ***********************************************************************************************************************included: /mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible/roles/web_app/tasks/wipe.yml for iu-devops-vm

TASK [web_app : Check if application directory exists] ****************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Stop and remove containers with Docker Compose] *******************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Remove docker-compose.yml file] ***********************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Remove application directory] *************************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : List Docker images for the application] ***************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove Docker images] *********************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Log wipe completion] **********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app wiped successfully",
        "Directory removed: /opt/devops-info-app",
        "Containers stopped: Yes",
        "Images removed: No"
    ]
}

TASK [web_app : Write wipe to log file] *******************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=8    changed=4    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0  
```

```bash
ubuntu@iu-devops-vm:/$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

ubuntu@iu-devops-vm:/$ ls /opt
containerd
```


## Scenario 3: Clean reinstallation (wipe → deploy)

```bash
$ ansible-playbook playbooks/deploy.yml \
>   -e "web_app_wipe=true"

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************
ok: [iu-devops-vm]

TASK [docker : Add Docker GPG key] ************************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Add Docker repository] *********************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Docker packages] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Ensure Docker service is running and enabled] **********************************************************************************************ok: [iu-devops-vm]

TASK [docker : Verify Docker is running] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Display Docker version] ********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": "Docker installed: Docker version 29.2.1, build a5c7197"
}

TASK [docker : Add user to docker group] ******************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Install Python Docker module] **************************************************************************************************************ok: [iu-devops-vm]

TASK [docker : Log Docker configuration status] ***********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Include wipe tasks] ***********************************************************************************************************************included: /mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible/roles/web_app/tasks/wipe.yml for iu-devops-vm

TASK [web_app : Check if application directory exists] ****************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Stop and remove containers with Docker Compose] *******************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove docker-compose.yml file] ***********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove application directory] *************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : List Docker images for the application] ***************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove Docker images] *********************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Log wipe completion] **********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app wiped successfully",
        "Directory removed: /opt/devops-info-app",
        "Containers stopped: N/A",
        "Images removed: No"
    ]
}

TASK [web_app : Write wipe to log file] *******************************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Create application directory] *************************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Check if Docker Hub login is needed] ******************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Log in to Docker Hub (if needed)] *********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Template docker-compose.yml file] *********************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Check if containers need update] **********************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Deploy with Docker Compose (if needed)] ***************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Get compose status] ***********************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Wait for application to be ready] *********************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Verify health endpoint] *******************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Display deployment status] ****************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app deployed successfully with Docker Compose!",
        "Project directory: /opt/devops-info-app",
        "Services:",
        "  - devops-info-app:latest",
        "  - Port: 8000:8000",
        "Health check: 200"
    ]
}

TASK [web_app : Display no-change status] *****************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Log deployment attempt] *******************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=23   changed=6    unreachable=0    failed=0    skipped=8    rescued=0    ignored=0 
```

```bash
ubuntu@iu-devops-vm:/$ docker ps -a
CONTAINER ID   IMAGE                                      COMMAND                  CREATED          STATUS          PORTS
       NAMES
73fcf660f677   konstantinqwertin/devops-info-app:latest   "uvicorn app_python.…"   27 seconds ago   Up 27 seconds   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   devops-info-app

ubuntu@iu-devops-vm:/$ curl http://localhost:8000
{"service":{"name":"devops-info-service","version":"1.0.0","description":"DevOps course info service","framework":"FastApi"},"system":{"hostname":"c40402d9e8e1","platform":"Linux","platform_version":"#180-Ubuntu SMP Fri Jan 9 16:10:31 UTC 2026","architecture":"x86_64","cpu_count":2,"python_version":"3.12.12"},"runtime":{"uptime_seconds":11,"uptime_human":"0 hours, 0 minutes","current_time":"2026-02-22T12:40:04.473259+00:00","timezone":"UTC"},"request":{"client_ip":"172.18.0.1","user_agent":"curl/7.81.0","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Service information"},{"path":"/health","method":"GET","description":"Health check"}]}
```

## Scenario 4: Safety checks (should NOT wipe)

```bash
$ ansible-playbook playbooks/deploy.yml --tags web_app_wipe

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Include wipe tasks] ***********************************************************************************************************************included: /mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible/roles/web_app/tasks/wipe.yml for iu-devops-vm

TASK [web_app : Check if application directory exists] ****************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Stop and remove containers with Docker Compose] *******************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove docker-compose.yml file] ***********************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove application directory] *************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : List Docker images for the application] ***************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove Docker images] *********************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Log wipe completion] **********************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Write wipe to log file] *******************************************************************************************************************skipping: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=2    changed=0    unreachable=0    failed=0    skipped=8    rescued=0    ignored=0


$ ansible-playbook playbooks/deploy.yml \
>   -e "web_app_wipe=true" \
>   --tags web_app_wipe

PLAY [Deploy application] *********************************************************************************************************************************
TASK [Gathering Facts] ************************************************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Include wipe tasks] ***********************************************************************************************************************included: /mnt/d/Innopolis/ucheba/DevOps/IU-DevOps-S25/ansible/roles/web_app/tasks/wipe.yml for iu-devops-vm

TASK [web_app : Check if application directory exists] ****************************************************************************************************ok: [iu-devops-vm]

TASK [web_app : Stop and remove containers with Docker Compose] *******************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Remove docker-compose.yml file] ***********************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : Remove application directory] *************************************************************************************************************changed: [iu-devops-vm]

TASK [web_app : List Docker images for the application] ***************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Remove Docker images] *********************************************************************************************************************skipping: [iu-devops-vm]

TASK [web_app : Log wipe completion] **********************************************************************************************************************ok: [iu-devops-vm] => {
    "msg": [
        "Application devops-info-app wiped successfully",
        "Directory removed: /opt/devops-info-app",
        "Containers stopped: Yes",
        "Images removed: No"
    ]
}

TASK [web_app : Write wipe to log file] *******************************************************************************************************************changed: [iu-devops-vm]

PLAY RECAP ************************************************************************************************************************************************iu-devops-vm               : ok=8    changed=4    unreachable=0    failed=0    skipped=2    rescued=0    ignored=
```
