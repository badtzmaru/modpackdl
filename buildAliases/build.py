#import dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv, os, sys
import progressbar


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

#setup browser object
chromeOptions = Options()
#chromeOptions.add_argument("--kiosk")
browser = webdriver.Chrome(chrome_options=chromeOptions)

#begin scrape
print("Starting scrape...")
browser.get("https://minecraft.curseforge.com/mc-mods")

parentElement = browser.find_elements_by_class_name("overflow-tip")[0]
elementList = parentElement.find_element_by_tag_name("a").get_attribute("href")


print("Building modlist...")
pageBar = progressbar.ProgressBar()
modBar = progressbar.ProgressBar()
modList = []

for x in pageBar(range(0, pages)):
    pageUrl = "https://minecraft.curseforge.com/mc-mods?filter-game-version=1738749986:628&filter-sort=popularity&page=" + str(x+1)
    browser.get(pageUrl)
    for y in range(0, 20):
        parentElement = browser.find_elements_by_class_name("overflow-tip")[y]
        modList.append(parentElement.find_element_by_tag_name("a").get_attribute("href"))

print("Getting project ids...")
for i in modBar(range(0, len(modList))):
    browser.get(modList[i])
    modName = browser.find_elements_by_class_name("overflow-tip")[0].text
    modId = browser.find_elements_by_class_name("info-data")[0].text
    addMod(str(modName.encode('utf-8')) + "," + str(modId) + "\n")
browser.close()
print("Build complete!")
