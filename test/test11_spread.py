# builder:wstki
# 开发时间21:03,2024/2/2
# name:test11_spread
# 通过获取一个城市中的受限制的300个poi，通过html链接中的其他poi的id进行不断的扩张
from functions.function_06_getHTML import html_crawler
from bs4 import BeautifulSoup



# 1 首先是打开一个已经存在的poi的链接，得到其html
url = 'https://www.mafengwo.cn/poi/3474.html'
html_content = html_crawler(url)
# 2 先获取这个html中的一些重要的信息
# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 概况
summary =soup.find('div', class_='summary')
# 提取文字内容，并去除换行符
text_content = summary.get_text(strip=True)

# POI地址
# 找到class为mhd的div元素
mhd_div = soup.find('div', class_='mhd')
# 找到p元素，并提取文本内容
address = mhd_div.find('p', class_='sub').get_text(strip=True)



print('end')
