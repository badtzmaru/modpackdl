from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
import os

chromeOptions = Options()
chromeOptions.add_argument("--kiosk")
browser = webdriver.Chrome(chrome_options=chromeOptions)
#browser.get("https://minecraft.curseforge.com/mc-mods")
#gameVerSelect = browser.find_element_by_id("filter-game-version")
#gameVerOption = browser.find_elements_by_class_name("game-version-type")[0]
#gameVerSelect.click()
#gameVerOption.click()
for x in range(0, 9):
    pageUrl = "https://minecraft.curseforge.com/mc-mods?filter-game-version=1738749986:628&filter-sort=popularity&page=" + str(x)
    for y in range(0, 19):
        browser.get(pageUrl)
        modList = browser.find_elements_by_class_name("overflow-tip")
        modList[y].click()
        modName = browser.find_elements_by_class_name("overflow-tip")[0].text
        modId = browser.find_elements_by_class_name("info-data")[0].text
        with open('aliases.csv','wb') as file:
            file.write(modName + ", " + modId + "\n")
browser.close()