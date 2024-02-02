# builder:wstki
# 开发时间17:26,2024/2/1
# name:function_03_getPOI
# 将02中的返回值输入到这里来，就能得到每个POI的各类数据

"""
已经弃用，url无法访问，改用地理编码获取地址坐标
"""


import requests
from functions.function_02_md5_getCityPOIList import _md5


def _get_poi(REQ,poi_id):
    URL_POI = 'http://pagelet.mafengwo.cn/poi/pagelet/poiLocationApi'
    '''
    获取景点经纬度信息
    '''
    payload = _md5({
        'params': {
            'poi_id': poi_id
        }
    })
    # 获取数据
    r = REQ.get(URL_POI, params=payload)
    if r.status_code == 403:
        exit('访问被拒绝')
    try:
        controller_data = r.json()['data']['controller_data']
        poi = controller_data['poi']
        return poi
    except Exception:
        return {}
