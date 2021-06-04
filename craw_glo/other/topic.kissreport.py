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
    link = 'https://topic.kissreport.com/category/'+site+'/page/'
    while check:
        i = i+1
        if i == 40:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', 'latestPost')
        if len(article) < 1:
            check = False;break

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                if titleSub.find('Best Korean Dramas') != -1:
                    continue
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
                div = soup.find('div', 'pagination').find_all('a')
                if soup.find('a', 'ext-link'):
                    host_url = soup.find('a', 'ext-link')['href']
                    title = titleSub+'_1'
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'topic.kissreport',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'other',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)

                for item in div:
                    if item.find('i'):
                        continue

                    ext_url = item['href']
                    title = titleSub+'_'+item.find('span').text.strip()
                    title_null = titleNull(title)

                    r = requests.get(ext_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    if soup.find('a', 'ext-link'):
                        host_url = soup.find('a', 'ext-link')['href']

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'topic.kissreport',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'other',
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

    print("topic.kissreport 크롤링 시작")
    site = ['korean-drama','kshows']
    for s in site:
        startCrawling(s)
    print("topic.kissreport 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")