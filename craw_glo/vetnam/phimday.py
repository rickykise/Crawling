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

def startCrawling(link):
    i = 0;check = True;a = 1;titeCH = '';titleTF= True
    link = 'https://www.phimday.com/search/label/Hàn%20Quốc?'+link
    while check:
        check = True
        i = i+1
        if i == 30:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'phimitem')

        try:
            for item in div:
                url = item.find('a')['onclick'].split('replace("')[1].split('")')[0]
                titleSub = item.find('a')['title'].strip()
                if titleSub.find('(20') != -1:
                    titleSub = titleSub.split('(20')[0].strip()
                title_check = titleNull(titleSub)
                if title_check == titeCH:
                    titleTF = False
                    a = 1
                    check = False;break
                if titleTF == True:
                    titeCH = title_check
                    titleTF = False

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
                text = str(soup)
                linkText = text.split('[link]')[1].split('[/link]')[0]

                try:
                    for item in text:
                        host_url = linkText.split(str(a)+"*")[1].split("]")[0]
                        title = titleSub+'_'+str(a)
                        title_null = titleNull(title)
                        a = a+1

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'phimday',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'vietnam',
                            'cnt_writer': '',
                            'origin_url': '',
                            'origin_osp': ''
                        }
                        print(data)
                        print("=================================")

                        # dbResult = insertALL(data)
                except:
                    a = 1
                    check=False;break
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phimday 크롤링 시작")
    site = [
        '&max-results=30',
        'updated-max=2019-10-21T03%3A07%3A00-07%3A00&max-results=30#PageNo=2',
        'updated-max=2019-09-29T11%3A09%3A00-07%3A00&max-results=30#PageNo=3',
        'updated-max=2019-09-22T10%3A31%3A00-07%3A00&max-results=30#PageNo=4',
        'updated-max=2019-09-17T07%3A42%3A00-07%3A00&max-results=30#PageNo=5',
        'updated-max=2019-08-30T12%3A47%3A00-07%3A00&max-results=30#PageNo=6'
    ]
    for s in site:
        startCrawling(s)
    print("phimday 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
