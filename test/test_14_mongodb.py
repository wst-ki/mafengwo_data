# builder:wstki
# 开发时间16:21,2024/2/3
# name:test_14_mongodb
import pymongo
# 连接到 MongoDB 服务器
client = pymongo.MongoClient("mongodb://localhost:27017")
# 创建一个数据库（如果不存在则自动创建）
my_database = client["Mafengwo"]
# 创建一个集合（如果不存在则自动创建）
my_collection = my_database["test"]
# 输出已创建的数据库和集合
print(f"Database: {my_database.name}")
print(f"Collection: {my_collection.name}")