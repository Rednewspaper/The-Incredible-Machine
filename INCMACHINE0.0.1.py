import dispy

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
    wordList = open("worst-passwords-2017.txt", 'r')
    newWordList =[]
    wordCount = 0
    for line in wordList.readline():
        line = line.strip()
        newWordList.append(line)
        count += 1
    return newWordList, wordCount


def splitListIntoTasks(wordList, wordCount, count_nodes):
    """Returns given_list split into chunks
Given_list can be an actual given wordlist
Brute is a boolean, default false.
If brute is true this function will generate a wordlist then split that as appropriate (might be more modular to just have brute as it’s own function that gets called from splitting, that collects what the char set is, then generates and returns the wordlist
"""

    #Insert function that splits a wordList into pieces of 10 lines (1000 in proper, but when testing with 100 word wordlist)

def crackPwd(chunk, hashType, password):
    """This is the function that is sent to the nodes"""
    #Insert haslib matching function (similar to youtube video)



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
for chunk in wordList:
    cluster = dispy.JobCluster(crackPwd(chunk, hashType, password))

#More logic needed down here regarding canceling jobs when we have found the password

a=input()
