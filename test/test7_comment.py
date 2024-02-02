# builder:wstki
# 开发时间14:50,2024/2/2
# name:test7_comment
# 构建一个爬取景点评论、评分、景点介绍、开放时间、门票等等的数据的test
import requests
from bs4 import BeautifulSoup
from js2py import eval_js
import js2py
from functions.function_01_get_encrypted_string import _get_md5_encrypted_string
from functions.function_02_md5_getCityPOIList import _md5


headers = {
    'Cookie':'__jsluid_s=8cfd058d0c90defead62c2650f641e5c; mfw_uuid=65bb0081-a8a9-3acd-5d64-dfd40246ffab; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222024-02-01+10%3A22%3A57%22%3B%7D; uva=s%3A92%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1706754178%3Bs%3A10%3A%22last_refer%22%3Bs%3A24%3A%22https%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1706754178%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=65bb0081-a8a9-3acd-5d64-dfd40246ffab; __omc_chl=; login=mafengwo; mafengwo=088d9da52bee1bfc15c89db531ffeb29_47825567_65bb0352d5f753.34317781_65bb0352d5f7a0.83381501; __jsluid_h=1b099d7a9762ee6818af68324510b352; PHPSESSID=troj8d594q84unselho826epf3; _r=bing; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A12%3A%22cn.bing.com%2F%22%3Bs%3A1%3A%22t%22%3Bi%3A1706840772%3B%7D; mfw_uid=47825567; __mfwothchid=referrer%7Ccn.bing.com; __mfwc=referrer%7Ccn.bing.com; bottom_ad_status=0; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1706754177,1706840773; __omc_r=; __mfwa=1706754176034.29533.9.1706861587839.1706864804003; __mfwlv=1706864804; __mfwvn=8; uol_throttle=47825567; __jsl_clearance_s=1706868478.978|0|eKlX9l7kv2r99ugoodejaXmbViE%3D; __mfwb=49cbf8634b10.23.direct; __mfwlt=1706868713; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1706868714',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36'
}
url = 'http://www.mafengwo.cn/poi/3474.html'
# 发送GET请求
response = requests.get(url, headers=headers,verify=False)
print(response.text)
result = eval_js(response.text)
# 检查请求是否成功
if response.status_code == 200:
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)

    # 提取所有文本信息
    all_text = soup.get_text()

    # 打印所有文本信息
    print(all_text)
else:
    print(f"请求失败，状态码: {response.status_code}")