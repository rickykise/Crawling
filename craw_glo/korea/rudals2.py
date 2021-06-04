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
    link = 'https://www.rudals2.net/'+site+'/'
    link2 = '//LOADMORE'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'col-4')

        try:
            for item in div:
                url = 'https://www.rudals2.net'+item.find('a')['href']
                titleSub = item.find('div').text.strip()
                title_null = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find('div', id='container').find_all('div', 'col-12')

                for item in div:
                    sub = item.find_all('a')
                    title = titleSub+'_'+item.find('span').text.strip()
                    title_null = titleNull(title)
                    for item in sub:
                        host_url = item['href']
                        if host_url.find('live/linker') == -1:
                            continue

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'rudals2',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            break

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("rudals2 크롤링 시작")
    site = ['드라마', '예능']
    for s in site:
        startCrawling(s)
    print("rudals2 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
