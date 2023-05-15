sudo apt update
sudo apt install apache2 mysql-server libapache2-mod-wsgi-py3 -y
sudo apt install python3 python3-pip -y
sudo pip3 install django
django-admin startproject myproject
sudo nano /etc/apache2/sites-available/myproject.conf
sudo a2ensite myproject
sudo systemctl restart apache2
ip a
exit 
vagrant ssh-config
exit
sudo nano index.html
exit
code .
exit
vagrant ssh-config
exit
code .
exit
