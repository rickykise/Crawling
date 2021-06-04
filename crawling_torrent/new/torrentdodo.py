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
    link = 'https://torrentdodo.com/bbs/search.php?sfl=wr_subject%7C%7Cwr_content&stx='+keyword+'&sop=and&gr_id=&srows=100&onetable=&page='
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            if soup.find('div', 'sch_tit'):
                div = soup.find_all('div', 'sch_tit')
                try:
                    for item in div:
                        title = item.find('a').text.strip()
                        title_null = titleNull(title)
                        # 키워드 체크
                        keyCheck = checkTitle(title_null, keyword, cnt_id)
                        if keyCheck['m'] == None:
                            continue
                        url = 'https://torrentdodo.com/bbs/'+item.find('a')['href'].split('./')[1]
                        if url.find('&page=') != -1:
                            url = url.split('&page=')[0].strip()
                        cnt_num = url.split('wr_id=')[1].strip()

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'torrentdodo',
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

    print("torrentdodo 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("torrentdodo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
