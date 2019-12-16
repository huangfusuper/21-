
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import io
import sys
import time
driver_url = r"./chromedriver.exe"

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
driver = webdriver.Chrome(executable_path=driver_url)
driver.get("https://www.baidu.com")
inputTag = driver.find_element_by_id('kw')
inputTag.send_keys('java')
submit = driver.find_element_by_id('su')
submit.click()
