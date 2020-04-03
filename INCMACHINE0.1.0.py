import dispy
import threading
import hashlib
import os
import numpy
import itertools

def countNodes():
    """Function for counting number of running dispy nodes in network"""

    os.system('nmap -p 61591 10.0.0.0/24 | grep open > newresult.txt')

    data = open('newresult.txt', 'r')
    count=0
    for x in data:
        if "open" in x:
            count=count+1
    data.close()
    os.remove('newresult.txt')
    return count

def modeList(wordList):
    """Function for selecting and reading wordlist"""
    wordList = open(wordList, 'r', encoding="utf-8", errors="replace").readlines()
    return wordList


def splitListIntoTasks(wordList):
    """Returns given_list split into chunks, for efficient wordlist mode cracking
    """
    chunkList = []
    nodeCount = countNodes()
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


def crackPwd(chunk, hashType, password):
    """This is the function that is sent to the nodes when cracking in wordlist mode"""
    #Insert haslib matching function (similar to youtube video)
    testHash = None
    for item in chunk:
        item = item.strip()
        if hashType == "MD5":
            testHash = hashlib.md5(item.encode('utf-8')).hexdigest()
        elif hashType == "SHA-1":
            testHash = hashlib.sha1(item.encode('utf-8')).hexdigest()
        elif hashType == "SHA-224":
            testHash = hashlib.sha224(item.encode('utf-8')).hexdigest()
        elif hashType == "SHA-256":
            testHash = hashlib.sha256(item.encode('utf-8')).hexdigest()
        elif hashType == "SHA-384":
            testHash = hashlib.sha384(item.encode('utf-8')).hexdigest()
        elif hashType == "SHA-512":
            testHash = hashlib.sha512(item.encode('utf-8')).hexdigest()
        if testHash == password:
            return item
    return False


def getHashType(password, hashMode):
    """This function determines the hash type, either by manual entry or using hashid: https://github.com/psypanda/hashID)
    Returns hashType"""
    hashType = None
    if hashMode == 1:
        while True:
            hashType = input("Enter hash type(only MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512): ")
            if hashType == "MD5" or hashType == "SHA-1" or hashType == "SHA-224" or hashType == "SHA-256" or hashType == "SHA-384" or hashType == "SHA-512":
                return hashType

    elif hashMode == 2:
        data = open('hashType.txt', 'w+')
        command = 'python3 /usr/local/lib/python3.7/dist-packages/hashid.py' + ' -m -o hashType.txt \'' + password + '\''
        os.system(command)

        for line in data:
            if 'MD5' in line:
                hashType = 'MD5'
            elif 'SHA-1' in line:
                hashType = 'SHA-1'
            elif 'SHA-224' in line:
                hashType = 'SHA-224'
            elif 'SHA-256' in line:
                hashType = 'SHA-256'
            elif 'SHA-384' in line:
                hashType = 'SHA-384'
            elif 'SHA-512' in line:
                hashType = 'SHA-512'
            else:
                hashType = False

        data.close()
        os.remove('hashType.txt')
    if hashType:
        return hashType
    else:
        print ("Unable to automatically determine hash, or hash type not supported. Check you entered hash correctly, or try setting hash manually")
        menuMode()

def crackBrute(password, hashType, cartProduct):
    """This is the function that is sent to the nodes when cracking in Bruteforce mode"""
    testHash = None
    for line in cartProduct:
        test="".join(line)
        test = test.strip()
        if hashType == "MD5":
            testHash = hashlib.md5(test.encode('utf-8')).hexdigest()
        elif hashType == "SHA-1":
            testHash = hashlib.sha1(test.encode('utf-8')).hexdigest()
        elif hashType == "SHA-224":
            testHash = hashlib.sha224(test.encode('utf-8')).hexdigest()
        elif hashType == "SHA-256":
            testHash = hashlib.sha256(test.encode('utf-8')).hexdigest()
        elif hashType == "SHA-384":
            testHash = hashlib.sha384(test.encode('utf-8')).hexdigest()
        elif hashType == "SHA-512":
            testHash = hashlib.sha512(test.encode('utf-8')).hexdigest()
        if testHash == password:
            return test
    return False



def generateBrute(password, hashType):
    """Function for getting bruteforce depth from user"""

    depth = input("What depth? (1-11): ")
    try:
        depth=int(depth)
    except ValueError:
        print ("The depth must be an integer")
        generateBrute(password, hashType)
    else:
        if depth > 11 or depth < 1:
            print ("Depth must be between 1 and 11")
            generateBrute(password, hashType)
        else:
            bruteLogic(password, hashType, depth)

def bruteLogic(password, hashType, depth):
    """Control function for submitting jobs to cluster while in bruteforce mode"""
    cluster = dispy.JobCluster(crackBrute, ip_addr='10.0.0.12')
    jobs=[]
    #TIME_START
    for passwordLength in range(1, depth+1):
        job = cluster.submit(password, hashType, itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=passwordLength))
        jobs.append(job)
    cluster.wait()
    for row in jobs:
        paswd = row
        value = paswd.result
        if value:
            cluster.stats()
            cluster.close()
            #TIME_STOP
            winScreen(value, password)
    print ("Unable to crack", password, "using the method you selected")
    restart = input("Do you want to crack another hash/retry hash using another method?(y/n): ")
    cluster.close()
    if restart == "y" or restart == "Y":
        menuMode()
    else:
        exit()


def winScreen(paswd, password):
    """Function that is called when hash is cracked"""

    print ("Victory")
    print (password, "=", paswd)


    restart = input("Do you want to crack another hash/retry hash using another method?(y/n): ")
    if restart == "y" or restart == "Y":
        menuMode()
    else:
        exit()

def job_callback(job): # executed at the client
    """Function for managing que based on job status"""
    global pending_jobs, jobs_cond, lower_bound
    if (job.status == dispy.DispyJob.Finished or job.status in (dispy.DispyJob.Terminated, dispy.DispyJob.Cancelled, dispy.DispyJob.Abandoned)):
        # 'pending_jobs' is shared between two threads, so access it with
        # 'jobs_cond' (see below)
        jobs_cond.acquire()
        if job.id: # job may have finished before 'main' assigned id
            pending_jobs.pop(job.id)
            if len(pending_jobs) <= lower_bound:
                jobs_cond.notify()
        jobs_cond.release()
def mainLogic(password, wordList, hashMode):
    """Control logic for submitting jobs to cluster while in wordList mode"""
    global pending_jobs, jobs_cond, lower_bound
    #win = False
    hashType = getHashType(password, hashMode)
    lower_bound, upper_bound = 3, 5

    # 'job_callback' is executed in another thread
    jobs_cond = threading.Condition()
    cluster = dispy.JobCluster(crackPwd, ip_addr='10.0.0.12', callback=job_callback)
    pending_jobs = {}
    fin_jobs=[]
    chunkList = splitListIntoTasks(wordList)
    #TIME_START
    for line in chunkList:
        job = cluster.submit(line, hashType, password)
        jobs_cond.acquire()
        # there is a chance the job may have finished and job_callback called by
        # this time, so put it in 'pending_jobs' only if job is pending
        if job.status == dispy.DispyJob.Created or job.status == dispy.DispyJob.Running:
            pending_jobs[job.id] = job
            if len(pending_jobs) >= upper_bound:
                while len(pending_jobs) > lower_bound:
                    jobs_cond.wait()
        jobs_cond.release()
        fin_jobs.append(job)
    cluster.wait()
    for row in fin_jobs:
        paswd = row
        value = paswd.result
        if value:
            cluster.stats()
            cluster.close()
            #TIME_STOP
            winScreen(value, password)

    print ("Unable to crack", password, "using the method you selected")
    restart = input("Do you want to crack another hash/retry hash using another method?(y/n): ")
    cluster.close()
    if restart == "y" or restart == "Y":
        menuMode()
    else:
        exit()



def menuMode():
    """Main menu function"""
    print (" ")
    print ("The Incredible Machine")
    print (" ")
    while True:
        password = input("Enter the hash that is going to be cracked: ")
        print (password)
        enterHash = input("Is this the correct hash?(y/n): ")
        if enterHash == "y" or enterHash == "Y":
            break
    while True:
        hashWhat = input("Enter 1 for entering hash type manually, or Enter 2 to attempt to automatically determine hash type using hash identifier: ")
        if hashWhat == "1":
            hashMode = 1
            break
        elif hashWhat == "2":
            hashMode = 2
            break

    while True:
        programType = input("Enter 1 for Wordlist mode or Enter 2 for Bruteforce mode(or 0 for quit): ")
        if programType == "1":
            while True:
                listType = input("Enter 1 for Default Wordlist or Enter 2 for Custom Wordlist(You need to provide the list)(or 0 to go back): ")
                if listType == "1":
                    wordList = modeList("1000-000-passwords.txt")
                    mainLogic(password, wordList, hashMode)
                elif listType == "2":
                    wordList = modeCustom()
                    mainLogic(password, wordList, hashMode)
                elif listType == "0":
                    break
        elif programType == "2":
            hashType = getHashType(password, hashMode)
            generateBrute(password, hashType)
        elif programType == "0":
            exit()

def modeCustom():
    """Function for collecting custom wordlist"""
    while True:
        wordList = input("Please enter the name of your wordlist file(only .txt file is accepted): ")
        exists = os.path.isfile(wordList)
        if exists:
            break
        else:
            print("The file you entered does not exist or is not in the same folder as this program")
    readlist = open(wordList, 'r', encoding="utf-8", errors="replace")
    wordlist = readlist.readlines()
    readlist.close()
    return wordlist




menuMode()
