#!/bin/bash
echo "Incredible Machine Install Script"
echo "Please wait"
### "Run as sudo" check
if [ $(whoami) != 'root' ]
then
    echo "
This script needs to be run as root, or with sudo:
    sudo $0
"
    exit 1
fi
### Update OS
apt-get update && apt-get -y upgrade
### Install software
apt-get -y install nmap
### Install python packages
apt-get -y install python3-pip
python3 -m pip install --upgrade pip
wget -O dispy-4.11.1.tar.gz https://sourceforge.net/projects/dispy/files/dispy-4.11.1.tar.gz/download
python3 -m pip install dispy-4.11.1.tar.gz
python3 -m pip install hashid
###Get files
wget https://raw.githubusercontent.com/Rednewspaper/The-Incredible-Machine/master/INCMACHINE0.1.0.py
wget https://raw.githubusercontent.com/Rednewspaper/The-Incredible-Machine/master/wordlists/1000-000-passwords.txt
wget https://raw.githubusercontent.com/Rednewspaper/The-Incredible-Machine/master/wordlists/100-000-passwords.txt 