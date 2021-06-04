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
            if i == 30:
                break
            link = "http://torank.cf/bbs/board.php?bo_table=todal_"+site+"&page="+str(i)
            post_one  = s.get(link)
            content = post_one.content
            soup = bs(content.decode('utf8','replace'), 'html.parser')
            try:
                if site == 'kmovie':
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
                        url = item.find('a', 'ellipsis')['href']
                        if url.find('&page=') != -1:
                            url = url.split('&page=')[0].strip()
                        if url.find('http:') == -1:
                            url = 'http:'+url
                        cnt_num = url.split('wr_id=')[1].strip()

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'torank',
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
                    td = soup.find_all('td', 'list-subject')
                    for item in td:
                        title = item.find('a').text.strip()
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
                        if url.find('&page=') != -1:
                            url = url.split('&page=')[0].strip()
                        if url.find('http:') == -1:
                            url = 'http:'+url
                        cnt_num = url.split('wr_id=')[1].strip()

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'torank',
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

    print("torank 크롤링 시작")
    site = ['kmovie','drama','ent','ani','kds']
    for s in site:
        startCrawling(s)
    print("torank 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
