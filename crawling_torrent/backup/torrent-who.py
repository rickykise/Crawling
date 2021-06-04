import requests,re
import pymysql,time,datetime
import urllib.parse
from webhardFun import *
from urllib.parse import unquote
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = "https://torrent-who.com/bbs/board.php?bo_table="+site+"&page="+str(i)
            post_one  = s.get(link)
            content = post_one.content
            soup = bs(content.decode('utf8','replace'), 'html.parser')
            try:
                if site == 'movie':
                    div = soup.find('div', 'list-container').find_all('div', 'list-row')
                    for item in div:
                        title = item.find('a', 'ellipsis').text.strip()
                        title_null = titleNull(title)
                        # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_null, getKey)
                        if keyCheck['m'] == None:
                            continue
                        keyCheck2 = checkTitle2(title_null, getKey)
                        if keyCheck2['m'] == None:
                            continue
                        cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')
                        url = item.find('a', 'ellipsis')['href']

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'torrent-who',
                            'Cnt_title': title,
                            'Cnt_title_null': title_null,
                            'Cnt_url': url,
                            'Cnt_price': '',
                            'Cnt_writer' : '',
                            'Cnt_vol' : '',
                            'Cnt_fname' : '',
                            'Cnt_chk': 0
                        }
                        # print(data)
                        # print('=============================================')

                        dbResult = insertALL(data)
                else:
                    li = soup.find('ul', 'list-body').find_all('li', 'list-item')
                    for item in li:
                        title = item.find('a', 'item-subject').text.strip()
                        title_null = titleNull(title)
                        # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_null, getKey)
                        if keyCheck['m'] == None:
                            continue
                        keyCheck2 = checkTitle2(title_null, getKey)
                        if keyCheck2['m'] == None:
                            continue
                        cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')
                        url = item.find('a', 'item-subject')['href']

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'torrent-who',
                            'Cnt_title': title,
                            'Cnt_title_null': title_null,
                            'Cnt_url': url,
                            'Cnt_price': '',
                            'Cnt_writer' : '',
                            'Cnt_vol' : '',
                            'Cnt_fname' : '',
                            'Cnt_chk': 0
                        }
                        # print(data)
                        # print('=============================================')

                        dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("torrent-who 크롤링 시작")
    site = ['movie','drama','entertain','tv','ani']
    for s in site:
        startCrawling(s)
    print("torrent-who 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
