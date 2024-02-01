# builder:wstki
# 开发时间15:24,2024/2/1
# name:test_encoding_string
import re
import requests
import json
import time
import hashlib
print("test")
# 通用 Headers
HEADERS = headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36'
}



REQ = requests.session()
REQ.headers=HEADERS
URL_ROUTE = 'http://www.mafengwo.cn/ajax/router.php'


def _stringify(data):
    """
    将 dict 的每一项都变成字符串
    """
    data = sorted(data.items(), key=lambda d: d[0])
    new_dict = {}
    for item in data:
        if type(item[1]) == dict:
            # 如果是字典类型，就递归处理
            new_dict[item[0]] = json.dumps(
                _stringify(item[1]), separators=(',', ':'))
        else:
            if type(item[1]) == list:
                # 如果是列表类型，就把每一项都变成字符串
                new_list = []
                for i in item[1]:
                    new_list.append(_stringify(i))
                new_dict[item[0]] = new_list
            else:
                if item[1] is None:
                    new_dict[item[0]] = ''
                else:
                    new_dict[item[0]] = str(item[1])
    return new_dict

def _get_md5_encrypted_string():

    # 以北京景点为例，首先获取加密 js 文件的地址
    url = 'http://www.mafengwo.cn/jd/10065/gonglve.html'
    r = REQ.get(url)

    if r.status_code == 403:
        exit('访问被拒绝，请检查是否为IP地址被禁')
    param = re.findall(
        r'src="https://js.mafengwo.net/js/hotel/sign/index.js(.*?)"', r.text)
    param = param[0]
    # 拼接 index.js 的文件地址
    url_indexjs = 'https://js.mafengwo.net/js/hotel/sign/index.js' + param
    # 获取 index.js
    r = REQ.get(url_indexjs)
    if r.status_code == 403:
        exit('访问被拒绝')
    response_text = r.text
    # 查找加密字符串
    result = re.findall(r'var __Ox2133f=\[(.*?)\];', response_text)[0]
    byteslike_encrypted_string = result.split(',')[46].replace('"', '')
    # 解码
    strTobytes = []
    for item in byteslike_encrypted_string.split('\\x'):
        if item != '':
            num = int(item, 16)
            strTobytes.append(num)
    # 转换字节为字符串
    encrypted_string = bytes(strTobytes).decode('utf8')
    encrypted_string = encrypted_string
    return encrypted_string

encrypted_string = _get_md5_encrypted_string()

def _md5(data):
    '''
    获取请求参数中的加密参数，_ts 和 _sn
    '''
    _ts = int(round(time.time() * 1000))
    data['_ts'] = _ts
    # 数据对象排序并字符串化
    orderd_data = _stringify(data)
    # md5 加密
    m = hashlib.md5()
    m.update((json.dumps(orderd_data, separators=(',', ':')) +
              encrypted_string).encode('utf8'))
    _sn = m.hexdigest()
    # _sn 是加密后字符串的一部分
    orderd_data['_sn'] = _sn[2:12]
    return orderd_data

post_data = _md5({
        'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
        'iMddid': 10065,
        'iTagId': 0,
        'iPage': 5
    })
url = URL_ROUTE + '?' + '&'.join([f'{key}={value}' for key, value in post_data.items()])
r = REQ.post(url)
if r.status_code == 403:
    exit('访问被拒绝')
response = r.json()
list_data = response['data']['list']
page_data = response['data']['page']
print(list_data)
print()