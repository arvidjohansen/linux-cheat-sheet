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
apt install apache2 -y #install
systemctl start apache2 #start service
systemctl enable apache2 #start on boot

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


## Installing MariaDB
Latest tutorial: [DigitalOcean Debian 11 MariaDB Installation](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-debian-11)
```sh
apt install mariadb-server
mysql_secure_installation
```

Answer according to the tutorial on the questions that come.

When you are finished you can simply

```sh
root@localhost:~# mariadb
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 36
Server version: 10.5.15-MariaDB-0+deb11u1 Debian 11

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>

```
If the database I want to create is called `games`, a common way to go is to create a user with the same name that has full access to the database.

Remember that database users are always created by specifying the location/hostname/IP of the user (aka the application server).

However you can ignore this by specifying `*`

database: games
username: games
password:ChangeMyPassword123
hostname/IP if the application server: * 




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
[hamvocke.com - quick and easy guide to tmux](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/)

[Nice cheat-sheet MohamedAlaa@github](https://gist.github.com/MohamedAlaa/2961058)

>Tmux allows you to split your terminal in many ways
>
### Installation
```
sudo apt install tmux
```
### Usage
Commands:  
`tmux` creates a new tmux-session with a nice all-green status bar at the bottom   
`tmux new -s monitoring` creates a new session called "monitoring"  
`exit` exits a tmux-session  
`tmux ls` lists active tmux-sessions   
`tmux attach -t 0` attaches to session id 0  
`tmux attach -t monitoring` attaches to session with name "monitoring"  

If tmux is running but you get the following error:

>no server running on /tmp/tmux-1000/default

`pkill -USR1 tmux`

it works sometimes :)



Keyboard shortcuts:  
`ctrl + b + d` **disconnects** from the current session   
`ctrl + b + %` splits screen vertically  
`ctrl + b + "` splits screen horizontally  
`ctrl + b` then release the b-key and use arrows to resize window  

Keyboard shortcut-commands:  
`ctrl + b + :` to open the command prompt   
``` 
:set-option -g mouse on
:set-option history-file ~/.bash_history 
:resize-pane -D (Resizes the current pane down)
:resize-pane -U (Resizes the current pane upward)
:resize-pane -L (Resizes the current pane left)
:resize-pane -R (Resizes the current pane right)
:resize-pane -D 10 (Resizes the current pane down by 10 cells)
:resize-pane -U 10 (Resizes the current pane upward by 10 cells)
:resize-pane -L 10 (Resizes the current pane left by 10 cells)
:resize-pane -R 10 (Resizes the current pane right by 10 cells)
```

## nload (network load)
>Shows network in/out traffic as a nice graph   

`sudo apt install nload` to install   
`nload`to start the monitoring-application  

## top
>Shows process information similar to task manager in windows   

`top` to start   
`f` to open filter-settings
`shift + s` write current settings to configuration file  


Useful arguments:
|Parameter|Description|
|---|---|
|-i|Do not show idle processes|

## s-tui
>shows a nice graph displaying cpu-load  

`sudo apt install s-tui` to install   
`s-tui` to start  

## iotop
> disk activity monitoring, similar to "top" but for disk activity instead 

`sudo iotop` to run
Useful arguments
|Parameter|Description|
|---|---|
|-o|Only show active processes (that actually does I/O)|
|-P|Show processes instead of threads|

## htop
>like top but better
`apt install htop`

## Glances
>The best monitoring utility
>Behaves smart
>
`apt install glances`

![Glances picture](https://nicolargo.github.io/glances/public/images/screenshot-web.png)




# Tips & tricks
## Searching for files - the find command
```
find / -name tmux.conf
``` 
Will search the entire file system for tmux.conf, but will spam out a whole bunch of "permission denied"-messages.  
To avoid that use this little trick:
```
find / -name tmux.conf 2>&1 | grep -v "Permission denied"
```
To find files CONTAINING a search string use *
```
find / -name *history*
```

## SSH keepalive
To prevent users disconnecing from terminal, add the following lines
to your `/etc/ssh/sshd_config`
```
TCPKeepAlive yes
ClientAliveInterval 60
```

## Monitoring failed login attempts
grep "authentication failure" /var/log/auth.log | awk '{ print $13 }' | cut -b7-  | sort | uniq -c


# Tools
|Name|Description|
|---|---|
|grep|Finds information in input|
|awk|Filters columns?|
|sed||
|wc|Word count|
|sort||
|cut||
|uniq||


## awk
https://www.geeksforgeeks.org/awk-command-unixlinux-examples/

## pstree
`pstree -p`
shows a tree structure of which processes spawned from where

# Resources

## Cheat sheets
1) https://cheatography.com/davechild/cheat-sheets/linux-command-line/

![cs-page-1](https://i.ibb.co/hBFqC63/lin-cs-1.png)
![cs-page-2](https://i.ibb.co/xfyS17Y/lin-cs-2.png)

# VSCode Remote SSH process memory problem
If you use VSCode with the remote SSH plugin, you will sometimes see hanging processes even after you exit.
These can take up a lot of memory when they pile up.
The processes are spawned because VSCode tries to do some autocorrect stuff described [here](https://medium.com/good-robot/use-visual-studio-code-remote-ssh-sftp-without-crashing-your-server-a1dc2ef0936d)

1. Hit the extensions button in VS Code (which looks like building blocks on the left toolbar)
2. Search for ‘@builtin TypeScript’
3. Disable the TypeScript and Javascript Language Features extension
4. Reload

# Bluetooth on Linux (bluetoothctl)
`apt install bluez`

`systemctl start bluetooth`

All commands prepended by `bluetoothctl <command>` when done outside the interactive shell, otherwise you can do all the commands directly into the shell spawned by `bluetothctl`

## Initial pairing
`discoverable on`

`scan on`

`pair 78:2B:64:A2:F8:F1`

`trust 78:2B:64:A2:F8:F1`

If names do not show, try this:

 `bluetoothctl devices | cut -f2 -d' ' | while read uuid; do bluetoothctl info $uuid; done|grep -e "Device\|Connected\|Name"`


## Every time
`connect 78:2B:64:A2:F8:F1`

and when done:

`disconnect`

## Todo
`power on`

>This video is nice:

[Youtube - BugsRider Bluetoth Guide](https://www.youtube.com/watch?v=Jhzqm8JKekk&ab_channel=BugsWriter)

![IMG](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi0.wp.com%2Fstatic1.makeuseofimages.com%2Fwordpress%2Fwp-content%2Fuploads%2F2021%2F05%2Fcheck_bluetooth_service_status-1.png%3Fw%3D750%26is-pending-load%3D1%23038%3Bssl%3D1&f=1&nofb=1&ipt=86f480bac07e0884afa8c1ea6d781ae927adb1547b81d2e1f975e38391bc0cf9&ipo=images)


# ls
https://www.linuxcommands.site/linux-file-and-directory-commands/linux-ls-sort/


# Mounting USB partition manually
Identify USB-device
lspci
lsusb
dmesg | less

`sudo pmount /dev/sda1 /media/a`
> partition now mounted


# Setting up VPN over SSH with Python
[VPN SSH Python guide](https://www.xmodulo.com/how-to-set-up-vpn-over-ssh-in-linux.html)
```sh
sudo apt-get install sshuttle
sudo yum install git
git clone git://github.com/apenwarr/sshuttle
sudo sshuttle -r user@remote_host 0.0.0.0/0 --dns
sudo sshuttle -r user@remote_host 172.194.0.0/16 172.195.0.0/16
```

# Neofetch (nice looking status motd)

```sh
apt install neofetch
echo neofetch >> ~/.bash_profile # run automatically on login
```

# Desktop stuff
## Redshift (blue light	filter)

```sh
apt install redshift
mkdir ~/.config/redshift
wget https://raw.githubusercontent.com/jonls/redshift/master/redshift.conf.sample
mv redshift.conf.sample ~/.config/redshift/redshift.conf
```

# tcpdump

[hackertarget.com examples](https://hackertarget.com/tcpdump-examples/)

[cyberciti.biz](https://www.cyberciti.biz/faq/tcpdump-capture-record-protocols-port/)

[tcpdump tutorial daniel miessler](https://danielmiessler.com/study/tcpdump/)

[tcpdump cheat sheet by packetlife](https://packetlife.net/media/library/12/tcpdump.pdf)

[tcpdump cheat sheet comapitech](https://cdn.comparitech.com/wp-content/uploads/2019/06/tcpdump-cheat-sheet.webp)

# Pipe/redirecting output/etc | > >>

redirect the output (AKA stdout) to a file:

```sh
SomeCommand > SomeFile.txt  
```

Or if you want to append data:

```sh
SomeCommand >> SomeFile.txt
```


If you want stderr as well use this:

```sh
SomeCommand &> SomeFile.txt  
```

or this to append:

```sh
SomeCommand &>> SomeFile.txt  
```

if you want to have both stderr and output displayed on the console and in a file use this:

```sh
SomeCommand 2>&1 | tee SomeFile.txt
```

(If you want the output only, drop the 2 above)


# PostgresQL installation on Linux (Debian 11)

First install 
```sh
sudo apt-get -y install postgresql
```
