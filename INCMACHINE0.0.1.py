import dispy
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
    nodeCount = countNodes()
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


def crackPwd(chunk, hashType, password):
    """This is the function that is sent to the nodes"""
    #Insert haslib matching function (similar to youtube video)
    for item in chunk:
        item = item.strip() 
        if hashType == "MD5":
            testHash = hashlib.md5(item).hexdigest()
        elif hashType == "SHA512":
            testHash = hashlib.sha512(item).hexdigest()
        if testHash == password:
            return item
    return False


def get_hash_type(password):
     """This function determines the hash type(using hashid: https://github.com/psypanda/hashID)
Return hash_type"""
    #Insert function for determining hash type
    return "MD5"



def generateBruteWordlist():
    #Insert function for determining what charset to use and depth (password length ) it should be
    #Insert function that uses determined parameters to create such a wordlist
    pass
    return newWordList, wordCount

password = "thunder"
wordList = selectMode()
chunkList = splitListIntoTasks(wordList)
for chunk in chunkList:
    cluster = dispy.JobCluster(crackPwd(chunk, hashType, password))

#More logic needed down here regarding canceling jobs when we have found the password

a=input()
