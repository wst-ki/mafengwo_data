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

def get_POIcomment_DB(cityID, mongo_instance):
    """
    获取一个城市中所有景点POI及其评论
    :param cityID: 从数据库中获取单个数据，是城市的对应id
    :param mongo_instance: 数据库实例
    :return: 内循环都会返回对应城市中一个景点的评论，外循环是城市
    """
    print(f"正在提取{cityID}的城市数据")

    # 根据城市的ID，获取所有POI的路线信息
    _get_route(cityID)
    results, df = _get_route(cityID)
    print(df)

    # 将每个路线信息及其评论保存到MongoDB中
    for _, route_data in df.iterrows():
        # 获取评论的现有代码
        link = route_data['link']
        POI = route_data['poi_id']
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

        # 构建文档，将评论数据添加到route_data中
        document = {
            'cityID': cityID,
            'route_data': route_data.to_dict(),  # df转为字典
            'comments': crawler_comment(POI, review_count_page),
            'text_content': text_content,
            'address': address
        }

        # 将文档保存到MongoDB中
        mongo_instance.insert_one(document)
        print(f'编号为{POI}的城市保存成功')
    print("数据保存成功！")
