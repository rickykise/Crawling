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

LOGIN_INFO = {
    'email_tail': 'naver.com',
    'id': 'e+I7njPr2yDYt1M1md31KQGYb5WGN169CRi4bNG4XpI=||mBF1k8kb4aaf9fe0f140514e1c3c581963eb71f',
    'id_nm': 'enjoy15',
    'login_backurl': '',
    'mode': 'login_exec',
    'pw': 'vJ35PvaiVfb1085ch4NaAA==||GRCiU6I08c1968a9f3698f07ff584287cca9763',
    'saved_pw': 'Y',
    'ssl_mobile_flg': '1',
    'wmode': 'noheader'
}

headers = {
    'Origin': 'http://m.smartfile.co.kr',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cookie': '_ga=GA1.3.154834487.1575943257; PHPSESSID=mck3dvocood3e86850god9ijq7; _gid=GA1.3.837046379.1577323453; _gat=1; CONNECT_NT=Y; SAVED_ID2=enjoy11; SAVED_DM2=naver.com; SAVED_ID=enjoy11%40naver.com; SAVED_PW=gAY1ja4WlahXA0iQjYJ4iA%3D%3D%7C%7CsERuK8D52e24b4a01d9d808fe58bbaf73013c08; mecrossCheck17822093=Y; AUTOLOGINSTOP=1'
}

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        login_req = s.get('http://m.smartfile.co.kr/member/login.html', data=LOGIN_INFO, headers=headers)
        while check:
            i = i+1
            if i == 5:
                break
            link = 'http://m.smartfile.co.kr/ajax/ajax.php'
            Page = {
                'mode': 'contents_list_sphinx',
                'page': i,
                'slist': '20',
                'cate1': site
            }
            post_one  = s.post(link, headers=headers, data=Page)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)

            try:
                for item in text:
                    adult = text.split('<adult_chk>')[a].split('</adult_chk>')[0]
                    if adult == 'Y':
                        continue
                    cnt_num = text.split('<idx>')[a].split('</idx>')[0]
                    url = 'http://m.smartfile.co.kr/board/board_view.html?idx='+cnt_num
                    a = a+1
                    if a == 21:
                        a = 1
                        break
                    url2 = 'http://m.smartfile.co.kr/ajax/ajax.left.php'
                    Page = {
                        'idx': cnt_num
                    }
                    post_two  = s.post(url2, headers=headers, data=Page)
                    content = post_two.content
                    soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                    cnt_chk = 0

                    title = soup.find('div', 'movie_info').find('h3').text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    cnt_price = soup.find('div', 'info').find_all('p')[1].find('span').text.split("P")[0].replace(",","").strip()
                    cnt_writer = soup.find('div', 'info').find('p').text.split(':')[1].split('/')[0].strip()
                    if soup.find('div', 'info').find('p').find('font'):
                        cnt_vol = soup.find('div', 'info').find('p').text.split(':')[2].split('[')[0].strip()
                        cnt_chk = 1
                    else:
                        cnt_vol = soup.find('div', 'info').find('p').text.split(':')[2].strip()
                    cnt_fname = soup.find('ul', 'lst').find('li').find('p').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'smartfile',
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
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_smartfile 크롤링 시작")
    site = ['2','3','4','5']
    for s in site:
        startCrawling(s)
    print("m_smartfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
