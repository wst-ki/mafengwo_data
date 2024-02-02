#coding:utf-8
import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import random
import re
import pandas as pd
# 导入写入的广州二手房数据
df = pd.read_excel(r'output/output2.xls')
df['latitude'] = None
df['longitude'] = None
print(df)

def query(z,addr):
    #查询addr的经纬度
    template = 'https://apis.map.qq.com/jsapi?qt=geoc&addr={addr}&key=UGMBZ-CINWR-DDRW5-W52AK-D3ENK-ZEBRC&output=jsonp&pf=jsapi&ref=jsapi&cb=qq.maps._svcb2.geocoder0'
    url = template.format(addr=addr)
    resp = requests.get(url)
    x = float(re.findall('pointx":"(.*?)",',resp.text)[0])
    y = float(re.findall('pointy":"(.*?)",',resp.text)[0])
    if x != None and y !=None:
        if x < 114 and y < 24:
            df.loc[z, 'latitude'] = x
            print(x)
            df.loc[z, 'longitude'] = y
            print(y)
        else:
            df.loc[z, 'latitude'] = None
            df.loc[z, 'longitude'] = None
    else:
        df.loc[z, 'latitude'] = None
        df.loc[z, 'longitude'] = None

for z in range(0,len(df)):
    gz="广州市"
    #search_string = gz+df['region'][x]+df['Address'][x]#+df['HouseName'][x]
    search_string = gz+df['address'][z]
    print(search_string)
    query(z,search_string)
    sleep(random.uniform(1, 2))
#将处理后的信息保存到csv
df.to_csv('包含经纬度的广州二手房数据清洗结果.csv')