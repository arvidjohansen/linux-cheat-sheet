# linux-cheat-sheet
This is a collection of useful Linux/shell-commands

## Securing the system
Thanks to NetworkChuck (https://www.youtube.com/watch?v=ZhMw53Ud2tY)

### Step 1: Enable automatic updates
Manual Updates:
```sh
apt update
apt dist-upgrade
``` 

Automatic Updates:
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

### Step 5: Firewall it up
See open ports
```sh
sudo ss -tulpn
```

Install, configure and enable ufw
```sh
apt install ufw
```
if unable to find ufw, add repository (debian):
```sh
add-apt-repository "deb http://http.debian.net/debian/ jessie main contrib non-free"
```
See UFW status:
```sh
sudo ufw status
```
Allow port through firewall:
```sh
sudo ufw allow 22
```
Start firewall:
```sh
sudo ufw enable
```
Restart firewall:
```sh
sudo ufw reload
```


## Installing PHP
Following https://computingforgeeks.com/how-to-install-latest-php-on-debian/
### Installing PHP
```sh
sudo apt -y install lsb-release apt-transport-https ca-certificates 
sudo wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list
sudo apt update
sudo apt -y install php7.4
sudo apt install php libapache2-mod-php php-mysql
```
### Installing PHP-mysql connector
```
sudo apt install php7.4-mysqli
```

## Installing MySQL

|
## Configuring apache

```sh
nano /etc/apache2/sites-available/site1.conf
# minimal configuration
<VirtualHost *:80>
DocumentRoot /var/www/site1.com
ServerName www.site1.com
ServerAlias site1.com
</VirtualHost>
```

Enabling site

```sh
sudo a2ensite site1.com
``` 

Reloading apache
```sh
sudo systemctl restart apache2
```

