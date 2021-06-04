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

def startCrawling(key):
    keyword = key
    keywordCh = keyword.replace(' ', '')
    print('키워드: '+keyword)
    i = 0;check = True; title_check = ''; titleCh = True
    link = 'https://torrent6.ibe.kr/bbs/search.php?sfl=wr_subject&stx='+keyword+'&sop=and&gr_id=&srows=15&onetable=&page='
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            if soup.find('div', 'media-heading'):
                div = soup.find_all('div', 'media-heading')
                if len(div) <= 2:
                    break
                try:
                    for item in div:
                        acheck = item.find_all('a')
                        if len(acheck) == 1:
                            title = item.find('a').text.strip()
                            if title.find('대박나거라') != -1 or title.find('운수대통') != -1:
                                continue
                            title_null = titleNull(title)
                            # 키워드 체크
                            if title_null.find(keywordCh) == -1:
                                continue
                            url = 'https://torrent6.ibe.kr/bbs'+item.find('a')['href']
                            if url.find('&no=') != -1:
                                url = url.split('&no=')[0]
                                cnt_num = url.split('wr_id=')[1].strip()
                            else:
                                cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')
                        else:
                            title = item.find_all('a')[1].text.strip()
                            title_null = titleNull(title)
                            # 키워드 체크
                            if title_null.find(keywordCh) == -1:
                                continue
                            url = 'https://torrent6.ibe.kr/bbs'+item.find_all('a')[1]['href']
                            if url.find('&no=') != -1:
                                url = url.split('&no=')[0]
                                cnt_num = url.split('wr_id=')[1].strip()
                            else:
                                cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')

                            data = {
                                'Cnt_num' : cnt_num,
                                'Cnt_osp' : 'torrent6.ibe',
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

    print("torrent6.ibe 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("torrent6.ibe 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
