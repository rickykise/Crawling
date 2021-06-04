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
    i = 0;check = True;a = 1
    link = 'https://fofmyanmar.com/ratings/page/'
    link2 = '/?get=tv'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', id=re.compile("post-+"))

        try:
            for item in article:
                imgUrl = item.find('img')['src']
                url = item.find('a')['href']
                titleSub = item.find('img')['alt']
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
                sub = soup.find_all('a', 'su-button')


                for item in sub:
                    check_url = item['href']
                    if check_url.find('mm1ink') != -1:
                        host_url = 'https://betvigososyal.com/go/'+item['href'].split('.net/')[1]
                    else:
                        host_url = check_url
                    title = titleSub + '_' + str(a)
                    title_null = titleNull(title)
                    a = a+1

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'fofmyanmar',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'myanmar',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
                a = 1
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("fofmyanmar 크롤링 시작")
    startCrawling()
    print("fofmyanmar 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
