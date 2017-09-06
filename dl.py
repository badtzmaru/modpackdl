#import depedencies
import os, requests, csv
import fuzzywuzzy
from bs4 import BeautifulSoup

#get list of mods from csv
mods = []
with open('aliases.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        mods.append(row);

#converts a mod name to the curseforge project id
def modIdFromName(modName):
    for i in range(0,len(mods)):
        if(mods[i][0] == modName):
            return mods[i][1]

#downloads the mods using the curseforge project id
def downloadMod(modId):
    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'

        r = s.get('https://minecraft.curseforge.com/projects/' + str(modId))
        soup = BeautifulSoup(r.text, 'html.parser')

        url  = soup.find('a', 'button alt fa-icon-download')['href']

        modName = soup.find('span', 'overflow-tip').string + '.jar'

        url = 'https://minecraft.curseforge.com/' + url
        print("Now downloading: " + str(modName))

        r = s.get(url, stream=True)

        with open(os.path.basename(modName), 'wb') as zipfile:
            for chunk in r.iter_content(chunk_size=1024):
                zipfile.write(chunk)

downloadMod(modIdFromName("jei"))