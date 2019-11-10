from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import json
import pandas as pd
import time

'''
爬虫：获取佛山出租车汽车信息查询系统信息
路径 ：数据查询 -》 网约车 -》驾驶员
'''

out_put='D:\\data_search_driver_'+str(round(time.time()))+'.xlsx'
total_page = 5  #总页数，每次执行需要修改


total_rows = []
read_timeout_list = []
read_timeout_warning=[]
for i in range(1,total_page+1):

    url = 'http://218.13.12.75:10013/api/v1/WYCGZWZ/WYCGZWZ/GetJiaShiYuanList?Page='+str(i)+'&Rows=50&XingMing=++&ShenFenZhengHaoMa=++&_=1569656652514'
          # 'http://218.13.12.75:10013/api/v1/WYCGZWZ/WYCGZWZ/GetWangYueCheList?Page=1&Rows=50&ChePaiHao=++&DaoLuYunShuZhengHao=&_=1573372643286'
          # 'http://218.13.12.75:10013/api/v1/WYCGZWZ/WYCGZWZ/GetJiaShiYuanList?Page=1&Rows=50&XingMing=++&ShenFenZhengHaoMa=&_=1573372814564'

    print(url)
    try:
        f = requests.get(url,timeout=30)
    except:
        read_timeout_list.append(url)
    soup = BeautifulSoup(f.content, "lxml")
    response = str(soup.find('p')).replace('<p>', '').replace('</p>', '')
    rows = json.loads(response)['rows']
    total_rows.append(rows)

# try again the timeout url
print(len(read_timeout_list))
for url in read_timeout_list:
    try:
        f = requests.get(url, timeout=60)
    except:
        read_timeout_warning.append(url)

    soup = BeautifulSoup(f.content, "lxml")
    response = str(soup.find('p')).replace('<p>', '').replace('</p>', '')
    rows = json.loads(response)['rows']
    total_rows.append(rows)


all_records= []
for page in total_rows:
    for row in page:
        all_records.append(row)

df = pd.DataFrame(all_records)
with pd.ExcelWriter(out_put) as writer:
    df.to_excel(writer,sheet_name='Sheet1')


if(len(read_timeout_warning)==0):
    print(' All data generate successfully ! ')
    print(' All data generate successfully ! And output file is : ' + out_put)
else:
    print(' ########################  Warning  ############################### ')
    print(' Warning !!! There can not get some page data, you need to manual download ! ')

for i in read_timeout_warning:
    print(i)
