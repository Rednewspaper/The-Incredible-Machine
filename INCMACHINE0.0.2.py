#import dispy                                             !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import hashlib
import os

def countNodes():

    os.system('nmap -p 61591 10.0.0.0/24 -oN result.txt | grep open')
    data = open('result.txt').read()
    nodeCount = data.count('open')
    data.close()

    os.remove('result.txt')
    return nodeCount

def selectMode(mode = "list"):
    """Function for selecting mode (brute force or wordList)
    returns the appropriate wordList
    """
    if mode == "list":
        return readList()
    else:
        return generateBruteWordlist()

def readList():
    """Function for selecting and reading wordlist"""
    wordList = open("worst-passwords-2017.txt", 'r').readlines()
    return wordList


def splitListIntoTasks(wordList):
    """Returns given_list split into chunks
    Given_list is handed to function by selectMode()
    """

    chunkList = []
#    nodeCount = countNodes()                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    nodeCount = 1
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
    pass
    return newWordList, wordCount

def mainMenu():
    print ("Insert nice menu text here")
    userChoice = input()
    if True:
        password = "5c7686c0284e0875b26de99c1008e998"
        wordList = selectMode()
        chunkList = splitListIntoTasks(wordList)
        hash_type = get_hash_type(password)
        for chunk in chunkList:                                  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            isIt = crackPwd(chunk, hash_type, password)
            if isIt:
                print (isIt)
                break

    else:
        pass

mainMenu()

#password = "5c7686c0284e0875b26de99c1008e998"
#wordList = selectMode()
#chunkList = splitListIntoTasks(wordList)
#for chunk in chunkList:                                                      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#    cluster = dispy.JobCluster(crackPwd(chunk, hashType, password))          !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#More logic needed down here regarding canceling jobs when we have found the password

pause=input()
