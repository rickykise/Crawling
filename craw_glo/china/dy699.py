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
    link = 'http://dy699.com/index.php?m=vod-list-id-'+site
    link2 = '-order--by--class-0-year-0-letter--area-韩国-lang-.html'
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            r = requests.get(link+link2)
        else:
            r = requests.get(link+'-pg-'+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find_all('a', 'li-hv')

        try:
            for item in sub:
                url = 'http://dy699.com'+item['href']
                titleSub = item['title']
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
                div = soup.find_all('div', id=re.compile("stab_+"))

                for item in div:
                    host_url = 'http://dy699.com'+item.find('a')['href']
                    title = titleSub+'_'+item.find('a')['title']
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'dy699',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dy699 크롤링 시작")
    site = ['14','3']
    for s in site:
        startCrawling(s)
    print("dy699 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
