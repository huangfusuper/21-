from selenium import webdriver
import time
driver_path = r'../chromedriver.exe'
#打开浏览器
driver = webdriver.Chrome(executable_path=driver_path)
#输入网址
driver.get("https://www.baidu.com/")
#获取cookis
# for coo in driver.get_cookies():
#     print(coo)
#打开一个新标签
driver.execute_script("window.open('https://www.douban.com/')")
#driver.current_url 获取网址
#将句柄切换到新标签中，不切换的话  获取的源代码等信息还是之前那个标签的
driver.switch_to.window(driver.window_handles[1])
# print(driver.current_url )
#关闭当前句柄的标签
driver.close()
#关闭浏览器
time.sleep(3)
driver.quit()


