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
    i = 0; a = 1;check = True
    with requests.Session() as s:
        link = "https://www.filecity.co.kr/module/contents_list.php"
        while check:
            # # 페이지 0부터 시작
            if i == 3:
                break
            i = i+1
            Page = {
                'down_chk': '0',
                'limit': '20',
                'no_overlap': '0',
                'not_adult': '1',
                'pn': i,
                'poster_chk': '0',
                's_value': '',
                'sale': '0',
                'sale2': '0',
                'tab': site,
                'tab2': '',
                'view': 'list',
                'year': '2020'
            }
            headers = {
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
            post_one  = s.post(link, data=Page, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)

            try:
                for item in text:
                    if a == 21:
                        a = 1
                        break
                    cnt_num = text.split('"idx":"')[a].split('","')[0]
                    # https://m.filecity.kr/contents/#tab=BD_UC&view=list&idx=23341737
                    cnt_num = '23341737'
                    adult = text.split('"adult_chk":"')[a].split('","')[0]
                    cnt_vol = text.split('"size":"')[a].split('","')[0]
                    url = "https://filecity.kr/html/view2.html"
                    url2 = "https://filecity.kr/html/view2.html?idx="+cnt_num
                    a = a+1
                    if adult == "1":
                        continue

                    idx = {
                        'idx': cnt_num,
                        'link': 'list',
                        'type': 'layer'
                    }

                    post_two  = s.post(url, data=idx)
                    soup = bs(post_two.text, 'html.parser')

                    cnt_chk = 0

                    title = soup.find('div', 'cont_title').text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    # getKey = getKeywordNet()
                    # keyCheck = checkTitleNet(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('filecity',title,title_null,url2)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('filecity',title,title_null,url2)
                    #     continue

                    cnt_price = soup.find('li', 'point02').find('span', 'num').text.strip().replace(",","")
                    cnt_writer = soup.find('li', 'nickname').text.strip()
                    cnt_fname = soup.find('div', 'info_body').find('li', 'info01')['title']

                    div = soup.find('div', 'cont_info clearfix')
                    if div.find('ul', 'clearfix icon_alliance'):
                        cnt_chk =1
                    if div.find('ul', 'clearfix icon_sale'):
                        cnt_chk =1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filecity',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url2,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    print(data)
                    print('======================================')

                    # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("filecity 크롤링 시작")
    site = ['BD_MV','BD_DM','BD_UC','BD_AN']
    for s in site:
        startCrawling(s)
    print("filecity 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
