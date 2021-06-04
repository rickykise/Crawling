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
            Page = {
                'mode': 'contents_list_sphinx',
                'page': i,
                'cate1': site,
                'cate2': '',
                'keyword': '',
                'slist': '20'
            }
            link = 'http://m.applefile.com/ajax/ajax.php'
            post_one  = s.post(link, data=Page)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)
            try:
                for item in text:
                    cnt_num = text.split("<idx>")[a].split("</idx>")[0]
                    url = 'http://m.applefile.com/board/board_view.html?idx='+cnt_num
                    a = a+1
                    if a == 21:
                        a = 1
                        break

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    if soup.find('title') == None:
                        continue
                    div = soup.find('div', 'fileinfo_textarea')
                    cnt_chk = 0

                    title = soup.find('title').text.strip().split("모바일 - ")[1]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    # checkPrice = str(keyCheck['p'])
                    price = div.find_all('li', 'info_a')[1].text.strip()
                    if price.find('제휴') != -1:
                        cnt_chk = 1
                    cnt_price = price.split('P')[0].replace(",","")
                    # if checkPrice == cnt_price:
                    #     cnt_chk = 1
                    cnt_writer = div.find_all('li', 'info_a')[2].text.strip()
                    divLen = soup.find_all('div', id='fileinfo_list')
                    if len(divLen) == 2:
                        cnt_vol = soup.find_all('div', id='fileinfo_list')[1].find('label').text.strip().split('(')[1].split(':')[0].replace(" ","")
                    else:
                        cnt_vol = soup.find('div', id='fileinfo_list').find('label').text.strip().split('(')[1].split(':')[0].replace(" ","")
                    cnt_fname = soup.find('li', 'info_title').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'applefile',
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

    print("m_applefile 크롤링 시작")
    site = ['','2','3','4','5']
    for s in site:
        startCrawling(s)
    print("m_applefile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
