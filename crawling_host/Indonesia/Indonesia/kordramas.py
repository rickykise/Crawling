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
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    while check:
        i = i+1
        if i == 30:
            break
        if site == '1':
            link = 'https://kordramas.com/category/drama-korea/page/'
            r = requests.get(link+str(i))
        else:
            link = 'https://kordramas.com/category/variety-show/page/'
            r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', id=re.compile("post-+"))

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div', 'entry-content').find_all('a')

                for item in sub:
                    check_url = item['href']
                    if check_url.find('720px.net') != -1:
                        host_url = check_url

                        r = requests.get(host_url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")

                        title = soup.find('table', 'table-striped').find('tbody').find_all('td')[1].text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'kordramas',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'indonesia',
                            'cnt_writer': ''
                        }
                        print(data)
                        print("=================================")

                    # dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kordramas 크롤링 시작")
    site = ['1','2']
    for s in site:
        startCrawling(s)
    print("kordramas 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
