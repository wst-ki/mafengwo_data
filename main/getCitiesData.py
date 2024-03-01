#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：mafengwo_data
@File    ：getCitiesData.py
@IDE     ：PyCharm 
@Author  ：lee_yukhang
@Date    ：2024/2/27 12:52 
'''

'''
将所有的城市ID、网址及其POI数量将会保存到数据库中
保存的数据库名称为：地途
保存的数据集名称为：cities_data
'''
from functions.class_01_mongodb import MongoDB
from functions.function_04_getCitiesData_MongoDB import getCitiesData_DB
# 爬取城市信息：使用func04-数据库版
my_mongo = MongoDB(dataset='地途', collection='cities_data')  # 新建或连接一个数据库实例
getCitiesData_DB(my_mongo) # 若集合里面有数据，就会不爬了，重复爬取请删除数据

# 爬取目的地信息(城市的POI信息)： 使用func05-getPOIID

# todo 将上述爬取的对应城市信息用于爬取其前300个POI
# 我测