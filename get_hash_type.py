import os 
import hashid

password = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'

def get_hash_type(password):
    
    data = open('hash_type.txt', 'w+')
    
    command = 'python3 hashid.py' + ' -m -o hash_type.txt \'' + password + '\''
    
    os.system(command)
    
    for line in data:
        if 'MD5' in line:
            hash_type = 'MD5'
        
        elif 'SHA-256' in line:
            hash_type = 'SHA-256'
            
    data.close()
    
    return hash_type
