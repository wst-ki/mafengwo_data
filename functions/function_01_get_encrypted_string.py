# builder:wstki
# 开发时间17:05,2024/2/1
# name:get_encrypted_string_01
# 这是整个程序的第一步，先要登陆马蜂窝账号才能进行这步,是一个函数，函数不需要输入，但是会输出一个唯一值encrypted_string
import requests
import re
import certifi
def _get_md5_encrypted_string(REQ):

    # 以北京景点为例，首先获取加密 js 文件的地址
    url = 'https://www.mafengwo.cn/jd/10065/gonglve.html'
    r = REQ.get(url,verify=certifi.where())

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