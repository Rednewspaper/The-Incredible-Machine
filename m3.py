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

    print (nodeCount)
    print (len(wordList))
    print (equalChunks)
    print (chunkSize)
    print (chunkList)
    for x in chunkList:
        for y in x:
            y = y.strip()
            print (y)

def readList():
    """Function for selecting and reading wordlist"""
    wordList = open("worst-passwords-2017.txt", 'r').readlines()
    return wordList


def countNodes():
    return 3

tryList = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

splitListIntoTasks(readList())

