import os, requests, csv
import fuzzywuzzy
from bs4 import BeautifulSoup

def modIdFromName(modName):
    with open('aliases.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:


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

downloadMod(238222)