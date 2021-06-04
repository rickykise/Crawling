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
    'Referer': 'http://sedisk.com/storage.php',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'ACEFCID=UID-5C22F965D514161EE9381054; _ga=GA1.2.1287727625.1545974475; ptn=ksc0110; ACEUCI=1; _gid=GA1.2.1421021257.1547447786; evLayer=N; _gat=1'
}

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.sedisk.com/storage.php?act=swipe_more&nPage='+str(i)+'&mSec='+site+'&sSec=&searchKey=&searchVal=&mAdult=0&startYN=N&fixView=&fix_all_view='
            print(link)
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            a = soup.find_all('a', 'viewLink')

            # try:
            for item in a:
                cnt_num = item['href'].split('idx=')[1].split('&')[0]
                url = 'http://m.sedisk.com'+item['href'].strip()
                url2 = 'http://sedisk.com/storage.php?act=view&idx=' + cnt_num

                post_two  = s.post(url2, headers=headers)
                soup = bs(post_two.text, 'html.parser')
                text = str(soup)
                if text.find('해당 컨텐츠는 로그인') != -1:
                    continue
                cnt_chk = 0

                title = soup.find('title').text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                cnt_price = soup.find('span', 'b_price').text.strip().split("P")[0].replace(",","")
                cnt_vol = soup.find('span', 'f_tahoma11').text.strip().replace("/ ","")
                cnt_writer = soup.find('span', 'name_s').text.strip()
                cnt_fname = soup.find('td', 'td_tit').text.strip()
                if soup.find_all('td', 'point_vol')[2].find('img'):
                    img = soup.find_all('td', 'point_vol')[2].find('img')['src']
                    if img.find('ico_jehu2') != -1:
                        cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'sedisk',
                    'Cnt_title': title,
                    'Cnt_title_null': title_null,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
                    'Cnt_chk': cnt_chk
                }
                print(data)
                print("=================================")

                    # dbResult = insertALL(data)
            # except:
            #     continue

if __name__=='__main__':
    start_time = time.time()

    print("m_sedisk 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_sedisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
