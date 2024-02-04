# builder:wstki
# 开发时间16:27,2024/2/3
# name:class_01_mongodb
# encoding: utf-8
""" 该代码主要是将mongodb的一些复杂初始化步骤进行简化
"""

import pymongo

host = '127.0.0.1'
port = '27017'


# dataset = 'bike_sharing2'


class MongoDB:
    def __init__(self, dataset: str, collection: str):
        self.client = pymongo.MongoClient(host, int(port))
        self.collection = self.client[dataset][collection]

    def insert_one(self, data: dict):
        self.collection.insert_one(data)
        # print('data has inserted successfully')

    def insert_many(self, data_list: list):
        try:
            self.collection.insert_many(data_list, ordered=False)
        except pymongo.errors.BulkWriteError:
            pass

    def create_index(self, field: str, unique: bool):
        self.collection.create_index(field, unique=unique)
        print('index has been created')

    def find(self, condition=None):
        return self.collection.find(condition)

    def find_big_data(self, condition=None):
        return self.collection.find(condition, no_cursor_timeout=True)

    def find_page(self, condition=None, page_size=10, page_num=0):
        return self.collection.find(condition).skip((page_num * page_size)).limit(page_size)

    def update_one(self, filter_: dict, update: dict):
        self.collection.update_one(filter_, {'$set': update})
        # print('data has updated successfully')

    def update_many(self, data_list: list):
        update_list = []
        for filter, update in data_list:
            update_list.append(pymongo.UpdateOne(filter, {'$set': update}))
        self.collection.bulk_write(update_list)

    def delete_field_one(self, filter_: dict, update: dict):
        self.collection.update_one(filter_, {'$unset': update})

    def delete_one(self, filter_):
        self.collection.delete_one(filter_)

    def delete_many(self, filter_):
        self.collection.delete_many(filter_)
