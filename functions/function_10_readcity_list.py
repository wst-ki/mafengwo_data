#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：mafengwo_data 
@File    ：function_10_readcity_list.py
@IDE     ：PyCharm 
@Author  ：lee_yukhang
@Date    ：2024/4/5 10:25 
"""
from functions.class_01_mongodb import MongoDB


def readcity_list(mongo_instance):
    '''
    本函数是读取cities_list文档（城市列表数据）中每一个城市的对应id，传入一个数据库实例，返回一个城市id列表
    :param mongo_instance: 存有城市poi数据的数据库实例
    :return: 城市id列表
    '''
    # city_mongo = MongoDB(dataset='地途', collection='cities_data')  # 连接城市数据库实例
    city_list = []
    # 查询所有文档，并且仅返回 "id" 字段
    result = mongo_instance.find({}, {"id": 1, "_id": 0})
    # 遍历查询结果，并将 id 添加到列表中
    for document in result:
        city_list.append(document["id"])
        # 返回包含所有 id 的列表
    # print(city_list) # 打印出来
    return city_list
