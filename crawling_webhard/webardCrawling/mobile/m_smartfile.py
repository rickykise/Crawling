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
    'id': 'dlsrlwkr@naver.com',
    'id_nm': 'dlsrlwkr',
    'login_backurl': '',
    'mode': 'login_exec',
    'pw': 'dlsrl11!',
    'saved_pw': 'Y',
    'ssl_mobile_flg': '1',
    'wmode': 'noheader'
}

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        login_headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'm.smartfile.co.kr',
            'Referer': 'http://m.smartfile.co.kr/realrank/?rnk_cate1='+site,
            'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
        }
        login_req = s.post('http://m.smartfile.co.kr/member/login.html', data=LOGIN_INFO, headers=login_headers)
        content = login_req.content
        soup = bs(content.decode('euc-kr','replace'), 'html.parser')
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
            headers = {
                'Origin': 'http://m.smartfile.co.kr',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            }
            post_one  = s.post(link, headers=headers, data=Page)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)

            # try:
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

                headers2 = {
                    'Accept': 'text/html, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ko-KR',
                    'Cache-Control': 'no-cache',
                    'Connection': 'Keep-Alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Host': 'm.smartfile.co.kr',
                    'Referer': 'http://m.smartfile.co.kr/?cate1='+site,
                    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
                    'X-Requested-With': 'XMLHttpRequest'
                }

                post_two  = s.post(url2, headers=headers2, data=Page)
                content = post_two.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                cnt_chk = 0

                title = soup.find('div', 'movie_info').find('h3').text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                # getKey = getKeyword()
                # keyCheck = checkTitle(title_null, getKey)
                # if keyCheck['m'] == None:
                #     continue
                # keyCheck2 = checkTitle2(title_null, getKey)
                # if keyCheck2['m'] == None:
                #     continue

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
                print(data)
                print("=================================")

                    # dbResult = insertALL(data)
            # except:
            #     continue

    time.sleep(90)

if __name__=='__main__':
    start_time = time.time()

    print("m_smartfile 크롤링 시작")
    site = ['3','4','5','2']
    for s in site:
        startCrawling(s)
    print("m_smartfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
