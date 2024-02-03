# builder:wstki
# 开发时间21:43,2024/2/2
# name:test12_city_POInumber
# 测试，查看一个城市中的POI的数量
from functions.function_06_getHTML import html_crawler
from bs4 import BeautifulSoup
import pandas as pd
import os

#  提取城市数据
# 检查CSV文件是否存在
csv_file_path = '..\cache\cities_data.csv'
if  os.path.exists(csv_file_path):
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
                       'poi_count':0,
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
            # 在对应id列的那一行添加 poi_count 设为 -1
            index_to_update = cities_df.index[cities_df['id'] == city_id].tolist()[0]
            cities_df.loc[index_to_update, 'poi_count'] = -1
            # 保存更新后的 DataFrame 到 CSV 文件
            cities_df.to_csv(csv_file_path, index=False)
