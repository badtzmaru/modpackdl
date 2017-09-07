from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

chromeOptions = Options()
chromeOptions.add_argument("--kiosk")
browser = webdriver.Chrome(chrome_options=chromeOptions)
browser.get("https://minecraft.curseforge.com/mc-mods")
modList = browser.find_elements_by_class_name("overflow-tip")
modList[0].click()
modName = browser.find_elements_by_class_name("overflow-tip")[0].text
modId = browser.find_elements_by_class_name("info-data")[0].text
print(modName)
print(modId)
browser.close()