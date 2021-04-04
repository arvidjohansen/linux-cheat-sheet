# linux-cheat-sheet
This is a collection of useful Linux/shell-commands

## Securing the system
Thanks to NetworkChuck (https://www.youtube.com/watch?v=ZhMw53Ud2tY)

### Step 1: Enable automatic updates
* Manual Updates:
```sh
apt update
apt dist-upgrade
``` 

* Automatic Updates:
```sh
apt install unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
``` 

### Step 2: Create a limited user account
```sh
adduser {username}
usermod -aG sudo {username}
``` 

### Step 3: Passwords are for suckers!
1) Create the Public Key Directory on your Linux Server
```sh
mkdir ~/.ssh && chmod 700 ~/.ssh
```
2) Create Public/Private keys on your computer
```sh
ssh-keygen -b 4096
```
3) Upload your Public key to the your Linux Server (Windows)
```sh
scp $env:USERPROFILE/.ssh/id_rsa.pub {username}@{server ip}:~/.ssh/authorized_keys
``` 

### Step 4: Lockdown Logins
```sh
sudo nano /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no (if you want to only permit certification-login)
```




Upload your Public key to the your Linux Server (Windows)
scp $env:USERPROFILE/.ssh/id_rsa.pub {username}@{server ip}:~/.ssh/authorized_keys

Upload your Public key to the your Linux Server (MAC)
scp ~/.ssh/id_rsa.pub {username}@{server ip}:~/.ssh/authorized_keys

Upload your Public key to the your Linux Server (LINUX)
ssh-copy-id {username}@{server ip}


STEP 4 - Lockdown Logins
Edit the SSH config file

sudo nano /etc/ssh/sshd_config
