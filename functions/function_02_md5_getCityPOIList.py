# builder:wstki
# 开发时间17:09,2024/2/1
# name:function_02_md5_getCityPOIList
# 第二步是根据function_01获取到的唯一值来构建查询，获取城市的所有POI数据
# 第二步的返回是一个html，我们需要其中的一个list
from functions.function_01_get_encrypted_string import _get_md5_encrypted_string
import time
import hashlib
import json
import requests
HEADERS = headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36'
}
REQ = requests.session()
REQ.headers=HEADERS
encrypted_string = _get_md5_encrypted_string(REQ)
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

# _md5的前置函数
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