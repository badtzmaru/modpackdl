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
browser.get("https://minecraft.curseforge.com/mc-mods")
#gameVerSelect = browser.find_element_by_id("filter-game-version")
#gameVerOption = browser.find_elements_by_class_name("game-version-type")[0]
#gameVerSelect.click()
#gameVerOption.click()
parentElement = browser.find_elements_by_class_name("overflow-tip")[0]
elementList = parentElement.find_element_by_tag_name("a").get_attribute("href")

if(len(sys.argv) != 2):
    pages = 50
else:
    pages = int(sys.argv[1])
modList = []
modComplete = []
for x in range(0, pages):
    pageUrl = "https://minecraft.curseforge.com/mc-mods?filter-game-version=1738749986:628&filter-sort=popularity&page=" + str(x+1)
    browser.get(pageUrl)
    for y in range(0, 20):
        parentElement = browser.find_elements_by_class_name("overflow-tip")[y]
        modList.append(parentElement.find_element_by_tag_name("a").get_attribute("href"))
for i in range(0, len(modList)):
    browser.get(modList[i])
    modName = browser.find_elements_by_class_name("overflow-tip")[0].text
    modId = browser.find_elements_by_class_name("info-data")[0].text
    modComplete.append(str(modName).encode('utf-8') + "," + str(modId) + "\n")
modComplete.sort()
with open('aliases.csv','w') as file:
   file.writelines(modComplete)
browser.close()

