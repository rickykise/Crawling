import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Referer': 'http://www.dodofile.com/board',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'opVal=1%7C1%7C0%7C1%7C0%7C0%7C0%7C0; PHPSESSID=49et3iqga9tssikfn4ggofme20; ACEFCID=UID-5C511801779491C04E7D2707; ACEUCI=1; _bbsInfoTab=Y; mi^c=2019-01-30%2012%3A20%3A37; mi^vi=JI0XN1IDQ1z7JKIQM2IEX125'
    }

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.dodofile.com/board.php?mSec='+site+'&sSec=&mAdult=0&searchVal=&search_ban=&nPage='+str(i)
            post_one  = s.get(link)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            table = soup.find('div', 'main_layer').find_all('table', 'm_list')
            try:
                for item in table:
                    cnt_num = item['onclick'].split("idx=")[1].split("&")[0]
                    url = 'http://m.dodofile.com' + item['onclick'].split("'")[1].split("'")[0]

                    post_two  = s.get(url, headers=headers)
                    content = post_two.content
                    soup = bs(content.decode('euc-kr','replace'), 'html.parser')

                    title = soup.find('div', 'view_tit').find('h2').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = dodoGetKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = soup.find('span', 'best_sz').find('span', 'b_price').text.strip()
                    cnt_vol = soup.find('td', 'view_nik').text.strip()
                    url2 = 'http://www.dodofile.com/board.php?act=bbs_info&idx='+cnt_num
                    post_writer  = s.get(url2)
                    c = post_writer.content
                    soup2 = bs(c.decode('euc-kr','replace'), 'html.parser')
                    cnt_writer = soup2.find_all('td', 'point_vol')[1].text.strip()
                    cnt_fname = soup2.find('li', 'file_f').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'dodofile',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': 0
                    }
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_dodofile 크롤링 시작")
    site = ['','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_dodofile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
