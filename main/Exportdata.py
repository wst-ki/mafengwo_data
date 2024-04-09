import pymongo
import json
import os

# MongoDB连接信息
host = '127.0.0.1'
port = '27017'
database_name = '地途'  # 修改为你的数据库名称

# 连接到 MongoDB
client = pymongo.MongoClient(host, int(port))
db = client[database_name]

# 获取数据库中的所有集合
collections = db.list_collection_names()

# 指定保存位置
output_dir = 'E:/地途/批量导出json'  # 修改为你希望保存的文件夹路径

# 检查路径是否存在，如果不存在则创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
count = 0
# 导出每个集合中的文档为 JSON 文件
for collection_name in collections:
    collection = db[collection_name]
    documents = collection.find()

    # 创建一个列表，用于存储集合中的所有文档
    all_documents = []

    # 将集合中的所有文档添加到列表中
    for document in documents:
        # 将 ObjectId 对象转换为字符串
        document = {key: str(value) if key == '_id' else value for key, value in document.items()}
        all_documents.append(document)

    # 打开文件并写入所有文档
    with open(os.path.join(output_dir, f'{collection_name}.json'), 'w', encoding='utf-8') as outfile:
        json.dump(all_documents, outfile, ensure_ascii=False, indent=4)
        print(f'{collection_name}.json已导出')
        count += 1
print(f'本次导出{count}个文件')