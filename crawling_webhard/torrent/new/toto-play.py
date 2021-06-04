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

def startCrawling(key, id):
    keyword = key;cnt_id = id[0]
    keywordCh = keyword.replace(' ', '')
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://toto-play.com/bbs/board.php?bo_table=tventer&sfl=wr_subject&stx='+keyword+'&sop=and&page='
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            if soup.find('li', 'list-item'):
                li = soup.find_all('li', 'list-item')
                try:
                    for item in li:
                        title = item.find('a').text.strip()
                        title_null = titleNull(title)
                        # 키워드 체크
                        keyCheck = checkTitle(title_null, keyword, cnt_id)
                        if keyCheck['m'] == None:
                            continue
                        url = item.find('a')['href']
                        if url.find('&sfl') != -1:
                            url = url.split('&sfl')[0].strip()
                        url = urllib.parse.unquote(url)
                        cnt_num = url.split('wr_id=')[1].split('&')[0].strip()

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'toto-play',
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
            else:
                break

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeyword()

    print("toto-play 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("toto-play 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
