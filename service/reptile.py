import requests, re, datetime
from bs4 import BeautifulSoup  # 解析网页数据
import xlwt  # 写入excel
import random


# 初始化
def init():
    global url, province_name, headers
    # 爬取文件地址
    url = 'https://www.yixue.com/'
    #  存储各省名称
    province_name = [
        '北京市', '天津市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '上海市',
        '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省',
        '湖南省', '广东省', '内蒙古自治区', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省',
        '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区'
    ]

    headers = {
        # 浏览器信息
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "user-agent": random_user_agent(),
        # 从哪里来
        "Referer": "https://www.yixue.com/",
        # 用户信息
        "cookie": "newstatisticUUID=1651282597_602532090; _csrfToken=rmG7zCbbkD7QK34BymosH69Xve6eibDLGzeI2q8q; pageOps=1; fu=1403875312; qdrs=0|3|0|0|1; showSectionCommentGuide=1; qdgd=1; lrbc=1033272309|702228691|0; rcr=1033272309; bc=1033272309; _gid=GA1.2.364214729.1651282600; readadclose=1; _gat_gtag_UA_199934072_2=1; _ga_FZMMH98S83=GS1.1.1651282598.1.1.1651282753.0; _ga_PFYW0QLV3P=GS1.1.1651282598.1.1.1651282753.0; _ga=GA1.2.279552178.1651282599"
    }

def get_province_name():
    return province_name

# 随机取数
def random_user_agent():
    ulist = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"]

    # 随机从列表中取值
    # print(random.choice(ulist))
    # 0,列表长度中取值
    return ulist[random.randint(0, len(ulist) - 1)]


# 存储数据
def sav_message(messgae, province_now):
    # 创建一个excel表格用来写入信息
    workbook = xlwt.Workbook(encoding='utf-8')
    name = province_now + "医院列表"
    # 添加工作表
    table = workbook.add_sheet(name)
    value = ["医院名称", "医院地址", "联系电话", "医院等级", "重点科室", "经营方式", "传真号码", "电子邮箱", "医院网站"]
    # 添加表头信息
    for i in range(len(value)):
        # 行,列,值 写入
        table.write(0, i, value[i])
    i = 0
    for data in messgae[4]: # 获取医院信息位置
        if len(data) <= 1:
            continue
        else:
            try:
                # 写入医院名称
                # hospltal = data.b.a.text
                table.write(i + 1, 0, data.b.a.text)
                for data_1 in data.ul:
                    now_mess = data_1.text.replace('\n', '')
                    now_data = now_mess.split('：')
                    count = 0
                    for tittle in value:
                        if tittle == now_data[0]:
                            index = count
                            table.write(i + 1, index, now_data[1])
                        count = count + 1
                i = i + 1
            except:
                print(data.b.text + "这家医院爬取失败")
    # 保存一个excle数据表格
    workbook.save('assets/' + province_now + '医院列表.xls')


# 获取当前省数据
def get_province_hospital(province_now):
    # 访问链接
    r = requests.get(url + province_now + '医院列表', headers=headers, timeout=10)
    # 数据分析
    # 加载  设置解析器
    soup = BeautifulSoup(r.text, "lxml")
    # 获取页面内容
    message = soup.find_all('ul')
    sav_message(message, province_now)


# 主函数
# if __name__ == '__main__':
#     init()
#     # 循环访问链接获取信息
#     for province in province_name:
#         # print(province)
#         get_province_hospital(province)
