# builder:wstki
# 开发时间21:11,2024/2/2
# name:function_06_getHTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def html_crawler(url):
    '''
    输入的是一个网址，输出是这个网页的源代码
    :param url:
    :return:
    '''
    # 配置
    ch_options = Options()
    # 开启无头模式
    ch_options.add_argument("--headless")
    ch_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    ch_options.add_experimental_option('useAutomationExtension', False)

    # 在启动浏览器时加入配置
    driver = webdriver.Chrome(options=ch_options)



    # 执行反爬虫手段
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    driver.get(url)
    # 使用显式等待等待元素出现（这里以页面标题为例）
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//title[contains(text(),'马蜂窝')]"))
        )
    except Exception as e:
        print(f"等待页面加载超时: {e}")
    # 获取页面 HTML 内容
    html_content = driver.page_source
    driver.quit()

    return html_content