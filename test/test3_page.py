# builder:wstki
# 开发时间17:16,2024/2/1
# name:test3_page
import re
from bs4 import BeautifulSoup
import requests
from functions.function_02_md5_getCityPOIList import _md5
REQ = requests.session()
from functions.function_01_get_encrypted_string import _get_md5_encrypted_string
import time
import hashlib
import json
import requests
import pandas as pd

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

def _get_route( mdd_id):
    '''
    获取景点信息
    '''


    results = []
    # 获取景点有多少页，防止少于20页
    post_data = _md5({
        'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
        'iMddid': mdd_id,
        'iTagId': 0,
        'iPage': 1
    })
    url = 'http://www.mafengwo.cn/ajax/router.php' + '?' + '&'.join(
        [f'{key}={value}' for key, value in post_data.items()])
    r = REQ.post(url, data=post_data)
    if r.status_code == 403:
        exit('访问被拒绝')
    response = r.json()
    list_data = response['data']['list']
    page_data = response['data']['page']
    soup_page = BeautifulSoup(page_data, "html.parser")
    page = int(soup_page.find('span', class_='count').find('span').text)
    # 没法突破20页的限制，每个城市最多只能获取300个POI
    for page in range(1,page+1):
        post_data = _md5({
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            'iMddid': mdd_id,
            'iTagId': 0,
            'iPage': page
        })
        url = 'http://www.mafengwo.cn/ajax/router.php' + '?' + '&'.join([f'{key}={value}' for key, value in post_data.items()])
        r = REQ.post(url, data=post_data)
        if r.status_code == 403:
            exit('访问被拒绝')
        response = r.json()
        list_data = response['data']['list']
        print(list_data)
        page_data = response['data']['page']
        # 解析景点列表数据
        soup = BeautifulSoup(list_data, "html.parser")
        route_list = soup.find_all('a')

        for route in route_list:
            link = route['href']
            route_id = re.findall(r'/poi/(.*?).html', link)
            name = route['title']
            image = route.find('img')['src'].split('?')[0]
            results.append({
                'poi_id': int(route_id[0]),
                'name': name,
                'image': image,
                'link': 'http://www.mafengwo.cn' + link,
            })

        df = pd.DataFrame(results)

        # 返回当前页列表数据和总页数
    return results,df
results,df = _get_route( mdd_id=10065)
df.to_csv("test.csv")
print(results)
print(df)
print(len(results))
