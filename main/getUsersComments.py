#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：mafengwo_data 
@File    ：getUsersComments.py
@IDE     ：PyCharm 
@Author  ：lee_yukhang
@Date    ：2024/3/3 10:44 
'''

#todo 基于test16的基础，从数据库中读取一个城市对应的所有POI数据，每一条POI数据读出每一条评论的用户id，爬取对应用户主页的游记
import pymongo
from functions.class_01_mongodb import MongoDB
from functions.function_09_getUserComment import getUserComment
# 新建一个用户id集合
userid_list = []
comments_mongo = MongoDB(dataset='地途', collection='user_comments')  # 新建或连接一个数据库实例
# 从数据库调取用户id
# TODO 报错啦
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["地途"]
mycol = mydb["10088_POIs"]
query_id = {}
projection_id = {"comments": 1}
result_id = mycol.find({},projection_id)
for x in result_id:
    for y in x['comments']:
        userid_list.append(y['user_id'])
print(userid_list)
for userid in userid_list:
    user_info = getUserComment(userid)  # 读取每一个用户id，爬取对应游记
    comments_mongo.insert_one(user_info)
