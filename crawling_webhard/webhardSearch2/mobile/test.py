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
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Content-Length': '63',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'm.filecity.co.kr',
    'Referer': 'https://m.filecity.co.kr/contents/',
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
    'X-Requested-With': 'XMLHttpRequest'
    }

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            if i == 4:
                break
            i = i+1
            Page = {
                'etc': '',
                'idx': '',
                'pn': i,
                's_value': '',
                'tab': site,
                'tab2': '',
                'type': 'mobile',
                'view': 'list'
            }
            link = 'https://m.filecity.co.kr/module/contents_list.php'
            post_one  = s.post(link, data=Page, headers=headers)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)

            try:
                for item in text:
                    cnt_num = text.split('"idx":"')[a].split('","')[0]
                    url = 'https://m.filecity.kr/contents/#tab='+site+'&view=list&idx='+cnt_num
                    cnt_vol = text.split('"size":"')[a].split('","')[0]
                    url2 = "https://filecity.kr/html/view2.html"
                    a = a+1
                    if a == 21:
                        a = 1
                        break
                    print(cnt_num)
                    idx = {
                        'idx': cnt_num,
                        'link': 'list',
                        'type': 'layer'
                    }
                    headers2 = {
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Cache-Control': 'no-cache',
                        'Connection': 'Keep-Alive',
                        'Content-Length': '117',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'www.filecity.co.kr',
                        'Referer': 'https://www.filecity.co.kr/contents/',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    post_two  = s.post(url2, data=idx, headers=headers2)
                    soup = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('div', 'cont_title').text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    # getKey = getKeywordNet()
                    # keyCheck = checkTitleNet(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     continue

                    # checkPrice = str(keyCheck['p'])
                    cnt_price = soup.find('li', 'point02').find('span', 'num').text.strip().replace(",","")
                    cnt_writer = soup.find('li', 'nickname').text.strip()
                    cnt_fname = soup.find('div', 'info_body').find('li', 'info01')['title']

                    if soup.find('ul', 'clearfix icon_alliance') or soup.find('ul', 'clearfix icon_alliance '):
                        cnt_chk = 1
                    if soup.find('ul', 'clearfix icon_sale'):
                        cnt_chk = 1
                    if cnt_chk == 0:
                        if checkPrice == cnt_price:
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filecity',
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

                    # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_filecity 크롤링 시작")
    site = ['BD_MV','BD_DM','BD_UC','BD_AN']
    for s in site:
        startCrawling(s)
    print("m_filecity 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
