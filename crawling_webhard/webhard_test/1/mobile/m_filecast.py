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
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://m.filecast.co.kr',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            Page = {
                'category': 'false',
                'first_load': 'false',
                'is_mobile': '1',
                'limit': '20',
                'main': site,
                'notice_unload': '1',
                'page': i,
                'page_load': '0',
                'search': '',
                'sort': 'is_non_adult',
                'sort_order': 'is_non_adult',
                'sub': '0',
                'total_count': '0',
                'type': 'cate'
            }
            link = 'http://m.filecast.co.kr/www/contents_m/mobile_list/'
            post_one  = s.post(link, data=Page, headers=headers)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)
            try:
                for item in text:
                    cnt_num = text.split('idx":"')[a].split('",')[0]
                    url = 'http://m.filecast.co.kr/mobile/#action=view&data='+cnt_num
                    url2 = 'http://filecast.co.kr/www/contents/view/'+cnt_num
                    a = a+1
                    if a == 41:
                        a = 1
                        break
                    if cnt_num == '0':
                        continue

                    post_two  = s.get(url2)
                    content = post_two.content
                    soup = bs(content.decode('utf-8','replace'), 'html.parser')

                    deleteText = str(soup)
                    if deleteText.find('삭제되었거나 제재된') != -1:
                        continue
                    cnt_chk = 0

                    title = soup.find('span', 'txt').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = soup.find('span', 'txt_blue txt_block').find('b').text.replace(",","").strip()
                    cnt_writer = soup.find('a', 'btn_memo')['onclick'].split("('")[1].split("')")[0]
                    cnt_vol = soup.find('li', 'l4').find('span', 'txt_block').text.replace(" ","").strip()
                    cnt_fname = soup.find('span', 'file_name').text.strip()
                    ico = soup.find('span', 'ico_partner')['class']
                    if ico[1] == 'on':
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filecast',
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

    print("m_filecast 크롤링 시작")
    site = ['1','2','3']
    for s in site:
        startCrawling(s)
    print("m_filecast 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
