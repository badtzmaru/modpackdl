#import dependencies
import sys, os, csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#read in mod archive
if(os.path.isfile('./buildAliases/aliases.csv')):
    mods = []
    with open('./buildAliases/aliases.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            mods.append(row);
else:
    print("No database found, please run build.py before attempting to download")
    os._exit(0)

#clear function
clear = lambda: os.system('cls')

clear()

#setup fuzzy matching
fuzzyBool = 0
choices = []
for i in range(0,len(mods)):
    choices.append(mods[i][0])

#adds mods to the file
def addMod(modName):
    with open(sys.argv[1], 'a') as file:
        file.write(modName)
        file.write("\n")
    print("Mod added!")

#check arguments
if(len(sys.argv) == 1):
    print("Output file must be specified!")
    os._exit(0)
elif(len(sys.argv) > 2):
    for i in range(1, len(sys.argv)):
        if(sys.argv[i] == "-f" or sys.argv[i] == "-fuzzy"):
            fuzzyBool = 1
            print("Fuzzy matching enabled.")
        elif(sys.argv[i] == "-o" or sys.argv[i] == "-overwrite"):
            if(os.path.isfile(sys.argv[1])):
                os.remove(sys.argv[1])
            print("File overwritten!")

#main loop
print("\nWelcome to the packbuilder! \nType a mod name and press enter to add!\nType \"done\" to end")
inputString = ""
modCount = 0
while(inputString != "done"):
    inputString = raw_input()
    if(inputString == "done"):
        break
    if(fuzzyBool == 0):
        if(inputString in choices):
            addMod(inputString)
            modCount = modCount + 1
        else:
            print("Mod not found!");
    elif(fuzzyBool == 1):
        result = process.extractOne(inputString, choices)
        if(result[1]>=80):
            addMod(result[0])
            modCount = modCount + 1
        else:
            print("Mod not found!")
print("Added " + str(modCount) + " mods to " + sys.argv[1])