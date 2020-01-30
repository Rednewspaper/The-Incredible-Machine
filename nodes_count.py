import os

def countNodes():
  
    os.system('nmap -p 61591 10.0.0.0/24 -oN result.txt | grep open')
    data = open('result.txt').read()
    count_nodes = data.count('open')
    data.close()

    os.remove('result.txt')
