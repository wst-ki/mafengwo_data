# builder:wstki
# 开发时间9:12,2024/2/3
# name:test_header_POIjson
# 使用小程序获取一个POI的json数据
import requests
import json
import certifi



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Cookie':'PHPSESSID=indi8nh4949f28fqiek7gobon7;mfw_uuid=65bda19f-36e9-e3b5-3e9a-0b7baadd9920;mfw_uid=47825567;'
}
base_url = 'http://wxapp.mafengwo.cn/ma_support/matrix/travel/construction/?jsondata={"filter":{"id":3474},"filter_style":"poi"}'
base_url2 = 'https://wxapp.mafengwo.cn/ma_support/matrix/poi/basic/3519'
# 发送请求
response = requests.get(base_url, headers=headers, verify=certifi.where())

# 检查请求是否成功
if response.status_code == 200:
    print(response.text)
    print(11)


else:
    print(response.status_code)
