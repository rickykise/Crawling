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
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.yesfile.com/ajax/ajax.php'
            Page = {
                'mode': 'contents_list_sphinx',
                'page': i,
                'slist': '20',
                'cate1': site
            }
            post_one  = s.post(link, data=Page)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)

            try:
                for item in text:
                    adult = text.split('<adult_chk>')[a].split('</adult_chk>')[0]
                    if adult == 'Y':
                        continue
                    cnt_num = text.split('<idx>')[a].split('</idx>')[0]
                    url = 'https://m.yesfile.com/board/board_view.html?idx='+cnt_num
                    a = a+1
                    if a == 21:
                        a = 1
                        break

                    post_two  = s.get(url)
                    content = post_two.content
                    soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                    cnt_chk = 0

                    title = soup.find('div', id='top_bnn_nav').find('p').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    if soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[1].find('span'):
                        cnt_price = soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[1].text.split('P')[0].replace(",","").strip()
                        cnt_chk = 1
                    else:
                        cnt_price = soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[1].text.split('P')[0].replace(",","").strip()
                    cnt_writer = soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[2].text.strip()
                    cnt_vol = soup.find('div', 'list_title').text.split('(')[1].split(':')[0].strip()
                    cnt_fname = soup.find('li', 'info_title').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'yesfile',
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

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_yesfile 크롤링 시작")
    site = ['','2','3','4','5']
    for s in site:
        startCrawling(s)
    print("m_yesfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
