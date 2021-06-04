import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(site):
    i = 0;check = True
    link = 'http://www.5rs-wc16.com/webtoon?week='+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'webtoon_list').find_all('li')

        try:
            for item in li:
                url = 'http://www.5rs-wc16.com'+item.find('a')['href']
                title = item.find('a')['title']
                title_check = titleNull(title)

                a = 0;pageCheck = True
                page_url = url+'?&page='
                while pageCheck:
                    a = a+1
                    if a == 10:
                        break
                    r = requests.get(page_url+str(a))
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    tr = soup.find('table', 'table left_area').find_all('tr')
                    if len(tr) < 1:
                        pageCheck=False;break

                    for item in tr:
                        craw_url = item.find_all('td')[1].find('a')['href']
                        craw_url = urllib.parse.unquote(craw_url)
                        if craw_url.find('?&page=') != -1:
                            craw_url = craw_url.split('?&page=')[0]
                        title_numCh = titleNull(item.find_all('td')[1].find('a').text.strip())
                        title_num = title_numCh.replace(title_check, '').split('화')[0].strip()

                        data = {
                            'craw_osp_id': '5rs-wc16',
                            'craw_domain': 'com',
                            'craw_title': title,
                            'craw_site_url' : url,
                            'craw_url': craw_url,
                            'craw_title_num': title_num
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("5rs-wc16 크롤링 시작")
    site = ['latest','1','2','3','4','5','6','0','10']
    for s in site:
        startCrawling(s)
    print("5rs-wc16 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
