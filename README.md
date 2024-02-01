# 数据获取的基本流程
部分参考了这个网页
https://blog.csdn.net/yuchunyu97/article/details/89504740
但是方法需要大量修改

## 1 获取登录字符串
首先需要一个马蜂窝账号，用来登陆网站，不是的话后面什么都做不了

~~~ python
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
主要的问题在于   https://js.mafengwo.net/js/hotel/sign/index.js ，需要通过这个网址来获取一个特殊的字符串encrypted_string用于验证身份


## 2 使用md5获取单个城市中的所有景点POI
