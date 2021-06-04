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

def startCrawling():
    i = 0; a = 1;check = True
    link = 'https://www.korecenneti.pw/jsn-dta-st/fposts/'
    link2 = '/fcreated'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)

        try:
            for item in text:
                titleSub = text.split('ftitle":"')[a].split('",')[0]
                title_check = titleNull(titleSub)
                url = 'https://www.korecenneti.pw/'+text.split('fhref":"')[a].split('",')[0]
                a = a+1

                if a == 41:
                    a = 1
                    chekc=False;break

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
                if soup.find('ul', 'kimbolumler'):
                    li = soup.find('ul', 'kimbolumler').find_all('li')

                    for item in li:
                        host_url = 'https://www.korecenneti.pw'+item.find('a')['href'].split('.')[1]+'.html'
                        title = item.find('a')['title'].strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'korecenneti',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'turkey',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("korecenneti 크롤링 시작")
    startCrawling()
    print("korecenneti 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
