# builder:wstki
# 开发时间16:06,2024/2/2
# name:test_headless
# 无头的浏览器测试一下
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 配置
ch_options = Options()
ch_options.add_argument("--headless")
ch_options.add_experimental_option('excludeSwitches', ['enable-automation'])
ch_options.add_experimental_option('useAutomationExtension', False)

# 在启动浏览器时加入配置
driver = webdriver.Chrome(options=ch_options)

url = 'http://www.mafengwo.cn/poi/3474.html'
driver.get(url)

# 使用显式等待等待元素出现（这里以页面标题为例）
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//title[contains(text(),'马蜂窝')]"))
    )
except Exception as e:
    print(f"等待页面加载超时: {e}")

# 执行反爬虫手段
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """
})

# 获取页面 HTML 内容
html_content = driver.page_source

# 将 HTML 内容保存到文件
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# 等待一段时间确保页面加载完成
time.sleep(2)

# 截图
driver.save_screenshot('./ch.png')

driver.quit()