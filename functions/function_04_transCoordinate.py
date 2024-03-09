# builder:wstki
# 开发时间10:11,2024/2/2
# name:function_04_transCoordinate
# 测试百度地图和腾讯地图的地理编码，其得到的坐标是GCJ02的，要转换为WGS84
import requests
import re
import math
import time
from urllib.parse import quote
from fake_useragent import UserAgent
import json
class From_gcj02_to_wgs84:
    """
    地理编码后需要坐标转换,腾讯地图的地理编码，其得到的坐标是GCJ02的，要转换为WGS84
    """
    def __init__(self):
        self.PI = 3.14159265358979324
        self.aa = 6378245.0
        self.ee = 0.00669342162296594323

    def transform_lat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.PI) + 20.0 * math.sin(2.0 * lng * self.PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.PI) + 40.0 * math.sin(lat / 3.0 * self.PI)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.PI) + 320 * math.sin(lat * self.PI / 30.0)) * 2.0 / 3.0
        return ret

    def transform_lng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.PI) + 20.0 * math.sin(2.0 * lng * self.PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.PI) + 40.0 * math.sin(lng / 3.0 * self.PI)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.PI) + 300.0 * math.sin(lng / 30.0 * self.PI)) * 2.0 / 3.0
        return ret

    def out_of_china(self, lng, lat):
        # 判断是否在中国范围外
        return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

    def gcj02_to_wgs84(self, lng, lat):
        # 判断是否为国外坐标
        if self.out_of_china(lng, lat):
            return [lng, lat]
        else:
            dlat = self.transform_lat(lng - 105.0, lat - 35.0)
            dlng = self.transform_lng(lng - 105.0, lat - 35.0)
            radlat = lat / 180.0 * self.PI
            magic = math.sin(radlat)
            magic = 1 - self.ee * magic * magic
            sqrtmagic = math.sqrt(magic)
            dlat = (dlat * 180.0) / ((self.aa * (1 - self.ee)) / (magic * sqrtmagic) * self.PI)
            dlng = (dlng * 180.0) / (self.aa / sqrtmagic * math.cos(radlat) * self.PI)
            mglat = lat + dlat
            mglng = lng + dlng
            return [lng * 2 - mglng, lat * 2 - mglat]



class From_bd09_to_wgs84:
    def __init__(self):
        self.PI = 3.14159265358979324
        self.aa = 6378245.0
        self.ee = 0.00669342162296594323

    def transform_lat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.PI) + 20.0 * math.sin(2.0 * lng * self.PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.PI) + 40.0 * math.sin(lat / 3.0 * self.PI)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.PI) + 320 * math.sin(lat * self.PI / 30.0)) * 2.0 / 3.0
        return ret

    def transform_lng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.PI) + 20.0 * math.sin(2.0 * lng * self.PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.PI) + 40.0 * math.sin(lng / 3.0 * self.PI)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.PI) + 300.0 * math.sin(lng / 30.0 * self.PI)) * 2.0 / 3.0
        return ret

    def out_of_china(self, lng, lat):
        # 判断是否在中国范围外
        return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

    def gcj02_to_bd09(self,lng,lat):
        z = math.sqrt(lng*lng+lat*lat)+0.00002 * math.sin(lat * self.PI)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * self.PI)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return [bd_lng, bd_lat]

    def bd09_to_gcj02(self,bd_lon, bd_lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)
        百度——>谷歌、高德
        :param bd_lat:百度坐标纬度
        :param bd_lon:百度坐标经度
        :return:转换后的坐标列表形式
        """
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.PI)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.PI)
        gg_lng = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return [gg_lng, gg_lat]

    def gcj02_to_wgs84(self, lng, lat):
        # 判断是否为国外坐标
        if self.out_of_china(lng, lat):
            return [lng, lat]
        else:
            dlat = self.transform_lat(lng - 105.0, lat - 35.0)
            dlng = self.transform_lng(lng - 105.0, lat - 35.0)
            radlat = lat / 180.0 * self.PI
            magic = math.sin(radlat)
            magic = 1 - self.ee * magic * magic
            sqrtmagic = math.sqrt(magic)
            dlat = (dlat * 180.0) / ((self.aa * (1 - self.ee)) / (magic * sqrtmagic) * self.PI)
            dlng = (dlng * 180.0) / (self.aa / sqrtmagic * math.cos(radlat) * self.PI)
            mglat = lat + dlat
            mglng = lng + dlng
            return [lng * 2 - mglng, lat * 2 - mglat]

    def bd09_to_wgs84(self,lng, lat):
        point = self.bd09_to_gcj02(lng, lat)
        wgs84point = self.gcj02_to_wgs84(point[0], point[1])
        return [wgs84point[0], wgs84point[1]]



# 使用腾讯地图进行地理编码查询
def tx_geoCoordinate(addr):
    with open(r'..\keys\tx_key.txt','r',encoding='utf-8') as file:
        key = file.read()
    #查询addr的经纬度
    template = f'https://apis.map.qq.com/jsapi?qt=geoc&addr={addr}&key={key}=jsonp&pf=jsapi&ref=jsapi&cb=qq.maps._svcb2.geocoder0'
    url = template.format(addr=addr)
    resp = requests.get(url)
    lon = float(re.findall('pointx":"(.*?)",', resp.text)[0])
    lat = float(re.findall('pointy":"(.*?)",', resp.text)[0])
    return lon,lat


# 备用，用百度地图获取地理编码
def bd_geoCoordinate(addr):
    with open(r'..\keys\bd_key.txt','r',encoding='utf-8') as file:
        key = file.read()
    ua = UserAgent()

    ua_get = ua.random

    header_get = {
        'User-Agent': ua_get,
        'Connection': "close"
    }
    # 百度提供的接口
    url = 'http://api.map.baidu.com/geocoding/v3/?address='
    # 数据
    output = 'json'
    # KEY要去百度地图开发者平台申请
    ak = key
    # 通过百度创建应用得到ak，记得写为浏览器端，然后写*
    addr = quote(str(addr))
    uri = url + addr + '&output=' + output + "&ak=" + ak
    try:
        req = requests.get(uri, headers=header_get).text
        #         print( req)

        # res = req.read().decode()
        time.sleep(0.1)
        # print(res)
        temp = json.loads(req)
        if temp['status'] == 0:
            # 精度
            lat = temp['result']['location']['lat']
            # 纬度
            lng = temp['result']['location']['lng']

            #  百度地图解析结果精度判断以字段comprehension的值为依据
            acc = temp['result']['comprehension']
            use = temp['result']['level']
        else:
            lat = 0
            lng = 0
            acc = "无"
            use = '无'
        # return lat, lng,acc
        return lng, lat, acc, use

    except Exception as e:
        print(e)
        #         print(data['地址1'].iloc[i])
        time.sleep(3)
        bd_geoCoordinate(addr)