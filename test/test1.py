# builder:wstki
# 开发时间12:39,2024/2/1
# name:test1
import requests
import time
import json
import hashlib



encrypted_string = ''
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

if __name__ == "__main__":
    # 查询景点的网址
    # 包含景点详情的链接、景点图片和景点名称
    URL_ROUTE = 'http://www.mafengwo.cn/ajax/router.php'

    # 通用 Headers
    HEADERS = {
        'Referer': 'http://www.mafengwo.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

    # 拿广州为例
    post_data = _md5({
        'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
        'iMddid': 10065,
        'iTagId': 0,
        'iPage': 1
    })
    print(post_data)
    url = URL_ROUTE + '?' + '&'.join([f'{key}={value}' for key, value in post_data.items()])
    print(url)
    REQ = requests.session()
    REQ.headers.update(HEADERS)

    r = REQ.post(url, data=post_data)
    print(r.json)
    print(78)
    print("r.content",r.content)
    if r.status_code == 403:
        exit('访问被拒绝')
    try:
        response = r.json()
        print(response)
        list_data = response['data']['list']
        page_data = response['data']['page']
    except requests.exceptions.JSONDecodeError:
        print('JSON解码错误或响应为空')