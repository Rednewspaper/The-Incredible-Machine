import dispy
import hashlib
import os

def countNodes():

    os.system('nmap -p 61591 10.0.0.0/24 | grep open > newresult.txt')

    data = open('newresult.txt', 'r')
    count=0
    for x in data:
        if "open" in x:
            count=count+1
    data.close()
    os.remove('newresult.txt')
    return count

def modeList():
    """Function for selecting and reading wordlist"""
    wordList = open("1-000-000.txt", 'r').readlines()
    return wordList


def splitListIntoTasks(wordList):
    """Returns given_list split into chunks
    Given_list is handed to function by selectMode()
    """

    chunkList = []
    nodeCount = countNodes()
    #nodeCount = 1
    factor = 3
    equalChunks = nodeCount * factor
    chunkSize = len(wordList) // equalChunks
    count=0
    for x in range(equalChunks):
        firstIndex=chunkSize * count
        lastIndex=firstIndex + chunkSize
        workingList = wordList[firstIndex : lastIndex]
        chunkList.append(workingList)
        count += 1
    if len(wordList) % equalChunks != 0:
        remainder = len(wordList) % equalChunks
        workingList = wordList[-remainder:]
        chunkList.append(workingList)
    return chunkList


def crackPwd(chunk, hashType, password):
    """This is the function that is sent to the nodes"""
    #Insert haslib matching function (similar to youtube video)
    testHash = None
    for item in chunk:
        item = item.strip()
        if hashType == "MD5":
            testHash = hashlib.md5(item.encode('utf-8')).hexdigest()
        elif hashType == "SHA512":
            testHash = hashlib.sha512(item.encode('utf-8')).hexdigest()
        if testHash == password:
            return item
    return False


def get_hash_type(password):
    """This function determines the hash type(using hashid: https://github.com/psypanda/hashID)
    Return hash_type"""
    data = open('hash_type.txt', 'w+')
    command = 'python3 hashid.py' + ' -m -o hash_type.txt \'' + password + '\''
    hash_type = None
    os.system(command)

    for line in data:
        if 'MD5' in line:
            hash_type = 'MD5'

        elif 'SHA-256' in line:
            hash_type = 'SHA-256'

    data.close()
    os.remove('hash_type.txt')
    hash_type = 'MD5'                                                                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return hash_type




def generateBruteWordlist():
    #Insert function for determining what charset to use and depth (password length ) it should be
    #Insert function that uses determined parameters to create such a wordlist
    print ("Under construction")
    menuMode()

def endScreen(password, win=False):
    if win:
        print ("Victory")
        print (password, "=", win)
    else:
        print ("Unable to crack", password, "using the method you selected")
    menuMode()

def mainLogic(password, wordList):
    win = False
    chunkList = splitListIntoTasks(wordList)
    hashType = get_hash_type(password)
    nodes = ['10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5']
    cluster = dispy.JobCluster(crackPwd, ip_addr='10.0.0.1', nodes=nodes)
    jobs = []
    password = "3a3a5c3f10e14cc9d5e92127a0ee0880"
    for chunk in chunkList:
        job = cluster.submit(chunk, hashType, password)
        jobs.append(job)
        didWeFind = job()
        if didWeFind:
            win = True
            cluster.close(timeout=None,terminate=True)
            endScreen(password, didWeFind)
    if not win:
        endScreen(password, False)

def menuMode():
    print (" ")
    print ("The Incredible Machine")
    print (" ")
    while True:
        password = input("Enter the hash that is going to be cracked:")
        print (password)
        enterHash = input("Is this the correct hash?(y/n):")
        if enterHash == "y" or enterHash == "Y":
            break

    while True:
        programType = input("Enter 1 for Wordlist mode or Enter 2 for Bruteforce mode(or 0 for quit):")
        if programType == "1":
            while True:
                listType = input("Enter 1 for Default Wordlist or Enter 2 for Custom Wordlist(You need to provide the list)(or 0 to go back):")
                if listType == "1":
                    wordList = modeList()
                    mainLogic(password, wordList)
                elif listType == "2":
                    wordList = modeCustom()
                    mainLogic(password, wordList)
                elif listType == "0":
                    break
        elif programType == "2":
            generateBruteWordlist()
        elif programType == "0":
            exit()

def modeCustom():
    while True:
        wordList = input("Please enter the name of your wordlist file(only .txt file is accepted):")
        exists = os.path.isfile(wordList)
        if exists:
            break
        else:
            print("The file you entered does not exist or is not in the same folder as this program")
    readlist = open(wordList, 'r')
    wordlist = readlist.readlines()
    readlist.close()
    return wordlist




menuMode()

#password = "5c7686c0284e0875b26de99c1008e998"
#wordList = selectMode()
#chunkList = splitListIntoTasks(wordList)
#for chunk in chunkList:                                                      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#    cluster = dispy.JobCluster(crackPwd(chunk, hashType, password))          !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#More logic needed down here regarding canceling jobs when we have found the password
