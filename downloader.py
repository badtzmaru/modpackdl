#import depedencies
import os, requests, csv, sys, math
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from bs4 import BeautifulSoup

#get list of mods from csv
if(os.path.isfile('./buildAliases/aliases.csv')):
    mods = []
    with open('./buildAliases/aliases.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            mods.append(row);
else:
    print("No database found, please run build.py before attempting to download")
    os._exit(0)

#setup code for fuzzy matching of mod names
fuzzyBool = 0
choices = []
for i in range(0,len(mods)):
    choices.append(mods[i][0])

#create mods directory
if(os.path.isdir("./mods") == False):
    os.mkdir("mods")

#clear function
clear = lambda: os.system('cls')

#converts a mod name to the curseforge project id
def modIdFromName(modName):
    if(fuzzyBool == 0):
        for i in range(0,len(mods)):
            for p in range(0,len(mods[i])-1):
                if(mods[i][p].lower() == modName.lower()):
                    return mods[i][len(mods[i])-1]
        return False
    else:
        result = process.extractOne(modName, choices)
        if(result[1]>=80):
            for i in range(0,len(mods)):
                if (mods[i][0] == result[0]):
                    return mods[i][1]
        return False

#downloads the mods using the curseforge project id
def downloadMod(modId):
    if(modId == False):
        return False
    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'

        r = s.get('https://minecraft.curseforge.com/projects/' + str(modId))
        soup = BeautifulSoup(r.text, 'html.parser')

        modName = soup.find('span', 'overflow-tip').string + '.jar'

        url = 'https://minecraft.curseforge.com/' + soup.find('a', 'button alt fa-icon-download')['href']

        print(modName)

        r = s.get(url, stream=True)

        with open("./mods/" + modName, 'wb') as zipfile:
            for chunk in r.iter_content(chunk_size=1024):
                zipfile.write(chunk)

#handles a modlist text file
def handleModlist(file):
    #begin downloads
    print("Now attempting to download all mods from " + file + ".")
    if(fuzzyBool == 0):
        print("Warning, fuzzy matching disabled, exact modnames must be used. -help for more info")
    modListFromFile = [line.rstrip('\n') for line in open(file)]
    modCount = len(modListFromFile)
    downloadComplete = modCount
    print("\n" + str(modCount) + " mods found.")
    for i in range(0,len(modListFromFile)):
        currentMod = modIdFromName(modListFromFile[i])
        if(currentMod):
            downloadMod(currentMod)
        else:
            print("Sorry, " + modListFromFile[i] + " could not be found.")
            downloadComplete = downloadComplete - 1
    print("\n" + str(downloadComplete) + "/" + str(modCount) + " mods downloaded!")
    if(float(downloadComplete)/float(modCount) < .75):
        print("It seems that you are missing quite a few mods, maybe try using fuzzy matching? -help for more info")

#help printout
def helpText():
    print("~ dl.py ~\nThis is a simple tool to help you download mods from curseforge using a modlist")
    print("Created by PanDoes and Badtz 2017")
    print("Usage:")
    print("dl.py <modlist file> [-fuzzy/-f] [-h]")
    print("-fuzzy / -f: enable fuzzy matching of modnames")
    print("-help / -h: display this help text")
    os._exit(0)

#main
clear()
if (len(sys.argv)>1):
    modListIndex = 0
    for i in range(1,len(sys.argv)):
        if(sys.argv[i] == "-f" or sys.argv[i] == "-fuzzy"):
            fuzzyBool = 1
        elif(sys.argv[i] == "-h" or sys.argv[i] == "-help"):
            helpText()
        elif(os.path.isfile(sys.argv[i])):
            modListIndex = i
    if(modListIndex != 0):
        handleModlist(sys.argv[modListIndex])
    else:
        helpText()
else:
    helpText()