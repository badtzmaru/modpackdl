#import depedencies
import os, requests, csv, sys
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

if(os.path.isdir("./mods") == False):
    os.mkdir("mods")

#clear function
clear = lambda: os.system('cls')

#converts a mod name to the curseforge project id
def modIdFromName(modName):
    #for i in range(0,len(mods)):
        #for p in range(0,len(mods[i])-1):
            #if(mods[i][p].lower() == modName.lower()):
                #return mods[i][len(mods[i])-1]
    #return False

    choices = []
    for i in range(0,len(mods)):
        choices.append(mods[i][0])
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

        print("Now downloading: " + str(modName))

        r = s.get(url, stream=True)

        with open("./mods/" + modName, 'wb') as zipfile:
            for chunk in r.iter_content(chunk_size=1024):
                zipfile.write(chunk)

#main
clear()
if (len(sys.argv)>1):
    modListFromFile = [line.rstrip('\n') for line in open(sys.argv[1])]
    print(str(len(modListFromFile)) + " mods found.")
    for i in range(0,len(modListFromFile)):
        currentMod = modIdFromName(modListFromFile[i])
        if(currentMod):
            downloadMod(currentMod)
        else:
            print("Sorry, " + modListFromFile[i] + " could not be found")