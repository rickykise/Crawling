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

def startCrawling():
    i = 0;check = True
    link = 'https://vuviphim.com/phim-han-quoc/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', 'item post')

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('a').find('img')['alt']
                title_check = titleNull(titleSub)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                eng_title = soup.find('span', 'tagline').text.strip()
                if eng_title.find('(') != -1:
                    eng_title = eng_title.split('(')[0]
                url2 = soup.find('div', 'content').find('a', 'nutplay')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'listserver').find_all('li')

                for item in li:
                    cnt_url = item.find('a')['href']
                    cnt_num = item.find('a')['data-episode-id']
                    titleNum = item.find('a').text.strip()
                    title = titleSub+eng_title+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_num' : cnt_num,
                        'cnt_osp' : 'vuviphim',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'cnt_url' : cnt_url,
                        'cnt_host' : '',
                        'cnt_writer' : '',
                        'cnt_nat': 'vietnam'
                    }
                    # print(data)

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("vuviphim 크롤링 시작")
    startCrawling()
    print("vuviphim 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
