'HW 13 Dictionary Attack Josh Sapirstein Joe Giuliani'
'Created: 4/27/22'
'Last Modified: 5/2/22'

#############################################################################################################################
##Imports
import hashlib
import time
from itertools import permutations, product, combinations_with_replacement
#############################################################################################################################

##Functions for the use of the program

# Reads a text file with one word per line
# Returns a dictionary where each key is a word length n and each value list of n-letter words
def readDictionary(fileName: str) -> dict:
    ret = {}
    with open(fileName) as file:
        for line in file:
            word = line.rstrip('\n')
            len_word = len(word)
            if (len_word) in ret.keys():
                ret[len_word].append(word)
            else:
                ret[len_word] = [word]
    
    return ret

# Hashes a string using SHA256  
def hashSHA256(data: str):
    return hashlib.sha256(data.encode()).hexdigest()

# Hashes a string using SHA512
def hashSHA512(data: str):
    return hashlib.sha512(data.encode()).hexdigest()

# Driver function for sumCombosRec
# Sorts values and passes length as the target sum
# Returns a list of the combinations of values whose sum is equal to length
# Assumes values only contains unique elements
def sumCombos(values: list, length: int) -> set:
    ret = []
    sumCombosRec(ret, list(sorted(values)), [], length, 0)
    return ret

# Recursive function that stores in out each combination of values whose sum equals the initial value passed to remaining 
def sumCombosRec(out: list, values: list, combo: int, remaining: int, index: int):
    
    if (remaining == 0):
        out.append(list(combo))
        return
    
    for i in range(index, len(values)):
        if remaining - values[i] >= 0:
            combo.append(values[i])
            sumCombosRec(out, values, combo, remaining-values[i], i)

            # Backtrace
            combo.remove(values[i]) 

# Returns the last position and number of times (respectively) that the value of arr[start]
# consecutively repeats itself in arr starting at index start
def endOfRepitition(start: int, arr: list):
    for i in range(start, len(arr)):
        if arr[i] != arr[start]:
            return i-1, i-start

    return len(arr)-1, len(arr)-start

# Stores all strings found in x in out
# Assumes x is either 1) a string or 2) iterable and contains only iterable and string types
def extractStrings(x, out: list):
    if type(x) == str:
        out.append(x)
        return

    for elem in x:
        extractStrings(elem, out)

# Generates word combinations based on a list of word lengths
def wordCombos(lengths: list) -> list:
    ret = []
    i = 0
    while i < len(lengths):
        currLength = lengthCombo[i]

        # Advances i to one past the index of the last element in lengthCombo matching wordLength
        i, numCurrLength = endOfRepitition(i, lengths)
        i += 1

        combo = list(combinations_with_replacement(dictionary[currLength], numCurrLength))
        if len(ret) == 0:
            ret = combo
        else:
            ret = list(product(ret, combo))

    return ret

## Driver code

dictionary = readDictionary("words500.txt")

userPasses = []

while True:

    # Assumes user enters password using words from dictionary file
    userInput = input("Enter password: ")
    if userInput == "q":
        break

    userPass = userInput
    userPasses.append(userPass)
    passLen = len(userPass)
    userSHA256 = hashSHA256(userPass)
    userSHA512 = hashSHA512(userPass)

    print("SHA256:", userSHA256)
    print("SHA512:", userSHA512)
    print()

    startTime = time.perf_counter()

    potentialPasses = []

    # Generate a list of combinations of available word lengths from the dictionary whose
    # sums equal the password length
    lengthCombos = sumCombos(dictionary.keys(), passLen)

    for lengthCombo in lengthCombos:

        # Generates word combinations based on the word length combination 
        for wordCombo in wordCombos(lengthCombo):
            
            # Creates a list of purely strings out of those in wordCombo
            words = []
            extractStrings(wordCombo, words)

            # Converts the permutations of wordCombo to single strings and them to potential passwords
            for permu in set(permutations(words, len(words))):
                potentialPasses.append("".join(permu))

    print("Calculated potential passwords in: ", time.perf_counter()-startTime, "seconds")

    hashFound = False
    startTime = time.perf_counter()
    for p in potentialPasses:
        if hashSHA256(p) == userSHA256:
            print("SHA256 found in", time.perf_counter()-startTime, "seconds:", p)
            hashFound = True
            break

    if not hashFound:
        print ("SHA256 not found!")

    hashFound = False
    startTime = time.perf_counter()
    for p in potentialPasses:
        if hashSHA512(p) == userSHA512:
            print("SHA512 found in", time.perf_counter()-startTime, "seconds:", p)
            hashFound = True
            break

    if not hashFound:
        print ("SHA512 not found!")