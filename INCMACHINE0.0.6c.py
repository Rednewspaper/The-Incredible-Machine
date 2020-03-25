import dispy
import threading
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
    wordList = open("worst-passwords-2017.txt", 'r').readlines()
    return wordList


def splitListIntoTasks(wordList):
    """Returns given_list split into chunks
    Given_list is handed to function by selectMode()
    """

    chunkList = []
    nodeCount = countNodes()
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

def crackLinePwd(line, hashType, password):
    testHash = None
    item = line.strip()
    if hashType == "MD5":
        testHash = hashlib.md5(item.encode('utf-8')).hexdigest()
    elif hashType == "SHA512":
        testHash = hashlib.sha512(item.encode('utf-8')).hexdigest()
    if testHash == password:
        return item
    else:
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
            return item
    return False


def getHashType(password, hashMode):
    """This function determines the hash type(using hashid: https://github.com/psypanda/hashID)
    Return hashType"""
    hashType = None
    if hashMode == 1:
        while True:
            hashType = input("Enter hash type(only MD5 and SHA-256):")
            if hashType == "MD5" or hashType == "SHA-256":
                hashType
                break

    elif hashMode == 2:
        data = open('hashType.txt', 'w+')
        command = 'python3 hashid.py' + ' -m -o hashType.txt \'' + password + '\''
        os.system(command)

        for line in data:
            if 'MD5' in line:
                hashType = 'MD5'

            elif 'SHA-256' in line:
                hashType = 'SHA-256'

        data.close()
        os.remove('hashType.txt')
        hashType = 'MD5'  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return hashType




def generateBruteWordlist():
    #Insert function for determining what charset to use and depth (password length ) it should be
    #Insert function that uses determined parameters to create such a wordlist
    print ("Under construction")
    menuMode()

def winScreen(pswd, passHash):
    print ("Victory")
    print (passHash, "=", pswd)
    
    restart = input("Do you want to crack another hash/retry hash using another method?(y/n):")
    if restart == "y" or restart == "Y":
        menuMode()
    else:
        exit()

def job_callback(job): # executed at the client
    global pending_jobs, jobs_cond, lower_bound
    if (job.status == dispy.DispyJob.Finished or job.status in (dispy.DispyJob.Terminated, dispy.DispyJob.Cancelled, dispy.DispyJob.Abandoned)):
        # 'pending_jobs' is shared between two threads, so access it with
        # 'jobs_cond' (see below)
        jobs_cond.acquire()
        if job.id: # job may have finished before 'main' assigned id
            pending_jobs.pop(job.id)
            # dispy.logger.info('job "%s" done with %s: %s', job.id, job.result, len(pending_jobs))
            if len(pending_jobs) <= lower_bound:
                jobs_cond.notify()
        jobs_cond.release()
def mainLogic(password, wordList, hashMode):
    global pending_jobs, jobs_cond, lower_bound
    win = False
    hashType = getHashType(password, hashMode)
    password = "5c7686c0284e0875b26de99c1008e998"
    lower_bound, upper_bound = 50, 100




    # use Condition variable to protect access to pending_jobs, as
    # 'job_callback' is executed in another thread
    jobs_cond = threading.Condition()
    cluster = dispy.JobCluster(crackLinePwd, ip_addr='10.0.0.1', callback=job_callback)
    pending_jobs = {}
    # submit 1000 jobs
    
    for line in wordList:
        job = cluster.submit(line, hashType, password)
        jobs_cond.acquire()
        # there is a chance the job may have finished and job_callback called by
        # this time, so put it in 'pending_jobs' only if job is pending
        if job.status == dispy.DispyJob.Created or job.status == dispy.DispyJob.Running:
            pending_jobs[job.id] = job
            # dispy.logger.info('job "%s" submitted: %s', i, len(pending_jobs))
            if len(pending_jobs) >= upper_bound:
                while len(pending_jobs) > lower_bound:
                    jobs_cond.wait()
        jobs_cond.release()

        paswd = job()
        if paswd:
            winScreen(paswd, password)
        
    cluster.wait()
    cluster.print_status()
    cluster.close() 
     
    print ("Unable to crack", password, "using the method you selected")

    restart = input("Do you want to crack another hash/retry hash using another method?(y/n):")
    if restart == "y" or restart == "Y":
        menuMode()
    else:
        exit()

    cluster.wait()
    cluster.print_status()
    cluster.close()
def mainOldLogic(password, wordList, hashMode):

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
        hashWhat = input("Enter 1 for entering hash type or Enter 2 for using hash identifier")
        if hashWhat == "1":
            hashMode = 1
            break
        elif hashWhat == "2":
            hashMode = 2
            break

    while True:
        programType = input("Enter 1 for Wordlist mode or Enter 2 for Bruteforce mode(or 0 for quit):")
        if programType == "1":
            while True:
                listType = input("Enter 1 for Default Wordlist or Enter 2 for Custom Wordlist(You need to provide the list)(or 0 to go back):")
                if listType == "1":
                    wordList = modeList()
                    mainLogic(password, wordList, hashMode)
                elif listType == "2":
                    wordList = modeCustom()
                    mainLogic(password, wordList, hashMode)
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
