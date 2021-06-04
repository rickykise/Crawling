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

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cookie': '__cfduid=d37ed378ee0f07a0ef24b3c287f6748031565764297; _ga=GA1.2.1392470427.1565764302; _gid=GA1.2.125641225.1565764302; _gat_gtag_UA_129151866_6=1',
    'Host': 'tabomtorrent2.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            link = "https://tabomtorrent2.com/category/"+site+"/page/"+str(i)+"/"
            post_one  = s.get(link, headers=headers)
            content = post_one.content
            soup = bs(content.decode('utf8','replace'), 'html.parser')
            div = soup.find('div', 'list-group').find_all('div', 'list')
            try:
                for item in div:
                    title = item.find('div', 'post-des').find('a').text.strip()
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
                    urlCheck = item.find('div', 'post-des').find('a')['href'].split('.com/')[1]
                    urlEncode = unquote(urlCheck)
                    url = 'https://tabomtorrent2.com/'+urlEncode

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'tabomtorrent',
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

    print("tabomtorrent 크롤링 시작")
    site = ['movie','broadcast/drama','broadcast/ent','broadcast/dacu','broadcast/animaion']
    for s in site:
        startCrawling(s)
    print("tabomtorrent 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
