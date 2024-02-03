# builder:wstki
# 开发时间14:09,2024/2/3
# name:test_13_B_comment
# 看看能不能调用已有的api来获取评论
import re
import requests
import bs4 as bs
import json
#评论内容所在的url，？后面是get请求需要的参数内容

# 理顺一下逻辑
# 首先是需要POI对应的url作为header中的referer
# 所以header需要每次都更新
# 然后是获取到的评论内容，应该是json，但是需要进行处理，提取有用信息

def crawler_comment(POI,page):
    """
    如果不使用fiddler抓包，就只能获得最多50条评论
    :param POI: 要获取的景点的POI的id
    :param page: 这个景点有几页评论
    :return: 返回一个列表，列表中是评论的内容
    """
    comment_url='http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?'
    requests_headers = {
    'Referer': f'http://www.mafengwo.cn/poi/{POI}.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }  # 请求头
    for num in range(1, page+1):
        requests_data = {
        'params': '{{"poi_id":"{}","page":"%d","just_comment":1}}'.format(POI) % (num)
        }
        response = requests.get(url=comment_url, headers=requests_headers, params=requests_data)
        if 200 == response.status_code:
            # 解析 JSON 字符串
            json_data = json.loads(response.text)
            html_content = json_data['data']
            # 获取键为 'html' 的值
            html_content = html_content.get('html', '')
            # 返回的结果是一个json，里面装着一个html，所以要用bf来解释
            soup = bs.BeautifulSoup(html_content, 'html.parser')
            # 找到包含评论的ul元素
            ul_element = soup.find('div', class_='rev-list').find('ul')

            # 获取所有li元素
            li_elements = ul_element.find_all('li')

            # 遍历li元素，提取内容并存入字典
            reviews_list = []
            for li_element in li_elements:
                # 添加条件判断，只处理class="rev-item comment-item clearfix"的li元素
                if 'rev-item' in li_element.get('class', []) and 'comment-item' in li_element.get('class',
                                                                                                  []) and 'clearfix' in li_element.get(
                    'class', []):
                    user_name = li_element.find('a', class_='name').get_text(strip=True)
                    comment_text = li_element.find('p', class_='rev-txt').get_text(strip=True)
                    review_dict = {'name': user_name, 'comment': comment_text}
                    reviews_list.append(review_dict)

            return(reviews_list)

crawler_comment(3474,5)