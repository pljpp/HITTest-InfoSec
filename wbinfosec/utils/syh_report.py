import re
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import json
import time

# 2_201涉黄信息_色情导流 15_1510违法信息_诈骗 41_4107涉未成年人_伤害未成年人 42_4205饭圈违规_造谣爆料 44_4404侵权行为_其他侵权行为
def report(class_id,tag_id,blogid):
    # 使用插件
    wb = webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chromedriver.exe")
    # 使用如下代码替换上一行时实现无窗口化运行
    # option = webdriver.ChromeOptions()
    #
    # option.add_argument('headless')
    #
    # wb = webdriver.Chrome(chrome_options=option)
    re_url = 'https://service.account.weibo.com/reportspamobile?rid='+blogid+'&type=1'
    # 隐式地等待
    wb.implicitly_wait(3)
    wb.maximize_window()
    wb.get(re_url)
    time.sleep(5)

    # 向浏览器添加保存的cookies进行登录
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
    #time.sleep(10)
    wb.refresh()

    Xpath1 = "//li[@class_id='"+class_id+"']"
    element0 = wb.find_element(By.XPATH,Xpath1)
    print(element0)
    element0.click()

    Xpath2 = "//li[@tag_id='" + tag_id + "']"
    element1 = wb.find_element(By.XPATH,Xpath2)
    print(element1)
    element1.click()

    element2 = wb.find_element(By.XPATH,"//input[@name='chk']")
    print(element2)
    element2.click()

    element3 = wb.find_element(By.XPATH,"//a[@href='javascript:void(0);']")
    print(element3)
    ActionChains(wb).move_to_element(element3).click().perform()

    #看一下效果用，可以去掉
    #time.sleep(60)
    # 关闭浏览器
    wb.close()

if __name__ == '__main__':
    blogid = 4906674710119009
    # string 需要投诉的博文链接（分享博文获得）
    string = 'https://weibo.com/7720233260/N1MQV82E4?refer_flag=1001030103_'
    #2_201涉黄信息_色情导流 15_1510违法信息_诈骗 41_4107涉未成年人_伤害未成年人 42_4205饭圈违规_造谣爆料 44_4404侵权行为_其他侵权行为
    #输入string类型
    report('42','4205',blogid)
