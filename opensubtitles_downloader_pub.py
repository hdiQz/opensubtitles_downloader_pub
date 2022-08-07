from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import requests
import os

os.chdir('~')

print('开始运行')
tconst = pd.read_csv('~', delimiter=',', encoding='utf-8') #文件获取途径看说明
df = pd.DataFrame(tconst)
row_num = df.shape[0] #读取行数
for m in range(0, row_num):
    tt = df.iloc[m, 0]
    print('电影：', tt)
    tt_num = tt.replace('tt', '')
    url_search = 'https://www.opensubtitles.org/zh/search/sublanguageid-eng/imdbid-' + str(tt_num) + '/sort-6/asc-0' #搜索英文字幕，按评分降序排列
    html_search = requests.get(url_search).text
    soup = BeautifulSoup(html_search, 'html.parser')
    msg_span = soup.find('span', {'style': 'float:right;'})
    try:
        sub_num = msg_span.select('b')[2].text
    except:
        sub_num = None
    print('字幕数量：', sub_num)
    if sub_num == None:
        continue
    else:
        find_tr = soup.find('tr', {'class':'change even expandable'})
        select_td = find_tr.select('td')[4]
        find_a = select_td.find('a')
        dl_num = find_a['href']
        dl_num = dl_num.replace('/zh/subtitleserve/sub/', '')
        download_url = 'https://dl.opensubtitles.org/zh/download/sub/' + dl_num
        IDM_Path = '~' #idm目录
        download_path = '~' #下载目录
        filename = tt + '.zip'
        os.chdir(IDM_Path)
        IDM = "IDMan.exe"
        command = ' '.join([IDM, '/d', download_url, '/p', download_path, '/f', filename, '/q'])
        os.system(command)
        print(tt, '下载中')
print('结束运行')
