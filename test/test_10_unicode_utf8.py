# builder:wstki
# 开发时间20:48,2024/2/2
# name:test_10_unicode_utf8
import json
unicode = '{"errno":0,"error":null,"data":{"@type":"landscape","uniq_id":"poi_3474","title":"\u6545\u5bab","thumbs":["https:\/\/p1-q.mafengwo.net\/s19\/M00\/2D\/FE\/CoNFJmJXiTI2MiNEAAkbC7NyIs4.jpeg"],"cover":"https:\/\/p1-q.mafengwo.net\/s19\/M00\/2D\/FE\/CoNFJmJXiTI2MiNEAAkbC7NyIs4.jpeg","desc":"\u00b7\u53c8\u540d\u7d2b\u7981\u57ce\uff0c\u662f\u4e2d\u56fd\u4e43\u81f3\u4e16\u754c\u4e0a\u4fdd\u5b58\u6700\u5b8c\u6574\uff0c\u89c4\u6a21\u6700\u5927\u7684\u6728\u8d28\u7ed3\u6784\u53e4\u5efa\u7b51\u7fa4\uff0c\u88ab\u8a89\u4e3a\u201c\u4e16\u754c\u4e94\u5927\u5bab\u4e4b\u9996\u201d\u3002\n\u00b7\u5185\u5ef7\u4ee5\u4e7e\u6e05\u5bab\u3001\u4ea4\u6cf0\u6bbf\u3001\u5764\u5b81\u5bab\u540e\u4e09\u5bab\u4e3a","address":"\u5317\u4eac\u5e02\u4e1c\u57ce\u533a\u666f\u5c71\u524d\u88574\u53f7","time":"","longitude":39.917839,"latitude":116.397029,"tags":["\u6545\u5bab","\u6545\u5bab\u535a\u7269\u9662|\u5317\u4eac\u6545\u5bab|\u7d2b\u7981\u57ce|\u5317\u4eac\u6545\u5bab\u535a\u7269\u9662","The Palace Museum"],"digest":""}}'
place_json = unicode
file_path = "./test.json"
# 打开文件并写入文本内容
with open(file_path, "w", encoding="utf-8") as file:
    file.write(place_json)
# 打开 JSON 文件并加载数据
with open(file_path, "r", encoding="utf-8【") as json_file:
    json_data = json.load(json_file)

# 现在，json_data 变量包含了 JSON 文件中的数据，你可以对其进行处理
print(json_data)