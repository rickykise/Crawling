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
            link = "https://torrenthaja4.com/bbs/board.php?bo_table=torrent_"+site+"&page="+str(i)
            post_one  = s.get(link)
            content = post_one.content
            soup = bs(content.decode('utf8','replace'), 'html.parser')
            tr = soup.find('div', 'board-list-body').find('tbody').find_all('tr')
            try:
                for item in tr:
                    td = item.find_all('td')
                    if len(td) == 1:
                        continue
                    titleCheck = len(item.find('td', 'td-width').find_all('a'))
                    if titleCheck != 1:
                        title = item.find('td', 'td-width').find_all('a')[1].text.strip()
                        url = item.find('td', 'td-width').find_all('a')[1]['href']
                        if url.find('page') != -1:
                            url = url.split('?page')[0]
                    else:
                        title = item.find('td', 'td-width').find('a').text.strip()
                        url = item.find('td', 'td-width').find('a')['href']
                        if url.find('page') != -1:
                            url = url.split('?page')[0]
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


                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'torrenthaja',
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

    print("torrenthaja 크롤링 시작")
    site = ['kmovie','drama','ent','docu','ani']
    for s in site:
        startCrawling(s)
    print("torrenthaja 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
