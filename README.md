# 编写人：wstki
1. 对于每个函数的构建过程进行解释
2. 数据获取过程中有什么值得记录的地方
3. 有什么经验教训

# 每个函数的构建过程进行总结
参考网站：
1.  [所有函数的原始参考，但是代码年久失修，需要大幅更改](https://blog.csdn.net/yuchunyu97/article/details/89504740)
2. [部分参考了这些这个，但是也是由于端口年久失修，需要更改](https://blog.csdn.net/u011291072/article/details/81266372)
3. [爬虫机制的绕过办法，十分好用，建议收藏](https://github.com/xiantang/Spider)

技术路线：
1. ruquest+beautifulsoup（下面称为bs）**基础的爬虫，但是无法绕过服务器**
2. selenium+bs **模拟真人进行浏览器操作，进行无头骑士的数据获取（大雾）

技巧
1. headers的设置
## function01 get encrypted_string
### 基础知识 1 md5 是什么
[关于md5和sha256的介绍](https://zhuanlan.zhihu.com/p/510264441)

简单来说，每次登陆到马蜂窝，用户都会将自己的账户信息以md5的加密形式上传到服务器端，服务器会对比自身数据库中对应用户的消息和上传的消息是否一致，这也正是为什么我们需要构建函数1 以通过服务器的检验

### 代码解释

~~~ python
import re  
import certifi  
  
# 尝试版本管理  
def _get_md5_encrypted_string(REQ):  
    """  
    获取加密字符串  
    :param REQ:    使用request的secession
    :return: 加密字符串  
    """    # 以北京景点为例，首先获取加密 js 文件的地址  
    url = 'https://www.mafengwo.cn/jd/10065/gonglve.html'  
    r = REQ.get(url,verify=certifi.where())  
  
    if r.status_code == 403:  
        exit('访问被拒绝，请检查是否为IP地址被禁')  
    param = re.findall(  
        r'src="https://js.mafengwo.net/js/hotel/sign/index.js(.*?)"', r.text)  
    param = param[0]  
    # 拼接 index.js 的文件地址  
    url_indexjs = 'https://js.mafengwo.net/js/hotel/sign/index.js' + param  
    # 获取 index.js    r = REQ.get(url_indexjs)  
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
~~~

1. 首先需要建立一个马蜂窝账户，并且保证其可用
2. 使用request进行登陆，获取index.js，这个js其中有自己的登陆信息，根据对于md5的介绍，可用使用这个js来模拟用户的登陆
3. 将index.js中的数据进行解密处理（这里是高科技的一部分，理解得不太透彻），应该不是直接的解密，而是将字符串中的一些特殊符号换掉，因为最后返回的`encrypted_string`实际上也是一个字符串

函数1最后返回的是一个字符串
## function02 md5 getcityPOIList
主要只讲解其中的   md5 函数

### headers（请求头）的设置 
这里是headders的第一次设置，后面还会为headers的设置交很多的学费
~~~ python
# 最简单的headers
HEADERS = headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '  
                  'Chrome/75.0.3770.142 Safari/537.36'}
~~~


简单讲一下headers的作用，实际上headers是用户用于请求服务端的数据，主要有以下几个作用：
1. 服务器判断用户的终端类型，比如上面的headers，就将自己伪装成了一个win10的chrome浏览器
2. 对于我们来说，因为大量网页使用user-agent这个参数来判断是不是爬虫在请求服务器，一次创建一个headers是很有必要的

### 代码解释
~~~ python
from functions.function_01_get_encrypted_string import _get_md5_encrypted_string  
import time  
import hashlib  
import json  
import requests  
HEADERS = headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '  
                  'Chrome/75.0.3770.142 Safari/537.36'}  
REQ = requests.session()  
REQ.headers=HEADERS  
encrypted_string = _get_md5_encrypted_string(REQ)  
def _md5(data):  
    '''  
    获取请求参数中的加密参数，_ts 和 _sn    '''    _ts = int(round(time.time() * 1000))  
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
    """    data = sorted(data.items(), key=lambda d: d[0])  
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
~~~
实际上我们并不是直接将function1中得到的字符串作为数据输入放到requests中然后请求数据，而是将 字符串encrypted_string + ts
(请求的时间)+sn（应该是一部分的请求字符串）一起作为一个postdata放到requests中


## function 03 （已经弃用）
函数3原本是通过 http://pagelet.mafengwo.cn/poi/pagelet/poiLocationApi 来获取每个poi的经纬度数据的，但是服务器端已经拒绝了访问，我也没有办法绕过，所以这个函数只能作废，但是通过函数的详细地址，能够进行地理编码，根据POI的门牌号获取对应的经纬度，并且进行坐标转换（来自地信学生的自信）

## function 04 transCoordinate
[参考网址](https://developer.aliyun.com/article/1281221)

看名字就知道，这是一个坐标转换的函数，function4的整个py实现了两个功能：
1. 地理编码，将地址编码为bd09或者gcj02的经纬度
2. 经纬度转换，将bd09或者gcj02的坐标转为wgs84的坐标

ps： 调用腾讯地图或者百度地图的api key需要自行获取

~~~ python
def tx_geoCoordinate(addr):  
    with open(r'E:\pycharm\keys\tx_key.txt','r',encoding='utf-8') as file:  
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
    with open(r'E:\pycharm\keys\bd_key.txt','r',encoding='utf-8') as file:  
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
  
        # res = req.read().decode()        time.sleep(0.1)  
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

~~~
提供了两个进行地理编码的方式，因为地理编码的api是有限制的，如果能够交替使用两个不同的地图进行地理编码就能效率最大化（露出了贫穷的笑容😀），或者找几个身边人借一下key也是可以的

上面的两个函数都十分简单，就是访问地图api，一般返回的是json数据，使用json进行解读，就能得到bd09或者gcj02的坐标，后面用类From_gcj02_to_wgs84（或者是From_bd09_to_wgs84）中的gcj02_to_wgs84(或bd09_to_wgs84)函数就能进行转换

## function04 getCitiesData
虽然这个函数也叫04，但是和上面的地理编码毫无干系，更像是后面的function05

函数作用：获取全国热门旅游城市的对应id
### 举出一个例子
这个函数是针对马蜂窝的[目的地主页](https://www.mafengwo.cn/mdd/)来设计的，除了获取国内城市的id，通过修改函数，还能够获取其他国外区域的数据

![[Pasted image 20240209190539.png]]
通过f12可以快速找到要获取的html中的一个列表（这个列表以及藏起来的列表都是可以直接获取的）

### 函数解析
~~~ python
# name:function_04_getCitiesData  
# 测试，查看一个城市中的POI的数量  
from functions.function_06_getHTML import html_crawler  
from bs4 import BeautifulSoup  
import pandas as pd  
import os  
  
#  提取城市数据  
# 检查CSV文件是否存在  
# todo 后面如果建立了数据库，就不用检查csv文件了，cache文件夹也不需要存在了，后面也会将这个函数的输出直接连接到数据库  
  
def getCitiesData():  
    csv_file_path = os.path.join('..', 'cache', 'cities_data.csv')  
  
    if os.path.exists(csv_file_path):  
        print("城市数据已存在，无需再次提取。")  
  
        exit()  
    else:  
        print("正在提取城市数据...")  
        url = 'https://www.mafengwo.cn/mdd/'  
        html_content = html_crawler(url)  
        soup = BeautifulSoup(html_content, 'html.parser')  
        # 找到包含城市信息的<div>标签  
        hot_list_div = soup.find('div', class_='hot-list clearfix')  
        # 找到<div>下的所有<dd>标签  
        dd_tags = hot_list_div.select('dd')  
        # 提取城市信息  
        # 提取城市信息并输出为字典列表  
        cities_list = []  
  
        for dd_tag in dd_tags:  
            # 找到<dd>标签中的所有城市链接  
            city_links = dd_tag.find_all('a', target='_blank')  
  
            # 构建字典列表  
            city_dicts = [{'city': link.get_text(strip=True),  
                           'link': link['href'],  
                           'poi_count': 0,  
                           'id': link['href'].rsplit('/', 1)[-1].rsplit('.', 1)[0]}  
                          for link in city_links  
                          ]  
  
            # 将当前<dd>标签中的城市字典列表加入总列表  
            cities_list.extend(city_dicts)  
  
        # 将字典列表转为DataFrame  
        df = pd.DataFrame(cities_list)  
        # 将DataFrame导出为CSV文件  
        df.to_csv('cities_data.csv', index=False)  
        print("城市数据提取完成。")  
        # 向df中添加poi数量，由于每次都要读一个网页，所以需要将csv每次都进行保存  
  
        cities_df = pd.read_csv(csv_file_path)  
        ids = cities_df['id']  
        # 去掉为空的项  
        ids = ids.dropna()  
        for city_id in ids:  
            if city_id is not None:  
                city_name = cities_df.loc[cities_df['id'] == city_id, 'city'].iloc[0]  
            else:  
                continue  
            try:  
                city_id_str = str(city_id).split('.')[0]  
                # 构建函数，输入城市名，查找这个城市的景点数量  
                url = f'https://www.mafengwo.cn/jd/{city_id_str}/gonglve.html'  
                # 使用条件筛选获取城市名称  
  
                # 检查 'poi_count' 对应的值是否为0  
                index_to_check = cities_df.index[cities_df['id'] == city_id].tolist()[0]  
                if cities_df.loc[index_to_check, 'poi_count'] == 0:  
                    html_content = html_crawler(url)  
                    soup = BeautifulSoup(html_content, 'html.parser')  
                    # 找到包含页数和条目数的<span>元素  
                    count_span = soup.find('span', class_='count')  
                    # 找到嵌套的所有<span>元素  
                    nested_spans = count_span.find_all('span')  
                    # 提取总条目数，位于第二个嵌套的<span>元素，即POI数量  
                    item_count = int(nested_spans[1].get_text(strip=True))  
                    # 在对应 id 列的那一行添加对应的 poi 数量  
                    index_to_update = cities_df.index[cities_df['id'] == city_id].tolist()[0]  
                    cities_df.loc[index_to_update, 'poi_count'] = item_count  
                    # 保存更新后的 DataFrame 到 CSV 文件  
                    cities_df.to_csv(csv_file_path, index=False)  
                    print(f"{city_name} 的景点数获取完毕。")  
                elif cities_df.loc[index_to_check, 'poi_count'] == -1:  
                    print(f"{city_name} 的景点数获取失败，将该城市的景点数设为 -1")  
                else:  
                    print(f"{city_name} 的景点数已存在，无需再次获取。")  
            except Exception as e:  
                print(f"An error occurred for city_id {city_name}: {str(e)},将该城市的景点数设为 -1")  
                # 在对应id列的那一行添加 poi_count 设为 -1                index_to_update = cities_df.index[cities_df['id'] == city_id].tolist()[0]  
                cities_df.loc[index_to_update, 'poi_count'] = -1  
                # 保存更新后的 DataFrame 到 CSV 文件  
                cities_df.to_csv(csv_file_path, index=False)
~~~
整个函数看起来很长，但是实际上十分简单，主要就是使用beautifulsoup来解析https://www.mafengwo.cn/mdd/这个网页，将自己想要的信息获取下来，在这里，我们将html中class为`hot-list clearfix`的div元素整体获取下来
~~~ python
hot_list_div = soup.find('div', class_='hot-list clearfix')
~~~
得到的就是我们想要的列表


## function 05 getPOIID
获取一个城市中的300个初始的POI

由于马蜂窝网页版的限制，在网页端，无论一个城市有多少个POI，最后能够爬下来的POI只有300个景点的ID

### 举出一个例子
以[北京市](https://www.mafengwo.cn/jd/10065/gonglve.html)为例
![[Pasted image 20240209184607.png]]
每页有15个景点，共20页，也就是一共300个，但是截图中显示北京市总共有15251个景点，这些景点理论上是能够获取的，但是仅对于目前而言暂时是没有必要的，后面也会简单聊到提取所有这些景点的id的可能方法

~~~ python
import re  
from bs4 import BeautifulSoup  
import requests  
import pandas as pd  
from functions.function_02_md5_getCityPOIList import _md5  
HEADERS = headers = {  
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '  
                  'Chrome/75.0.3770.142 Safari/537.36'}  
REQ = requests.session()  
REQ.headers=HEADERS  
# 获取一个城市的POI和对应的编号  
def _get_route(mdd_id):  
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

~~~






### PS 关于POIID爬取的一些想法
暂时跳过


### 代码解释
跳过对From_bd09_to_wgs84和From_gcj02_to_wgs84的解释



## 说在最后
1. 从零构建一个爬虫确实是一件十分困难的事情，站在前人的肩膀上才能更好的进化嘿嘿嘿
