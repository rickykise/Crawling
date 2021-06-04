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

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Cookie': 'mlsAdult=0',
                'Host': 'm.dodofile.com',
                'Referer': 'http://m.dodofile.com/board.php?mAdult=0&mSec='+site+'&appAndroid=',
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
            }
            data = {
                'mAdult': '0',
                'mSec': site,
                'nPage': str(i),
                'search_ban': '',
                'searchVal': '',
                'sSec': ''
            }
            link = 'http://m.dodofile.com/board.php?mSec='+site+'&sSec=&mAdult=0&searchVal=&search_ban=&nPage='+str(i)
            post_one  = s.get(link, headers=headers, data=data)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            table = soup.find('div', 'main_layer').find_all('table', 'm_list')

            try:
                for item in table:
                    cnt_num = item['onclick'].split("idx=")[1].split("&")[0]
                    url = 'http://m.dodofile.com' + item['onclick'].split("'")[1].split("'")[0]

                    headers2 = {
                        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Connection': 'Keep-Alive',
                        'Cookie': 'mlsAdult=0',
                        'Host': 'm.dodofile.com',
                        'Referer': url,
                        'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
                    }

                    data2 = {
                        'act': 'view',
                        'idx': cnt_num,
                        'mSec': site,
                        'nLimit': 20,
                        'nPage': str(i),
                        'tSec': site
                    }

                    cnt_chk = 0
                    post_two  = s.get(url, headers=headers2, data=data2)
                    content = post_two.content
                    soup = bs(content.decode('euc-kr','replace'), 'html.parser')

                    title = soup.find('div', 'view_tit').find('h2').text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    cnt_price = soup.find('span', 'b_price').text.replace(',', '').split('P')[0].strip()
                    cnt_vol = soup.find('div', 'view_info').find_all('li')[2].find('p').text.strip()

                    cnt_writer = soup.find('div', 'view_catename').find('span').text.strip()
                    cnt_fname = str(soup).split('realname:"')[1].split('",')[0].strip()
                    if soup.find('div', 'view_info').find_all('li')[3].find('img'):
                        jehu = soup.find('div', 'view_info').find_all('li')[3].find('img')['src']
                        if jehu.find('jehu.gif') != -1:
                            cnt_chk = 1

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
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print('==================================')

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_dodofile 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_dodofile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
