from selenium import webdriver
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome()
browser.get("https://minecraft.curseforge.com/mc-mods")
modList = browser.find_elements_by_class_name("overflow-tip")
modList[0].click()
modName = browser.find_element_by_class_name("overflow-tip").text
modId = browser.find_elements_by_class_name("info-data")
print(modName)
print(modId[0])
browser.close()