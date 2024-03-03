# builder:wstki
# 开发时间10:04,2024/2/5
# name:funciton_08_getPOIcomment
# 获取一个城市中所有景点的评论
from functions.function_05_getPOIID import _get_route
import pandas as pd
import os
from functions.function_06_getHTML import html_crawler
from bs4 import BeautifulSoup
from functions.function_07_getComment import crawler_comment

# todo 后面要改成从数据库获取数据 先将评论返回到csv中,注意现在这个函数已经能够返回POI的地址了，需要进行地理编码
# todo 对于cityID_list需要添加一个判定，如果其中的某个POIid对应的评论数量为-1或者POI的id为none就跳过这个POI
def get_mdd_POIcomment(cityID_list,csv_path):
    """
    获取一个城市中所有景点的评论
    :param cityID_list: 从数据库中获取一列数据，是城市的对应id
    :param csv_path: csv的路径，后面要更改为数据库路径
    :return: 内循环都会返回对应城市中一个景点的评论，外循环是城市
    """
    if not os.path.exists(csv_path):
        for cityID in cityID_list:
            _get_route(cityID)
            results, df = _get_route(cityID)
            print(df)
            df.to_csv(f'../cache/{cityID}.csv', index=False)
    else:
        print(f'{csv_path} 文件已存在')
        pass
    df = pd.read_csv(csv_path)
    link_col = df['link']
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
        span_tag = soup.find('span', class_='count')

        # 提取评价数量

        # 评论的页数
        review_count_page = int(span_tag.span.get_text(strip=True))
        nested_spans = span_tag.find_all('span')

        # 获取评论
        comments = crawler_comment(POI, review_count_page)
        comment_df = pd.DataFrame(comments)
        comment_df.to_csv(os.path.join('..','cache',f'{POI}.csv'), index=False)
        print(f'{POI}.csv 已保存')
        """
        {
        POIname
        summery
        city_id
        city_name
        POI_id
        POI_link
        POI_address
        address对应的经纬度
        POI_comment_count
        commentPage    
        comment_df:user_name,comment,data_comment_id,star_number,user_id
        }
        """