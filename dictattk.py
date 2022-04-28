'HW 13 Dictionary Attack Josh Sapirstein Joe Giuliani'
'Created: 4/27/22'
'Last Modified: 4/27/22'
#############################################################################################################################
##Imports
import hashlib



#############################################################################################################################
##Functions for the use of the program

#Creates the dictionary
def makeDict(fileName):
    wordDict = {}
    with open(fileName) as file:
        for line in file:
 
            (key, value) = line.split(' ')
            wordDict[int(key)] = value.rstrip("\n")
    #print ('\nContents=\n',wordDict)
    return wordDict
    
#Checks if the word exists within the dictionary
def validWordCheck(word, wordDict):
    if word in wordDict.values():
        return True
    else:
        return False

#Creates the password    
def getPassword():
    password = ""
    quantity = input("How many words are going to be within your password (1-4): ")
    count = 0
    
    if (quantity == 1):
        word = input("Enter in the word for your password: ")
        while (validWordCheck(word, wordDict) != True):
            print("Word is invalid!")
            word = input("Enter in the word for your password: ")
        password += word
        #print(password)
        return password
    if (quantity > 1):
        while (count < quantity):
            word = input("Enter in the words for your password,\nEnter in one by one in the order you wish for them to appear: ")
            while (validWordCheck(word, wordDict) != True):
                print("Word is invalid!")
                word = input("Enter in the word for your password: ")
            password += word
            count += 1
        #print(password)
        return password
    

#Hashes the password using SHA256  
def hashSHA256(password):
    hashed = password.encode()
    h = hashlib.sha256(hashed)
    final = h.hexdigest()
    #print("Encoded password: " + final)
    return final

#Hashes the password using SHA512
def hashSHA512(password):
    hashed = password.encode()
    h = hashlib.sha512(hashed)
    final = h.hexdigest()
    #print("Encoded password: " + final)
    return final

def attack():
    ##NEED TO FINISH
    return True
#############################################################################################################################    

wordDict = makeDict("wordsSmall.txt")
password = getPassword()
hashSHA256(password)
hashSHA512(password)





