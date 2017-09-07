from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
import os
import sys

chromeOptions = Options()
#chromeOptions.add_argument("--kiosk")
browser = webdriver.Chrome(chrome_options=chromeOptions)
try:
    os.remove("aliases.csv")
except OSError:
    pass
#browser.get("https://minecraft.curseforge.com/mc-mods")
#gameVerSelect = browser.find_element_by_id("filter-game-version")
#gameVerOption = browser.find_elements_by_class_name("game-version-type")[0]
#gameVerSelect.click()
#gameVerOption.click()
if(len(sys.argv) != 2):
    pages = 50
else:
    pages = int(sys.argv[1])
modlist = []
for x in range(0, pages):
    pageUrl = "https://minecraft.curseforge.com/mc-mods?filter-game-version=1738749986:628&filter-sort=popularity&page=" + str(x+1)
    for y in range(0, 20):
        browser.get(pageUrl)
        modList = browser.find_elements_by_class_name("overflow-tip")
        modList[y].click()
        modName = browser.find_elements_by_class_name("overflow-tip")[0].text
        modId = browser.find_elements_by_class_name("info-data")[0].text
        modlist.append(str(modName) + "," + str(modId) + "\n")
modlist.sort()
with open('aliases.csv','w') as file:
    file.writelines(modlist)
browser.close()