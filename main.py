
"""
File: main.py

Description:
    爬取全国医院相关信息

Author: paceboy
Date Created: 2024-10-31
Last Modified: 2024-10-31

"""

from service import reptile

if __name__ == '__main__':
    print(f'The miracle is starting ...')
    reptile.init()
    # 循环访问链接获取信息
    for province in reptile.get_province_name():
        print(province)
        reptile.get_province_hospital(province)

