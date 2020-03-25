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
