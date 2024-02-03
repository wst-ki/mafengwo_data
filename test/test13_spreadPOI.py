# builder:wstki
# 开发时间10:37,2024/2/3
# name:test13_spreadPOI
from functions.function_05_getPOIID import _get_route
import pandas as pd
import os
from functions.function_06_getHTML import html_crawler
from bs4 import BeautifulSoup
from functions.function_07_getComment import crawler_comment
# 先封装一个获取评论的函数

# 以广州为例，获取广州的POI数据
cityID_list = [10088]
csv_path = f'../cache/{10088}.csv'
if  not os.path.exists(csv_path):
    for cityID in cityID_list:
        _get_route(cityID)
        results, df = _get_route(cityID)
        print(df)
        df.to_csv(f'../cache/{cityID}.csv', index=False)
else:
    print(f'{csv_path} 文件已存在')
    pass
df = pd.read_csv(csv_path)
link_col =df['link']
link_col = link_col.dropna()
for link in link_col:

    POI = df.loc[df['link'] == link, 'poi_id'].iloc[-1]

    html_content = html_crawler(link)


    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 概况
    summary = soup.find('div', class_='summary')
    # 提取文字内容，并去除换行符
    text_content = summary.get_text(strip=True)

    # POI地址
    # 找到class为mhd的div元素
    mhd_div = soup.find('div', class_='mhd')
    # 找到p元素，并提取文本内容
    address = mhd_div.find('p', class_='sub').get_text(strip=True)

    # 获取POI评论数量
    # 找到包含评价数量的<span>标签
    # 找到包含评价数量的<span>标签
    span_tag = soup.find('span', class_='count')

    # 提取评价数量

        # 评论的页数
    review_count_page = int(span_tag.span.get_text(strip=True))
    nested_spans = span_tag.find_all('span')

    # 获取评论
    comments = crawler_comment(POI,review_count_page)
    print(address,summary)
    print(comments)