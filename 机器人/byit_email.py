from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#行为链
from selenium.webdriver.common.action_chains import ActionChains

driver_path = r'../chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
#隐士等待
#driver.implicitly_wait(20)
driver.get("http://mail.byitgroup.com/")
#显示等待
WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.ID,"usernameTip"))
)
usernameInput = driver.find_element_by_id("usernameTip")
action = ActionChains(driver)
#鼠标悬停到
action.move_to_element(usernameInput)
action.send_keys_to_element(usernameInput,"huangfukexing")
#鼠标悬停到密码框
passInput = driver.find_element_by_id("userType")
action.move_to_element(passInput)
#输入密码
action.send_keys_to_element(passInput,"huangfu123")
#鼠标移动到登录按钮
wmSubBtn = driver.find_element_by_id("wmSubBtn")
action.move_to_element(wmSubBtn)
action.click(wmSubBtn)
action.perform()
#打印网页信息
print(driver.page_source)
# passInput = driver.find_element_by_id("userType")
# passInput.send_keys("huangfu123")
#
# wmSubBtn = driver.find_element_by_id("wmSubBtn")
# wmSubBtn.click()