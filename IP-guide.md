# Guide for setting up Raspberry Pi’s on the 10.0.0.0/24 subnet

## Step 1

To start setting up the IP 's on the 10.0.0.0/24 subnet, you first need to gain access to your Pi’s. This can either be done by connecting the Pi’s to peripherals or connecting to the Pi’s  through SSH. If you have access to the Pi’s through peripherals you can skip directly to [Step 3](#Step 3). 

If you are not able  to SSH into your Raspberry Pi’s(due to it being set up from a Buster lite image) you can follow this [guide](https://www.hackster.io/najad/enable-ssh-on-raspberry-pi-without-monitor-keyboard-210dc4) for enabling SSH on the buster lite OS. 



## Step 2

The next step would be to actually SSH into your Pi’s, if the computer you are SSH from is a Windows this could easily be done by either install a Linux subsystem(which can easily by install using this [guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10)) or using PuTTy.


### Using a Linux subsystem

Using Linux subsystem you can easily SSH into your Pi’s by opening your Linux subsystem from the Windows search bar. The command you need to enter is:

```
$ ssh pi@[IP-ADDRESS OF PI]
```

The default name of your Pi’s is “pi”, if this has been changed you will need to command to your hostname. If this is the first time you are SSH into your Pi’s you will need to accept the prompt that is displayed.




Having done this you will be asked to enter the password of the Pi which by default is “raspberry”.

### Using PuTTY
 
For using PuTTY you need to open the program and enter the IP of the Pi in the designated field.



After this you will need to click open, if this is the first time you are SSH into the Pi’s you will get an alert which needs to be accepted. 

 

Having done this you will be prompted to enter the login and password of the Pi. The default hostname is “pi” and the default password is “raspberry”

## Step 3

Having gained access to your Pi you will need to edit the dhcpcd.conf file which enables the usage of a static ip address. This file can be access and edited by using this command:

```
$ sudo nano /etc/dhcpcd.conf
```
Having entered this file the following needs to be added on the bottom of the file.

```
interface eth0
static ip_address=10.0.0.1/24
```

For each subsequent Pi configured this ip address has to be changed to the next in line. We advise to have the master node as the Pi with the address 10.0.0.1/24 and any subsequent as 10.0.0.2/24, 10.0.0.3/24 and so forth.

For this changes to take effect the Pi’s should be rebooted using this command:

```
$ sudo reboot
```
