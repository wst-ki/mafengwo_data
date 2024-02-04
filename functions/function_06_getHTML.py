# builder:wstki
# 开发时间21:11,2024/2/2
# name:function_06_getHTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def html_crawler(url, max_retries=3):
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

    retry_count = 0
    while retry_count < max_retries:
        try:
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
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//title[contains(text(),'马蜂窝')]"))
            )

            # 获取页面 HTML 内容
            html_content = driver.page_source
            driver.quit()

            return html_content

        except Exception as e:
            print(f"页面加载失败，正在第 {retry_count + 1} 次重试: {e}")
            retry_count += 1

            # 可以在此处添加额外的等待时间或其他策略
            # 例如，您可能希望在重试之前等待几秒钟
            driver.quit()
            continue

    print(f"无法加载页面，已达到最大重试次数")
    return None