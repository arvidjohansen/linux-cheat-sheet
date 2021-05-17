# linux-cheat-sheet
This is a collection of useful Linux/shell-commands

## Configuring terminal for root
To enable terminal-coloring for root, open /root/.bashrc
and uncomment the following lines:
```sh
# You may uncomment the following lines if you want `ls' to be colorized:
 export LS_OPTIONS='--color=auto'
 eval "`dircolors`"
 alias ls='ls $LS_OPTIONS'
 alias ll='ls $LS_OPTIONS -l'
 alias l='ls $LS_OPTIONS -lA'
```

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

## Configuring virtual hosts
Always configure virtual hosts in /etc/apache2/sites-available/

Example with domain name containing æ,ø,å and files in /var/www/alpha
```sh
<VirtualHost *:80>
	# Actual domain name is alpha.bodø.city but since it contains 
	# non-ascii characters we have to use punycode, more info:
	# http://handbok.dinstudio.no/0/37/o-a-i-domenenavn/
	# https://www.punycoder.com/
	
        ServerName alpha.xn--bod-2na.city
        ServerAlias www.alpha.xn--bod-2na.city

        ServerAdmin arvid@bodø.city
        DocumentRoot /var/www/alpha

	ErrorLog ${APACHE_LOG_DIR}/error-alpha.log
        CustomLog ${APACHE_LOG_DIR}/access-alpha.log combined
</VirtualHost>
```
When finished, enable site with command:
```sh
a2ensite site.name.conf
```
Always restart service after making changes: 
```sh
systemctl reload apache2
```
Disable site with:
```sh
a2dissite site.name.conf
```

## Limiting access with .htaccess files
https://www.linode.com/docs/guides/how-to-set-up-htaccess-on-apache/
https://phoenixnap.com/kb/how-to-set-up-enable-htaccess-apache
By creating a file called .htaccess in a directory served by apache,
you can limit access to files and folders based on a pattern i.e. disallowing .git folder:

```sh
RedirectMatch 404 /\.git
```
or disallowing directory listing (showing files and folders if no index-file is present):
```sh
Options -Indexes
```

But first you have to enable it by adding the following to your vhost conf (inside virtualhost definition):
```sh
<Directory /var/www/html-templates>
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>
```

## HTTPS / Creating a SSL certificate
Install Certbot
```sh
sudo add-apt-repository ppa:certbot/certbot
apt-get install software-properties-common
apt install python-certbot-apache
certbot --apache -d templates.arvid.software
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
#apt update
#apt upgrade should work
sudo apt-get install mysql-community-server
sudo systemctl status mysql
```
### Creating database and user
```sql
CREATE DATABASE stock;
CREATE USER 'stock'@'localhost' IDENTIFIED BY 'StockFish123';
GRANT ALL PRIVILEGES ON stock.* TO 'stock'@'localhost';
FLUSH PRIVILEGES;
```
or use the built-in python-script to generate SQL code for you:
```sql
C:\Users\Arvid\Desktop\git\linux-cheat-sheet>python create_mysql_db_and_usr.py

Welcome!

This script will generate sql for creating a database, user,
and giving the user full permissions on the specified host like this example:

********************************************
CREATE DATABASE <dbname>;
CREATE USER '<usr>'@'<host>' IDENTIFIED BY '<pw>';
GRANT ALL PRIVILEGES ON <dbname>.* TO '<usr>'@'<host>';
********************************************

Enter value for host (default: localhost):
Enter value for db (default: ): phpmyadmin
Enter value for usr (default: ): phpmyadmin
Enter value for pw (default: ): Php@Myadm123!
********************************************

CREATE DATABASE phpmyadmin;
CREATE USER 'phpmyadmin'@'localhost' IDENTIFIED BY 'Php@Myadm123!';
GRANT ALL PRIVILEGES ON phpmyadmin.* TO 'phpmyadmin'@'localhost';

********************************************
```

## Installing PHP-mysql connector
```
sudo apt install php7.4-mysqli
```

## Installing phpMyAdmin
Following
#https://phoenixnap.com/kb/how-to-install-phpmyadmin-on-debian-10
#sudo apt install php php-cgi php-mysqli php-pear php-mbstring php-gettext libapache2-mod-php php-common php-phpseclib php-mysql -y #do I need all these?

https://computingforgeeks.com/install-phpmyadmin-with-apache-on-debian-10-buster/

Do we reaaally need phpmyadmin?


## PGP Encryption
```sh
sudo apt install gnupg2 gpa
gpg --full-generate-key #1 enter #4096 enter #0 enter #y #<name and email> #o enter 
#enter passphrase

sudo gpa

```

# Useful applications
## Tmux (terminal multiplexer)
>Tmux allows you to split your terminal in many ways
>
### Installation
```
sudo apt install tmux
```
### Usage
`tmux` creates a new tmux-session with a nice all-green status bar at the bottom   
`tmux new -s monitoring` creates a new session called "monitoring"
`exit` exits a tmux-session  
`tmux -l` lists active tmux-sessions   
`tmux attach -t 0` attaches to session id 0  
`tmux attach -t monitoring` attaches to session with name "monitoring"  
`ctrl + b + %` splits screen vertically  
`ctrl + b + "` splits screen horizontally  
`ctrl + b + d` disconnects from the current session

## nload (network load)
>Shows network in/out traffic as a nice graph   

`sudo apt install nload` to install   
`nload`to start the monitoring-application  

## top
>Shows process information similar to task manager in windows   

`top` to start  

## s-tui
>shows a nice graph displaying cpu-load  

`sudo apt install s-tui` to install   
`s-tui` to start  







