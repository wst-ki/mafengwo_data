# builder:wstki
# 开发时间19:10,2024/2/5
# name:function_09_getUserComment
# 以用户为主题获取每个用户的评论
from functions.function_06_getHTML import html_crawler
import bs4 as bs


# todo 后面在使用的时候需要加入一个判断，id是否已经在数据库中，如果有就不重复爬取
def getUserComment(user_id):
    """
    获取用户评论
    :param id: 输入的是每个用户的id
    :return: 返回用户的评论信息、性别（如果有）、现居地
    """
    url = f'https://www.mafengwo.cn/u/{user_id}/note.html'
    html_content = html_crawler(url)
    # 如果没有游记就跳过这个用户
    # 如果有游记就看看能不能获得所有游记的链接
    soup = bs.BeautifulSoup(html_content, 'html.parser')
    # 找到包含游记的 div 元素
    div_for_travelogue = soup.find('div', {'class': 'MAvaNums'})
    # 提取游记的数量
    travelogue_count = div_for_travelogue.find('strong').get_text(strip=True)
    # 用于存储已提取的文章编号的集合
    seen_article_ids = set()
    print("游记数量:", travelogue_count)
    if int(travelogue_count) > 0:
        # 提取用户名
        info = html_crawler(f'https://www.mafengwo.cn/u/{user_id}.html')
        info_soup = bs.BeautifulSoup(info, 'html.parser')
        username = info_soup.find('div', class_='MAvaName').get_text(strip=True)
        # 提取这个用户的信息，比如性别和居住地
        # 提取居住地
        try:
            location = info_soup.select('.MAvaPlace.flt1')[0].get_text(strip=True).split('：')[-1]
        except:
            location = None
        # 提取性别
        try:
            gender_content = info_soup.select('.MGenderFemale.mfw-acc-hide')[0]
            class_value = gender_content.get('class')
            gender_class = next((cls for cls in class_value if 'Gender' in cls), None)
            gender = gender_class.replace('MGender', '')

        except:
            gender = None
        # 找到包含所有游记的元素
        ul_element = soup.find('div', class_='notes_list')
        # 提取所有包含链接的 a 元素
        a_elements = ul_element.find_all('a', href=True)
        # 提取链接中的文章编号
        for a_element in a_elements:
            link_href = a_element['href']
            article_id = link_href.split('/')[-1].split('.')[0]
            # 检查文章编号是否已经在集合中
            if article_id not in seen_article_ids:
                # 如果编号不在集合中，添加到集合并进行处理
                seen_article_ids.add(article_id)
        # 将每篇游记都下载下来
        articles = []
        for id in seen_article_ids:
            # test cache E:\pycharm\mafengwo_data\cache\test.html https://www.mafengwo.cn/i/{int(id)}.html
            try:
                id = int(id)
                article_url = f'https://www.mafengwo.cn/i/{int(id)}.html'
            except:
                continue
            article_html_content = html_crawler(article_url)
            # 如果长期获取不到就跳过吧
            if article_html_content == 'error,长期无法连接，已跳过':
                continue
            article_soup = bs.BeautifulSoup(article_html_content, 'html.parser')
            travel_info = {}
            try:
                print("默认有头图")
                # 获取文章标题
                title_text = article_soup.find('div', class_='vi_con').find('h1').get_text(strip=True)

                # 获取旅程相关信息
                # 使用try except
                # travel_info_div = soup.find_all('div', class_=["tarvel_dir_list", "clearfix"])

                try:
                    travel_info_div = article_soup.select('.tarvel_dir_list.clearfix')[0]

                    if travel_info_div:
                        ul = travel_info_div.find('ul')
                        if ul:
                            for li in ul.find_all('li'):
                                key = li.get_text(strip=True).split('／')[0].split('/')[0]
                                value = li.get_text(strip=True).split('／')[0].split('/')[1] if len(
                                    li.get_text(strip=True).split('／')[0]) != 0 else None
                                travel_info[key] = value
                except:
                    travel_info_div = None

                # 获取文章内容
                article_content = article_soup.find('div', class_='_j_content_box')
                article_texts = article_content.find_all('p')
                # 建立空列表，存储每段文本
                article_text = []
                for paragraph in article_texts:
                    paragraph_text = paragraph.get_text(strip=True)
                    article_text.append(paragraph_text)
                article = ' '.join(article_text)
                article_info = {
                    'title': title_text,
                    'travel_info': travel_info,
                    'article': article,
                    'article_id': id
                }
                articles.append(article_info)
            except:
                print("无头图测试")
                title_text = article_soup.select('.post_title.clearfix')[0].find('h1').get_text(strip=True)
                travel_info_div = article_soup.select('.tarvel_dir_list.clearfix')[0]

                try:
                    travel_info_div = article_soup.select('.tarvel_dir_list.clearfix')[0]

                    if travel_info_div:
                        ul = travel_info_div.find('ul')
                        if ul:
                            for li in ul.find_all('li'):
                                key = li.get_text(strip=True).split('／')[0].split('/')[0]
                                value = li.get_text(strip=True).split('／')[0].split('/')[1] if len(
                                    li.get_text(strip=True).split('／')[0]) != 0 else None
                                travel_info[key] = value
                except:
                    travel_info_div = None
                # 获取文章内容
                article_content = article_soup.select('.a_con_text.cont')[0]
                article_texts = article_content.find_all('p')
                # 建立空列表，存储每段文本
                article_text = []
                for paragraph in article_texts:
                    paragraph_text = paragraph.get_text(strip=True)
                    article_text.append(paragraph_text)
                article = ' '.join(article_text)
                article_info = {
                    'title': title_text,
                    'travel_info': travel_info,
                    'article': article,
                    'article_id': id
                }
                articles.append(article_info)
        user_info = {
            'username': username,
            'gender': gender,
            'user_id': user_id,
            'articles': articles
        }
        print(user_info)
        return user_info
    else:
        print("该用户没有游记，已经跳过该用户")
        return None
