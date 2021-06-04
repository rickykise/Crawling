import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 2:
                break
                
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'm.filemong.com',
                'Referer': 'https://m.filemong.com/contents/best.html?bs='+site,
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
            }

            link = 'https://m.filemong.com/contents/best.html?bs='+site
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find('ul', 'content-list').find_all('li')

            try:
                for item in li:
                    title = item.find('strong', 'ctit').text.strip()
                    title_null = titleNull(title)
                    cnt_num = item.find('a', 'content-item')['onclick'].split("page_open('")[1].split("')")[0].strip()
                    url = 'https://m.filemong.com/contents/view.html?idx='+cnt_num

                    # 키워드 체크
                    getKey = getKeywordNet()
                    keyCheck = checkTitleNet(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    checkPrice = str(keyCheck['p'])

                    post_one  = s.get(url, headers=headers, allow_redirects=False)
                    soup = bs(post_one.text, 'html.parser')

                    cnt_price = soup.find('dl', 'dsc-view').text.split('가격')[1].replace(",","").replace('P', '').strip()
                    cnt_fname = soup.find('tr', 'trShow_non').find('td').text.strip()
                    cnt_writer = soup.find('h1', 'hd-prof').text.strip()
                    cnt_vol = ''
                    cnt_chk = 0
                    if checkPrice == cnt_price:
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filemong',
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

    print("m_filemong 크롤링 시작")
    site = ['DRA','BCT']
    for s in site:
        startCrawling(s)
    print("m_filemong 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
