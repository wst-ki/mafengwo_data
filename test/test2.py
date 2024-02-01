# builder:wstki
# 开发时间14:31,2024/2/1
# name:test2
import requests
import hashlib

import time
import json
encrypted_string=""
data  = {
        'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
        'iMddid': 10065,
        'iTagId': 0,
        'iPage': 1
    }
# 通用 Headers
HEADERS = headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36'
}


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
post_data = orderd_data

REQ = requests.session()
REQ.headers.update(HEADERS)
# 查询景点的网址
# 包含景点详情的链接、景点图片和景点名称
URL_ROUTE = 'http://www.mafengwo.cn/ajax/router.php'
r = REQ.post(URL_ROUTE, data=post_data)
response = r.json()
print(response)