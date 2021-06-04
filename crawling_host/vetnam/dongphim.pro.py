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
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.py')[0]
getDel = ospCheck(osp_id)

def startCrawling(url, keyItem):
    url = url;cnt_id = keyItem[0];cnt_osp = keyItem[1];cnt_title = keyItem[2];cnt_nat = keyItem[3];cnt_keyword = '';a = 1

    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('a', 'movie-eps-item')
        mid = url.split('_')[1].split('.')[0]
        current = soup.find('a', 'movie-eps-item')['title'].split('Tập')[1].strip()
        url2 = 'http://dongphim.pro/ajax_loadep.php?drt=down&mid='+mid+'&idx=10&current='+current

        for item in div:
            host_url = item['href']
            if host_url == '#':
                continue
            title = cnt_title + '_' + item.text.split('Tập')[1].strip()
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'dongphim.pro',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'vietnam',
                'cnt_writer': ''
            }
            # print(data)
            # print("=================================")

            dbResult = insertALL(data)

        r = requests.get(url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup).replace('\\', '')
        splitHref = "href='"

        try:
            for item in text:
                host_url = text.split(splitHref+'"')[a].split('"')[0]
                title = cnt_title + '_' + text.split('<a ')[a].split('"')[0]
                title_null = titleNull(title)

                a = a+1

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'dongphim.pro',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'vietnam',
                    'cnt_writer': ''
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except:
            pass
    except:
        pass

    dbInResult = dbUpdate(url)

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getUrl = gethost(osp_id)

    print("dongphim.pro 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("dongphim.pro 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
