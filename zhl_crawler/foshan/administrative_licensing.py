from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import json
import pandas as pd
import time
import xlsxwriter

'''
爬虫：获取佛山出租车汽车信息查询系统信息
路径 ：行政许可 -》网约许可 
'''

out_put='D:\\My\\Python\\data\\administrative_licensing_'+str(round(time.time()))+'.xlsx'
total_page =  5  #总页数，每次执行需要修改


total_rows = []
read_timeout_list = []
read_timeout_warning=[]
for i in range(1,total_page+1):

    url = 'http://218.13.12.75:10013/api/v1/WYCGZWZ/WYCGZWZ/GetXingZhengXuKeList?Page='+str(i)+'&Rows=50&ShenQingLiuShuiHao=++&_=1573374369610'
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
        # 分割身份证号
        index = row['CaoZuoRenMingCheng'].find('_')
        card_id = ''
        if(index != -1):
            card_id = row['CaoZuoRenMingCheng'][index+1:]
        row['card_id'] = card_id
        all_records.append(row)

df = pd.DataFrame(all_records)
try:
    with pd.ExcelWriter(out_put) as writer:
        df.to_excel(writer, engine='xlsxwriter',sheet_name='Sheet1')
except:
    excpet_out_put='D:\\My\\Python\\data\\administrative_licensing_'+str(round(time.time()))+'.txt'
    print(' DataFrame to excel get some issue , please check !  Exception output ' + excpet_out_put)
    with open(excpet_out_put,mode='w',encoding='utf-8') as fo:
        fo.writelines(df)

if(len(read_timeout_warning)==0):
    print(' All data generate successfully ! And output file is : ' + out_put)
else:
    print(' ########################  Warning  ############################### ')
    print(' There can not get some page data, you need to manual download ! ')

for i in read_timeout_warning:
    print(i)
