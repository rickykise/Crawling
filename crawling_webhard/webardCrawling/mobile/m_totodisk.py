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
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

def startCrawling(site):
    i = 0;check = True;category2 = ''
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = "http://m.totodisk.com/Home/AjaxSrchContentsByText.asp"
            if site == '200':
                category2 = '201'
            else:
                category2 = '301'
            Data = {
                'category1': site,
                'category2': category2,
                'currentPage': i,
                'keyword': ''
            }
            post_one  = s.post(link, data=Data, headers=headers)
            c = post_one.content
            soup = bs(c.decode('utf8','replace'), 'html.parser')
            li = soup.find('ul', id='contentsList').find_all('li')

            # try:
            for item in li:
                title = item.find('h2').text.strip()
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeywordNet()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue
                cnt_num = item.find('a')['href'].split("WatchContent('")[1].split("')")[0]
                url = 'http://m.totodisk.com/Content/Index.asp?folderId='+cnt_num

                post_two = s.get(url, headers=headers)
                c = post_two.content
                soup = bs(c.decode('utf8','replace'), 'html.parser')
                cnt_chk = 0
                div = soup.find('div', id='tabMenuList')
                cnt_writer = soup.find('div', 'cate').text.split(":")[1].strip()

                cnt_price = div.find('span', 'cash').text.split("원")[0].replace(',','').strip()
                cnt_vol = div.find('span', 'data').text.strip()
                if cnt_vol.find('원본') != -1:
                    cnt_vol = cnt_vol.split("[")[0].strip()
                cnt_fname = div.find('span', 'listT').text.strip()
                jehu = div.find('span', 'cash').text.strip()
                if jehu.find('제휴') != -1:
                    cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'totodisk',
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

    print("m_totodisk 크롤링 시작")
    site = ['200','300']
    for s in site:
        startCrawling(s)
    print("m_totodisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
