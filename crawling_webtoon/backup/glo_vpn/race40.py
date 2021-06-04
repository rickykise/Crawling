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

    headers= {
        'Accept' : 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'ko-KR',
        'Cookie' : '__cfduid=d35513a2524c19e1280f577c1185d02451592787474; cf_clearance=000441b9bd485932da7d2b674ec64aa8a7632ff1-1592787474-0-a3d10e56-150; sc_is_visitor_unique=rx11476733.1592788708.CAC64635E4194F200E395973EFA05B41.1.1.1.1.1.1.1.1.1; cf_chl_1=9d4653c22a08ec0',
        'Host' : 'www.race40.xyz',
        'Referer' : 'https://www.race40.xyz/?__cf_chl_jschl_tk__=4410f98d9e6adbfb123e06e1ac072e291ad91fd3-1592787469-0-AZh2vDuXFqFGIf6Jlz4b_4Prx9c3rZn0VqQhFOfAAgIPHQDeW2QtOYkO74znwnjog70n9TFvrNe6Sx4pWEEtp0zpF2EAYHTpT9LGxqofdb7HbDlgJiaRUl39i6EJ4XwZ7vXwVXKZUjAmubuYrPUEI_slA0FvwrSHNXHQ3LlMQKrlYSjhvG7ZLuWwMIqIngFuPCqxM8Mv1pM2JmXRBd6t97U9a7-Fx6PbKjNjAM5hptlnx1cTMEXRfZ7PTzHH8Du9M0Yl0QnapVxvWmsNw9tjnZQ',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    link = 'https://www.race40.xyz/'+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'section-item-title')

        try:
            for item in div:
                url = item.find('a')['href']
                title = item.find('a').text.strip()
                title_check = titleNull(title)

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                tr = soup.find('table', 'web_list').find_all('tr')

                for item in tr:
                    craw_url = item.find('a')['href']
                    title_numCh = titleNull(item.find('td', 'content__title')['title'])
                    title_num = title_numCh.split(title_check)[1].split('화')[0].strip()

                    data = {
                        'craw_osp_id': 'race40',
                        'craw_domain': 'xyz',
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

    print("race40 크롤링 시작")
    site = ['','finish.php']
    for s in site:
        startCrawling(s)
    print("race40 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
