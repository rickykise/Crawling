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
            link = "https://www.tfreeca3.com/board.php?mode=list&b_id="+site+"&page="+str(i)
            post_one  = s.get(link)
            content = post_one.content
            soup = bs(content.decode('utf8','replace'), 'html.parser')
            tr = soup.find('table', 'b_list').find_all('tr')
            try:
                for item in tr:
                    if item.find('td', 'subject'):
                        title = item.find('a', re.compile("stitle+")).text.strip()
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
                        urlCheck = item.find('a', re.compile("stitle+"))['href']
                        b_id = urlCheck.split('&b_id=')[1].split('&')[0]
                        id = urlCheck.split('&id=')[1].split('&')[0]
                        url = 'https://www.tfreeca3.com/board.php?mode=view&b_id='+b_id+'&id='+id

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'tfreeca',
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

    print("tfreeca 크롤링 시작")
    site = ['tmovie','tdrama','tent','tv','tani']
    for s in site:
        startCrawling(s)
    print("tfreeca 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
