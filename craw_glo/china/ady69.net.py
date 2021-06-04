import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'http://www.ady69.net/list/?5-{}.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        r.encoding = r.apparent_encoding
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        list_a = soup.find('div','clist').find_all('a', 'pic')
        try:
            for item in list_a:
                url = item['href']
                titleSub = item['title'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                r.encoding = r.apparent_encoding
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div',id='playlist').find_all('a',href=lambda x: x and "/video/" in x)

                for item in sub:
                    host_url = 'http://www.ady69.net'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'ady69.net',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("ady69.net 크롤링 시작")
    startCrawling()
    print("ady69.net 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
