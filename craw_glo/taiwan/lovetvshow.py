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
    link = 'https://lovetvshow.cc/filter/'+site
    link2 = '-.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'myui-vodlist').find_all('li')

        try:
            for item in li:
                url = 'https://lovetvshow.cc'+item.find('a')['href']
                titleSub = item.find('a')['title']
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
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
                div = soup.find_all('div', id=re.compile("playlist+"))

                for item in div:
                    li = item.find_all('li')

                    for item in li:
                        if item.find('a'):
                            host_url = 'https://lovetvshow.cc'+item.find('a')['href']
                            title = titleSub+'_'+item.find('a').text.strip()
                            if title.find('SP') != -1:
                                continue
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'lovetvshow',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'taiwan',
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

    print("lovetvshow 크롤링 시작")
    site = ['krdr---', 'variety-韓國--']
    for s in site:
        startCrawling(s)
    print("lovetvshow 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
