# builder:wstki
# 开发时间10:22,2024/2/5
# name:test_14_commentToCSV
# 测试function8能不能实现
from functions.function_08_getPOIcomment import  get_mdd_POIcomment
import os
cityID_list = [10088]
csv_path = os.path.join('..','cache',f'{10088}.csv')
get_mdd_POIcomment(cityID_list,csv_path)