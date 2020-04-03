import hashlib
import itertools
import time

def crackBrute(password, hashType, cartProduct):
    testHash = None
    for line in cartProduct:
        test="".join(line)
        test = test.strip()
        if hashType == "MD5":
            testHash = hashlib.md5(test.encode('utf-8')).hexdigest()
        elif hashType == "SHA512":
            testHash = hashlib.sha512(test.encode('utf-8')).hexdigest()
        if testHash == password:
            return test
    return False

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
            #print("test")
            return item
    return False

def testBruteLogic(password, hashType):
    jobs=[]
    #print("test")
    start_time = time.time()
    for passwordLength in range(1, 6):
        job = crackBrute(password, hashType, itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=passwordLength))
        jobs.append(job)
    for row in jobs:
        paswd = row
        if paswd:
            print("--- %s seconds ---" % (time.time() - start_time))
            print (password, "=", paswd)

def testWordListLogic(password, wordList, hashType):
    jobs=[]
    chunkList = splitListIntoTasks(wordList)
    start_time = time.time()
    #print("test1")
    for line in chunkList:
        job=crackPwd(line, hashType, password)
        jobs.append(job)
    for row in jobs:
        if row:
            #print("tas")
            print("--- %s seconds ---" % (time.time() - start_time))
            print (password, "=", row)
            
                   


def splitListIntoTasks(wordList):
    chunkList = []
    #nodeCount = 10
    nodeCount = 4
    factor = 10
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

def modeList(wordList):
    """Function for selecting and reading wordlist"""
    wordList = open(wordList, 'r', encoding="utf-8", errors="replace").readlines()
    return wordList

def runAllTests():
    #print("test")
    testBruteLogic("b61a6d542f9036550ba9c401c80f00ef", "MD5")
    testWordListLogic("3a3a5c3f10e14cc9d5e92127a0ee0880", modeList("1-000-000.txt"), "MD5")
    testWordListLogic("5c7686c0284e0875b26de99c1008e998", modeList("100-000.txt"), "MD5")

runAllTests()
