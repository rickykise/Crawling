import requests,re
import pymysql,time,datetime
import urllib.parse
from webhardFun import *
from urllib.parse import unquote
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Host': 'torrentsky.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key, id):
    keyword = key;cnt_id = id[0]
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'http://torrentsky.net/bbs/search.php?sfl=wr_subject%7C%7Cwr_content&stx='+keyword+'&sop=and&gr_id=&srows=10&onetable=&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        if soup.find('div', 'media-heading'):
            div = soup.find_all('div', 'media-heading')
            try:
                for item in div:
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    keyCheck = checkTitle(title_null, keyword, cnt_id)
                    if keyCheck['m'] == None:
                        continue
                    url = 'http://torrentsky.net/bbs/'+item.find('a')['href'].split('./')[1]
                    if url.find('&page=') != -1:
                        url = url.split('&page=')[0].strip()
                    cnt_num = url.split('wr_id=')[1].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'torrentsky',
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

    print("torrentsky 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("torrentsky 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
