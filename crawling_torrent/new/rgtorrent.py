import requests,re
import pymysql,time,datetime
import urllib.parse
from webhardFun import *
from urllib.parse import unquote
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup


def startCrawling(site):
    i = 0;check = True
    link = 'https://www.rgtorrent.org/bbs/board.php?bo_table='+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find('div', 'tbl_head01').find('tbody').find_all('tr')

        try:
            for item in tr:
                title = item.find('a')['title']
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                url = item.find('a')['href']
                cnt_num = url.split('wr_id=')[1].strip()
                if cnt_num.find('&page=') != -1:
                    cnt_num = cnt_num.split('&page=')[0].strip()

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'rgtorrent',
                    'Cnt_title': title,
                    'Cnt_title_null': title_null,
                    'Cnt_url': url,
                    'Cnt_price': '',
                    'Cnt_writer' : '',
                    'Cnt_vol' : '',
                    'Cnt_fname' : '',
                    'Cnt_chk': 0
                }
                print(data)
                print('=============================================')

                # dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("rgtorrent 크롤링 시작")
    site = ['kr_drama', 'kr_drama1', 'kr_ent', 'kr_ent1', 'fun_tv', 'drama_tv', 'ani']
    for s in site:
        startCrawling(s)
    print("rgtorrent 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
