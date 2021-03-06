'HW 13 Dictionary Attack Josh Sapirstein Joe Giuliani'
'Created: 4/27/22'
'Last Modified: 5/2/22'

#############################################################################################################################
##Imports
import hashlib
import time
from itertools import permutations, product, combinations_with_replacement
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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

# Statistics containers
userPasses       = []
passesCalcTimes  = []
SHA256MatchTimes = []
SHA512MatchTimes = []
SHA256NumGuesses = []
SHA512NumGuesses = []

# Begin user input
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

    duration = time.perf_counter()-startTime
    passesCalcTimes.append(duration)
    print("Calculated potential passwords in: ", duration, "seconds")

    startTime = time.perf_counter()
    for i in range(len(potentialPasses)):
        if hashSHA256(potentialPasses[i]) == userSHA256:
            duration = time.perf_counter()-startTime
            SHA256MatchTimes.append(duration)
            SHA256NumGuesses.append(i+1)
            print("SHA256 found in", duration, "seconds:", potentialPasses[i])
            break

    startTime = time.perf_counter()
    for i in range(len(potentialPasses)):
        if hashSHA512(potentialPasses[i]) == userSHA512:
            duration = time.perf_counter()-startTime
            SHA512MatchTimes.append(duration)
            SHA512NumGuesses.append(i+1)
            print("SHA512 found in", duration, "seconds:", potentialPasses[i])
            break

    print()

# End user input

# Plot program statistics

fig = plt.figure()
fig.suptitle("500-word dictionary", fontsize=14)

ax1 = plt.subplot(321)
plt.scatter(userPasses, passesCalcTimes)
plt.xlabel("Password")
plt.ylabel("Passwords Calculation Time in Seconds")
# Removes scientific notation
ax1.xaxis.get_offset_text().set_visible(False)
ax1.yaxis.get_offset_text().set_visible(False)

ax2 = plt.subplot(322)
plt.scatter(userPasses, SHA256MatchTimes)
plt.xlabel("Password")
plt.ylabel("SHA256 Crack Time in Seconds")
ax2.xaxis.get_offset_text().set_visible(False)
ax2.yaxis.get_offset_text().set_visible(False)

ax3 = plt.subplot(323)
plt.scatter(userPasses, SHA512MatchTimes)
plt.xlabel("Password")
plt.ylabel("SHA512 Crack Time in Seconds")
ax3.xaxis.get_offset_text().set_visible(False)
ax3.yaxis.get_offset_text().set_visible(False)

ax4 = plt.subplot(324)
plt.scatter(userPasses, SHA256NumGuesses)
plt.xlabel("Password")
plt.ylabel("SHA256 Number of Guesses")
ax4.xaxis.get_offset_text().set_visible(False)
ax4.yaxis.get_offset_text().set_visible(False)

ax5 = plt.subplot(325)
plt.scatter(userPasses, SHA512NumGuesses)
plt.xlabel("Password")
plt.ylabel("SHA512 Number of Guesses")
ax5.xaxis.get_offset_text().set_visible(False)
ax5.yaxis.get_offset_text().set_visible(False)

plt.show()
