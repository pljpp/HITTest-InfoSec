from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import json
import time

def blog_po(topic,blog):
    # 打开网址
    wb = webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chromedriver.exe")
    # 隐式地等待
    wb.implicitly_wait(3)
    wb.maximize_window()
    wb.get('https://weibo.com')
    time.sleep(5)

    # 向浏览器添加保存的cookies
    try:
        cookies = json.load(open("D:/djangoProject/wbinfosec/utils/cookies.txt", "rb"))
        for cookie in cookies:
            cookie_dict = {
                "domain": cookie.get('domain'),
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": "",
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False}
            wb.add_cookie(cookie_dict)
    except Exception as e:
        print(e)

    ## 刷新
    # time.sleep(10)
    wb.refresh()

    tXpath = "//textarea[@class='Form_input_2gtXx']"
    textarea = wb.find_element(By.XPATH, tXpath)
    print(textarea)
    blog = '#'+topic+'#'+blog
    textarea.send_keys(blog)

    bXpath = "//button[@class='woo-button-main woo-button-flat woo-button-primary woo-button-m woo-button-round Tool_btn_2Eane']"
    button = wb.find_element(By.XPATH, bXpath)
    print(button)
    button.click()

if __name__ == '__main__':
    topic = '苏古怪'
    blog = '苏古怪测试'
    blog_po(topic,blog)