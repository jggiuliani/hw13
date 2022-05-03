# HW13 Dictionary Attack Documentation 
Josh Sapirstein, Joe Giuliani

This program is a demonstration of the ability of a dictionary attack to pursue unlocking access to an account secured by a password. It reveals how the length of a password and its hash type relate to the password’s security and how quickly a threat can have access to your personal information, financials and even gain control over your life.

The program begins by prompting the user for passwords in the console. Each password is assumed to be made up of words from the dictionary file. After each password is entered, the SHA256 and SHA512 hash for the password is printed. The program hashes all possible combinations of words from the dictionary which match the password length with SHA256 and SHA512. If a potential password’s hash matches the user’s password’s hash of the same hash type, the password match and find time is printed. Once the user is done entering passwords, he/she enters “q” into the console. The program then presents graphs of the program’s statistics, like dictionary size, time taken to create potential passwords, time taken to match potential passwords to the user’s password’s hashes, etc

How to run (assuming you have Python3 installed on your computer and are running Windows):
    1. Extract the contents of the program’s zip file
    2. Open Command Prompt or Windows PowerShell, navigate to the directory where you extracted the zip file to
    3. Type “python3 dictattk.py”
    4. You will be prompted for a password. You may enter a password of any length so long as it only contains words from words500.txt. When you are done typing the password, press enter.
    5. The program will output the SHA256 and SHA512 hashes of your password as well as how long it took to crack them.
    6. You may continue entering passwords as you please. Once you are done, enter “q” when prompted for a password.
    7. Once quit, the program will display plots of the dictionary attacks that include various statistics about the dictionary attacks.
