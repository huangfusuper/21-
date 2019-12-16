from selenium import webdriver
#设置代理
# chromeOptions = webdriver.ChromeOptions()
# chromeOptions.add_argument("--proxy-server=http://223.199.22.43:9999")
driver_path = r'../chromedriver.exe'
# driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chromeOptions)
driver = webdriver.Chrome(executable_path=driver_path)
driver.get("https://www.baidu.com")
submitBtn = driver.find_element_by_id('su')
print(submitBtn.get_attribute("value"))
#截图当前界面
# driver.save_screenshot('baidu.png')
