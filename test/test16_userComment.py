# builder:wstki
# 开发时间19:14,2024/2/5
# name:test16_userComment
# 测试function09
from functions.class_01_mongodb import MongoDB
from functions.function_09_getUserComment import  getUserComment
my_mongo = MongoDB(dataset='地途', collection='user_comments')  # 新建或连接一个数据库实例
user_info = getUserComment(76742257)
my_mongo.insert_one(user_info)