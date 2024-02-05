# builder:wstki
# 开发时间14:19,2024/2/5
# name:test15_b_multiClass
# 一个元素有多个类，soup应该如何操作
from bs4 import BeautifulSoup
import os
html = """
<html>
<head>
<style>
    .class1 {
        color: red;
    }
    .class2 {
        font-weight: bold;
    }
</style>
</head>
<body>
<p class="class1 class2">This is a paragraph with class1 and class2.</p>
<p class="class1">This is a paragraph with only class1.</p>
<p class="class2">This is a paragraph with only class2.</p>
</body>
</html>
"""
url = os.path.join('..','cache','test.html')
with open(url, 'r', encoding='utf-8') as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser')

# 使用CSS选择器指定多个类的查找条件
elements = soup.select('.tarvel_dir_list.clearfix')
for element in elements:
    print(element.text)
