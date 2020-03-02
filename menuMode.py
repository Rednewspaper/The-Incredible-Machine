def menuMode():
    
    while True:
        programType = input("Enter 1 for Wordlist mode or Enter 2 for Bruteforce mode(or 0 for quit):")
        if programType == "1":
            while True:
                listType = input("Enter 1 for Default Wordlist or Enter 2 for Custom Wordlist(You need to provide the list)(or 0 to go back):")
                if listType == "1":
                    wordList = modeCustom()
                    mainLogic(password, wordList)
                elif listType == "2":
                    wordList = modeList()
                    mainLogic(password, wordList)
                elif listType == "0":
                    break
        elif programType == "2":
            wordList = generateBruteWordlist()
            mainLogic(password, wordList)
        elif programType == "0":
            break
