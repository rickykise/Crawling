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
path = inspect.getfile(inspect.currentframe())
x = path.split('\\')
x.reverse()
osp_id = x[0].split('.py')[0].strip()

def startCrawling(site):
    i = 0;check = True;cnt_osp = 'goguma27'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        link = group_url+'index.php/vod/show/id/'+site+'/page/'
        link2 = '.html'
        cnt_osp = group_id
    else:
        link = 'https://goguma27.tv/index.php/vod/show/id/'+site+'/page/'
        link2 = '.html'
    while check:
        i = i+1
        if i == 50:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'img-list').find_all('li', 'yk-pack')

        try:
            for item in li:
                url = 'https://goguma27.tv'+item.find('a')['href']
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
                sub = soup.find('div', 'num-tab-main').find_all('a')

                for item in sub:
                    host_url = 'https://goguma27.tv'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : cnt_osp,
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
            continue

if __name__=='__main__':
    start_time = time.time()

    print("goguma27 크롤링 시작")
    site = ['2', '3']
    for s in site:
        startCrawling(s)
    print("goguma27 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
