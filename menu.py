def menu():
    while True:
        userInput = input("Enter 1 for Wordlist mode or Enter 2 for Bruteforce mode(1 or 2):")
        try:
            programType = int(userInput)
            if programType == 1 or programType == 2:
                break
            else:
                pass
        except ValueError:
            pass
        
    if programType == 1:
        while True:
            userInput = input("Enter 1 for Default Wordlist or Enter 2 for Custom Wordlist(You need to provide the list)(1 or 2):")
            try:
                listType = int(userInput)
                if listType == 1 or listType == 2:
                    break
                else:
                    pass
            except ValueError:
                pass

        if listType == 1:
            return readList()

        elif listType == 2:
            import os
            while True:
                userInput = input("Please enter the name of your wordlist file(excluding .txt)")
                wordList = " ".join((userInput, ".txt"))
                exists = os.path.isfile(wordList)
                if exists:
                    break
                else:
                    print("The file you entered does not exist or is not in the same folder as this program")
            #Need to add more logic to check if list is "useable"
            wordList = open(wordList, 'r').readlines()
            return wordList

    elif programType == 2:
        while True:
            #Probably needs some more info into what deep means(couldn't describe it good)
            userInput = input("How deep?(integer):")  
            try:
                bruteDeep = int(userInput)
                break
            except ValueError:
                pass
        
        charType = "test"
        return bruteDeep, charType
