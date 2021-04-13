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

## Installing Apache
Following https://www.tecmint.com/install-apache-with-virtual-hosts-on-debian-10/
```sh
sudo apt install apache2 -y #install
sudo systemctl start apache2 #start service
sudo systemctl enable apache2 #start on boot

sudo ufw allow 80/tcp #allow through firewall
```

## Installing PHP
Following https://computingforgeeks.com/how-to-install-latest-php-on-debian/
  
```sh
sudo apt -y install lsb-release apt-transport-https ca-certificates 
sudo wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list
sudo apt update
sudo apt -y install php7.4
sudo apt install php libapache2-mod-php php-mysql
```


## Installing MySQL
```sh
wget http://repo.mysql.com/mysql-apt-config_0.8.13-1_all.deb
sudo apt install ./mysql-apt-config_0.8.13-1_all.deb
sudo apt-get install mysql-community-server
sudo systemctl status mysql
```
Create database and user
```sql
CREATE DATABASE stock;
CREATE USER 'stock'@'localhost' IDENTIFIED BY 'StockFish123';
GRANT ALL PRIVILEGES ON stock.* TO 'stock'@'localhost';
FLUSH PRIVILEGES;
```

## Installing PHP-mysql connector
```
sudo apt install php7.4-mysqli
```

