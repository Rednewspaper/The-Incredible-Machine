# The Incredible Machine

The Incredible Machine is easy to use password cracker that utilize two or more Raspberry Pi nodes. The program uses one node as the master/main node that is responsible for doing some startup calculations(like amount of nodes and size of jobs distributed) while all other nodes are treated as slave/secondary nodes that are assigned a computation with jobs(jobs here being different parameters for the computation) to perform. Each node will perform its job and result its results to the main node. The program is fully scalable and will work as long as one main and one secondary or more nodes are configured correctly. The program is not very efficient running with only one secondary node, but it is exponentially becoming more efficient for each node added.(might need to change this part based on benchmarking results)

The Incredible Machine works with Python version 3.1+. It has been designed for usage in a Linux environment, it has been tested with Raspbian buster lite on a Raspberry Pi. 

## Features

* Hash cracking of custom password by default wordlist  with [1-000-000.txt](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt).
* Hash cracking of custom password by custom wordlist, user submitted.
* Hash cracking of custom password by bruteforce wordlist, generated using custom user depth.
* Password computations are divided in chunks for distribution as jobs. These chunks are decided by the amount of nodes and wordlist length. 
* Capabilities for detecting MD5 and SHA-256 hashing algorithms, by utilizing [hashid](https://github.com/psypanda/hashID).
* Capabilities for cracking MD5 and SHA-256 encrypted hashes.

## Dependencies

The Incredible Machine requires nmap for node discovery(slave nodes) for usage in brute force wordlist chunk size numeration. It requires [dispy](http://dispy.sourceforge.net/dispy.html) as its distribution system, for managing the cluster and submitting jobs to the cluster. It also requires [hashid](https://github.com/psypanda/hashID) which is used to identify the type of hashing algorithm used to encrypt the password that is being cracked. The Incredible Machine also requires a default wordlist, which is set to [rockyou.txt](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Leaked-Databases/rockyou-20.txt), this list is used for the default wordlist mode. This wordlist can be replaced by changing using another wordlist and changing the read file in the modeList() function in the source code. These dependencies are automatically installed if the [installScriptMainNode](https://github.com/Rednewspaper/The-Incredible-Machine/blob/master/installScripts/installScriptMainNode)(for master/main/head node) and [installScriptSlaveNode](https://github.com/Rednewspaper/The-Incredible-Machine/blob/master/installScripts/installScriptSlaveNode)(for other nodes) are installed. Apart from this The Incredible Machine utilizes python 3 with the module OS which needs to be installed in the Raspberry Pi’s that are in use. 

## Installation

To collect The Incredible Machine and install its dependencies collect and run [installScriptMainNode](https://github.com/Rednewspaper/The-Incredible-Machine/blob/master/installScripts/installScriptMainNode):

``` 
$ wget https://raw.githubusercontent.com/Rednewspaper/The-Incredible-Machine/master/installScriptMainNode?token=AOH75QFON2ZJMHI7I6XV3GK6PJT4M
$ chmod +x installScriptMainNode
$ ./installScriptMainNode
```

## Initial Configurations

In order for the program to work as intended a couple of ip addresses has to be changed in the source code. These addresses are that of the master/main node and of the subnet where the slave nodes are located. These changes do not have to be done if this [guide](https://github.com/Rednewspaper/The-Incredible-Machine/blob/master/IP-guide.md#step-3) for setting up your Raspberry Pi’s on the 10.0.0.0/24 subnet has been performed. Otherwise the changes can be by doing this:

Enter the folder where you ran the [installScriptMainNode](https://github.com/Rednewspaper/The-Incredible-Machine/blob/master/installScripts/installScriptMainNode).

```
$ nano INCMACHINE0.0.[version].py
```

Scroll to the countNodes() function and change the following line:



```
$ os.system(‘nmap -p 61591 [Subnet ip] | grep open > newresult.txt’)
```

Scroll to the mainLogic() function and change the following line:




```
$ Cluster = dispy.JobCluster(crackPwd, ip_addr=’[IP address of master node]’)
```

## Usage

### Slave Nodes:

Enter the dispy folder  on the slave nodes, which can be accessed using the following command:

```
$ cd /home/[USER]/.local/lib/dispy
```

Start the dispynode.py program which executes jobs submitted by clients:

```
$ python3 dispynode.py -i [IP ADDRESS]
```

This ip address is the address you want the program to use, default(without -i) is localhost. It needs to be specified and match that of the interface you want to use(example eth0 or wlan0). A guide on how to setup the Raspberry Pi’s nodes within the 10.0.0.0/24 subnet on eth0 is provided [here](https://github.com/Rednewspaper/The-Incredible-Machine/blob/master/IP-guide.md#step-3). If this guide is used the Pi’s will use the addresses 10.0.0.2-[amount of nodes].

### Main Node:

Enter the folder where you ran the [installScriptMainNode](https://github.com/Rednewspaper/The-Incredible-Machine/blob/master/installScripts/installScriptMainNode) and run the program.

```
$ python3 INCMACHINE0.0.5a.py 
```

## Authors

* Lewis Campbell
* Gustav Martin Kvilhaug Magnussen
* Kenny Carlos Hernandez Aguilera

