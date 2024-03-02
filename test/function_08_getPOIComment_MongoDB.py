#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：mafengwo_data 
@File    ：function_08_getPOIComment_MongoDB.py
@IDE     ：PyCharm 
@Author  ：lee_yukhang
@Date    ：2024/3/1 20:06 
"""
import os

import pandas as pd
import pymongo
from bs4 import BeautifulSoup

from functions.function_05_getPOIID import _get_route
from functions.function_06_getHTML import html_crawler
from functions.function_07_getComment import crawler_comment


def get_POIcomment_DB(cityID_list, mongo_instance):
    """
    获取一个城市中所有景点的评论
    :param cityID_list: 从数据库中获取一列数据，是城市的对应id
    :param mongo_instance: 数据库实例
    :return: 内循环都会返回对应城市中一个景点的评论，外循环是城市
    """
    # 检查集合是否已存在数据
    print(f"正在提取{cityID_list}城市数据...")
    for cityID in cityID_list:
        # 使用 count_documents 检查数据库中是否存在指定的城市ID
        count = mongo_instance.collection.count_documents({'id': cityID})
        if count > 0:
            print(f"已经提取id为{cityID}城市数据...")
            continue
        print(f"正在提取{cityID}的城市数据")

        # 获取路线信息的现有代码
        _get_route(cityID)
        results, df = _get_route(cityID)
        print(df)

        # 将路线信息保存到MongoDB
        mongo_instance.insert_one({'id': cityID, 'route_data': df.to_dict(orient='records')})

        # 获取评论的现有代码
        link_col = df['link'].dropna()
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

            # 将评论保存到MongoDB
            comments = crawler_comment(POI, review_count_page)
            mongo_instance.update_one(
                {'id': int(cityID), 'route_data.$.poi_id': int(POI)},
                {
                    '$set': {
                        'route_data.$.comments': comments
                    }
                }
            )
            print(f'{POI}保存成功')
            # todo 不知道为什么不能保存数据
