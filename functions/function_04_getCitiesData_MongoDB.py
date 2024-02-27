#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：mafengwo_data 
@File    ：function_04_getCitiesData_MongoDB.py
@IDE     ：PyCharm 
@Author  ：lee_yukhang
@Date    ：2024/2/27 19:56 
'''
import pymongo
from functions.function_06_getHTML import html_crawler
from bs4 import BeautifulSoup

'''
本函数是function04_getCitiesData的数据库版，所有的城市ID、网址及其POI数量将会保存到数据库中
'''


def getCitiesData_DB(mongo_instance):
    '''
    传入一个数据库实例（告诉它你要传的数据库叫什么名字，存在哪一个数据集合）
    :param mongo_instance: 数据库实例
    :return: 没啥好返回的
    '''
    # 检查集合是否已存在数据
    if mongo_instance.collection.count_documents({}) > 0:
        print("城市数据已存在，无需再次提取。")
        return
    else:
        print("正在提取城市数据...")
        url = 'https://www.mafengwo.cn/mdd/'
        html_content = html_crawler(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        # 找到包含城市信息的<div>标签
        hot_list_div = soup.find('div', class_='hot-list clearfix')
        # 找到<div>下的所有<dd>标签
        dd_tags = hot_list_div.select('dd')
        # 提取城市信息
        # 提取城市信息并输出为字典列表
        cities_list = []

        for dd_tag in dd_tags:
            # 找到<dd>标签中的所有城市链接
            city_links = dd_tag.find_all('a', target='_blank')

            for link in city_links:
                city_name = link.get_text(strip=True)
                city_link = link['href']
                city_id = city_link.rsplit('/', 1)[-1].rsplit('.', 1)[0]

                # 打印城市信息
                print(f"提取城市：{city_name}，链接：{city_link}，ID：{city_id}")

                # 构建字典并加入列表
                city_dict = {'city': city_name,
                             'link': city_link,
                             'poi_count': 0,
                             'id': city_id}

                # 获取城市的POI数量
                try:
                    city_id_str = str(city_id).split('.')[0]
                    # 构建函数，输入城市名，查找这个城市的景点数量
                    url = f'https://www.mafengwo.cn/jd/{city_id_str}/gonglve.html'

                    # 检查 'poi_count' 对应的值是否为 0
                    if city_dict['poi_count'] == 0:
                        html_content = html_crawler(url)
                        soup = BeautifulSoup(html_content, 'html.parser')
                        # 找到包含页数和条目数的<span>元素
                        count_span = soup.find('span', class_='count')
                        # 找到嵌套的所有<span>元素
                        nested_spans = count_span.find_all('span')
                        # 提取总条目数，位于第二个嵌套的<span>元素，即POI数量
                        item_count = int(nested_spans[1].get_text(strip=True))
                        # 更新字典的 'poi_count' 键对应的值
                        city_dict['poi_count'] = item_count
                        # 向数据库中插入该城市的数据
                        mongo_instance.insert_one(city_dict)
                        print(f"{city_name} 的景点数获取完毕。")
                    elif city_dict['poi_count'] == -1:
                        print(f"{city_name} 的景点数获取失败，将该城市的景点数设为 -1")
                    else:
                        print(f"{city_name} 的景点数已存在，无需再次获取。")
                except Exception as e:
                    print(f"An error occurred for city_id {city_name}: {str(e)}, 将该城市的景点数设为 -1")
                    city_dict['poi_count'] = -1
                    # 向数据库中插入该城市的数据
                    mongo_instance.insert_one(city_dict)

        print("城市数据提取完成。")
