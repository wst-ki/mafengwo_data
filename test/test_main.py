# builder:wstki
# 开发时间17:36,2024/2/1
# name:test_main
# 进行function的功能测试
import requests
from functions.function_01_get_encrypted_string import _get_md5_encrypted_string
from functions.function_02_md5_getCityPOIList import _md5


HEADERS = headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36'
}
REQ = requests.session()
REQ.headers=HEADERS


post_data = _md5({
        'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
        'iMddid': 10065,
        'iTagId': 0,
        'iPage': 2
    })
url = 'http://www.mafengwo.cn/ajax/router.php' + '?' + '&'.join([f'{key}={value}' for key, value in post_data.items()])


# 测试前两个函数

r = REQ.post(url)
if r.status_code == 403:
    exit('访问被拒绝')
response = r.json()
list_data = response['data']['list']
page_data = response['data']['page']
print(list_data)
