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
            
# Prompts the user for a password made up of 1-4 words from the dictionary
def promptUserForPassword():
    password = ""
    quantity = int(input("How many words are going to be within your password (1-4): "))
    count = 0

    while (count < quantity):
        word = input("Enter in the words for your password, return after each word\n")
        while (word not in dictionary):
            print("Word is invalid, try again\n")
            word = input("Enter in the word for your password: ")
        password += word
        count += 1

    return password

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

## Driver code

dictionary = readDictionary("words500.txt")

password = promptUserForPassword(dictionary)
password_length = len(password)
passwordSHA256 = hashSHA256(password)
passwordSHA512 = hashSHA512(password)

startTime = time.perf_counter()

potentialPasswords = []

# Generate a list of combinations of available word lengths from the dictionary whose
# sums equal the password length
lengthCombos = sumCombos(dictionary.keys(), password_length)

for lengthCombo in lengthCombos:

    # Generates word combinations based on the word length combination 
    for wordCombo in wordCombos(lengthCombo):
        
        # Creates a list of purely strings out of those in wordCombo
        words = []
        extractStrings(wordCombo, words)

        # Converts the permutations of wordCombo to single strings and them to potential passwords
        for permu in set(permutations(words, password_length)):
            potentialPasswords.append("".join(permu))

print("Calculation of potential passwords took: ", time.perf_counter()-startTime, "seconds")

startTime = time.perf_counter()
for p in potentialPasswords:
    if hashSHA256(p) == passwordSHA256:
        break
print("User's password's SHA256 hash found in", time.perf_counter()-startTime, "seconds")

startTime = time.perf_counter()
for p in potentialPasswords:
    if hashSHA512(p) == passwordSHA512:
        break
print("User's password's SHA512 hash found in", time.perf_counter()-startTime, "seconds")
