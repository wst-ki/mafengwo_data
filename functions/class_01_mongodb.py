# builder:wstki
# 开发时间16:27,2024/2/3
# name:class_01_mongodb
# encoding: utf-8
""" 该代码主要是将mongodb的一些复杂初始化步骤进行简化
"""

import pymongo

# todo 存在相同user_id的数据不要重复入库，具体实现有待商榷

host = '127.0.0.1'
port = '27017'


# dataset = 'bike_sharing2'


class MongoDB:
    def __init__(self, dataset: str, collection: str):
        self.client = pymongo.MongoClient(host, int(port))

        # 检查数据库是否已存在
        if dataset not in self.client.list_database_names():
            # 如果数据库不存在，则创建它
            self.create_database(dataset)

        # 检查集合是否已存在
        if collection not in self.client[dataset].list_collection_names():
            # 如果集合不存在，则创建它或执行其他初始化任务
            self.create_collection(dataset, collection)

        # 连接到指定的集合
        self.collection = self.client[dataset][collection]

    def create_database(self, dataset: str):
        """
        创建数据库
        :param dataset: 数据库名称
        :return: 在mongodb新建的数据库
        """
        try:
            self.client[dataset].command("create")
            print(f"数据库 '{dataset}' 创建成功。")
        except Exception as e:
            print(f"创建数据库 '{dataset}' 时出错：{e}")

    def create_collection(self, dataset: str, collection: str):
        """
        数据集合
        :param dataset:指定数据库名称
        :param collection: 新建集合名称
        :return: 在mongodb中指定数据库的新集合
        """
        try:
            # 在这里进行其他初始化任务或创建索引（如果需要）
            self.client[dataset].create_collection(collection)
            print(f"集合 '{collection}' 创建成功。")
        except Exception as e:
            print(f"创建集合 '{collection}' 时出错：{e}")

    def insert_one(self, data: dict):
        """
        插入单个字典型数据到数据库中
        :param data: 字典型数据
        :return: 没啥好返回的
        """
        self.collection.insert_one(data)
        print('data has inserted successfully')

    def insert_many(self, data_list: list):
        """
        使用insert_many方法可以插入多个文档（数据字典组成的列表）到指定的集合中。
        如果有重复的 _id，由于 ordered=False，会忽略错误。
        :param data_list: 数据字典组成的列表
        :return:
        """
        try:
            self.collection.insert_many(data_list, ordered=False)
        except pymongo.errors.BulkWriteError:
            pass

    def create_index(self, field: str, unique: bool):
        """
        创建索引
        :param field: 要创建索引的字段
        :param unique: 是否为唯一索引
        """
        self.collection.create_index(field, unique=unique)
        print('index has been created')

    def find(self, condition=None):
        """
        使用find方法可以检索集合中符合条件的文档。
        :param condition:条件
        :return:
        """
        return self.collection.find(condition)

    def find_one(self, condition=None):
        """
        使用find_one方法可以检索集合中符合条件的第一个文档。
        :param condition:条件
        :return:
        """
        return self.collection.find_one(condition)

    def find_big_data(self, condition=None):
        """
        查询大量数据
        :param condition: 查询条件，默认为 None，表示查询所有数据
        :return: 返回查询结果的游标，no_cursor_timeout=True 避免游标超时
        """
        return self.collection.find(condition, no_cursor_timeout=True)

    def find_page(self, condition=None, page_size=10, page_num=0):
        """
        分页查询数据
         :param condition: 查询条件，默认为 None，表示查询所有数据
         :param page_size: 每页数据数量，默认为 10
         :param page_num: 页码，默认为 0
         :return: 返回查询结果的游标
         """
        return self.collection.find(condition).skip((page_num * page_size)).limit(page_size)

    def update_one(self, filter_: dict, update: dict):
        """
        更新单个文档
        :param filter_: 更新条件
        :param update: 更新的数据
        """
        self.collection.update_one(filter_, {'$set': update})
        # print('data has updated successfully')

    def update_many(self, data_list: list):
        """
        批量更新文档
        :param data_list: 包含更新条件和数据的列表，每个元素为 (filter, update)
        """
        update_list = []
        for filter, update in data_list:
            update_list.append(pymongo.UpdateOne(filter, {'$set': update}))
        self.collection.bulk_write(update_list)

    def delete_field_one(self, filter_: dict, update: dict):
        """
        删除单个文档的指定字段
        :param filter_: 删除条件
        :param update: 包含要删除的字段的数据字典
        """
        self.collection.update_one(filter_, {'$unset': update})

    def delete_one(self, filter_):
        """
        删除单个文档
        :param filter_: 删除条件
        """
        self.collection.delete_one(filter_)

    def delete_many(self, filter_):
        """
        批量删除文档
        :param filter_: 删除条件
        """
        self.collection.delete_many(filter_)
