#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：mafengwo_data 
@File    ：getUsersComments.py
@IDE     ：PyCharm 
@Author  ：lee_yukhang
@Date    ：2024/3/3 10:44 
'''

# todo 基于test16的基础，从数据库中读取一个城市对应的所有POI数据，每一条POI数据读出每一条评论的用户id，爬取对应用户主页的游记

from functions.class_01_mongodb import MongoDB
from functions.function_09_getUserComment import getUserComment

# 新建一个用户id集合
userid_list = []
comments_mongo = MongoDB(dataset='地途', collection='user_comments')
cities_mongo = MongoDB(dataset='地途', collection='cities_data')

# TODO 从数据库调取城市id(暂时只用广州的10088,后面再调用)
city_id_list = [10088]
# city_id_list = []
# cursor = cities_mongo.find({}, {"_id": 0, "id": 1})  # 查询所有文档，仅返回"id"字段，不包括"_id"字段
# for document in cursor:
#     city_id_list.append(document["id"])

# 创建空列表user_id_list，用于存放所有用户的id
user_id_list = []

# 遍历 城市id列表
for city_id in city_id_list:
    # 构造数据集名称，形如"10088_POIs"
    dataset_name = f"{city_id}_POIs"
    data = MongoDB(dataset='地途', collection=dataset_name)
    # 查询并遍历集合中的每个文档
    cursor = data.find({}, {"comments.user_id": 1})

    # 遍历游标以获取实际数据
    for document in cursor:
        # 检查文档是否包含comments字段
        if "comments" in document:
            # 遍历每个评论
            for comment in document["comments"]:
                # 提取用户ID并添加到列表中
                user_id_list.append(comment["user_id"])

# # 打印所有提取到的user_id
# print(user_id_list)


for userid in user_id_list:
    if comments_mongo.find_one({"user_id": userid}, ) is not None:
        print("该用户已存储到数据库中")
        continue
    user_info = getUserComment(userid)  # 读取每一个用户id，爬取对应游记
    if user_info == None:
        continue
    else:
        comments_mongo.insert_one(user_info)
