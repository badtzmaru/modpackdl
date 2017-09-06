from selenium import webdriver
from selenium.webdriver.common.keys import Keys
browser = webdriver.Chrome()
browser.get("https://minecraft.curseforge.com/mc-mods")
modlist = browser.find_elements_by_class_name("overflow-tip")
browser.close()