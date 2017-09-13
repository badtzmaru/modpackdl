#import dependencies
import csv, os, sys, requests
import progressbar
from bs4 import BeautifulSoup


#handle command line arguments
if(len(sys.argv) == 1):
    pages = 50
elif(sys.argv[1] == "-h" or sys.argv[1] == "-help"):
    print("~ build.py ~\nThis is a simple tool to help you build a list of all the mod names and project ids")
    print("Note that chrome may have to be maximized to funtion correctly")
    print("Created by PanDoes and Badtz 2017")
    print("Usage:")
    print("build.py <pageCount> [-help/-h]")
    print("pageCount: the number of pages of mods to add to the csv, default is 50")
    print("-help / -h: display this help text")
    os._exit(0)
else:
    pages = int(sys.argv[1])

#remove old csv
try:
    os.remove("aliases.csv")
except OSError:
    pass

#adds mods to the file
def addMod(modName):
    with open("aliases.csv", 'a') as file:
        file.write(modName)

#begin scrape
print("Building modlist...")
pageBar = progressbar.ProgressBar()
modBar = progressbar.ProgressBar()
modList = []

with requests.session() as browser:
    browser.headers['user-agent'] = 'Mozilla/5.0'

    for x in pageBar(range(0, pages)):
        pageUrl = "https://minecraft.curseforge.com/mc-mods?filter-game-version=1738749986:628&filter-sort=popularity&page=" + str(x+1)
        r = browser.get(pageUrl)
        soup = BeautifulSoup(r.text, 'html.parser')
        parentElement = soup.find('div', {'class': 'overflow-tip'})
        children = parentElement.findChildren()
        for y in range(0,len(children)): 
            modList.append(children[y]['href'])

    print("Getting project ids...")
    for i in modBar(range(0, len(modList))):
        r = browser.get("https://minecraft.curseforge.com" + modList[i])
        soup = BeautifulSoup(r.text, 'html.parser')
        modName = soup.find('span', {'class': 'overflow-tip'}).string
        modId = soup.find('div', {'class': 'info-data'}).string
        print(modName)
        print(modId)
        addMod(str(modName.encode('utf-8')) + "," + str(modId) + "\n")

    print("Build complete!")