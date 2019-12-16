from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import io
import sys
driver_url = r"./chromedriver.exe"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
driver = webdriver.Chrome(executable_path=driver_url)
driver.get("https://www.baidu.com")
acctons = ActionChains(driver)

inputTag = driver.find_element_by_id('kw')
submitTag = driver.find_element_by_id('su')

acctons.move_to_element(inputTag)
acctons.send_keys_to_element(inputTag,'huangfu')
acctons.move_to_element(submitTag)
acctons.click(submitTag)
acctons.perform()
