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
    'Origin': 'http://m.filemaru.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            Data = {
                'adtChk': '1'
            }
            adult = s.post('http://m.filemaru.com/proInclude/ajax/adtCtl.php', data=Data)
            i = i+1
            if i == 4:
                break
            link = "http://m.filemaru.com/proInclude/scroll/infScroll.php?doc=submenu_cate&mSec="+site+"&sSec=&p="+str(i)+"&sort=&searchVal=&searchType=&searchChk="
            post_one  = s.post(link)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find_all('li', 'list_box ctrView')
            try:
                for item in li:
                    cnt_num = item.find('a')['idx']
                    span = item.find('div', 'b_info_left').find('span').text.strip()
                    cnt_vol = item.find('div', 'b_info_left').text.split(span)[0].strip()
                    if item.find('div', 'b_info_right').find('span'):
                        price = item.find('div', 'b_info_right').find('span').text.strip()
                        cnt_price = item.find('div', 'b_info_right').text.split(price)[1].strip().replace(",","").split('P')[0]
                    else:
                        cnt_price = item.find('div', 'b_info_right').text.strip().replace(",","").split('P')[0]
                    url = 'http://m.filemaru.com/proInclude/ajax/view.php'
                    url2 = "http://m.filemaru.com/proInclude/ajax/view.php"+cnt_num
                    Page = {
                        'idx': cnt_num
                    }
                    post_one  = s.post(url, data=Page)
                    soup = bs(post_one.text, 'html.parser')
                    text = str(soup)
                    cnt_chk = 0

                    title = text.split('fileTitle" : "')[1].split('"')[0]
                    title_null = titleNull(title)
                     # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_writer = text.split('fileRegNick" : "')[1].split('"')[0]
                    cnt_fname = text.split('fileName" : "')[1].split('"')[0]
                    if text.find('files') != -1:
                        cnt_fname = text.split('fileName" : "')[2].split('"')[0]

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filemaru',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url2,
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

    print("m_filemaru 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_filemaru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
