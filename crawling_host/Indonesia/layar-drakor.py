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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(url, keyItem):
    url = url;cnt_id = keyItem[0];cnt_osp = keyItem[1];cnt_title = keyItem[2];cnt_nat = keyItem[3];cnt_keyword = ''

    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'les-content').find_all('a')
        liLen = len(li)

        if liLen == 1:
            host_url = url
            title = soup.find('div', 'mvic-desc').find('h3').text.strip()
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'layar-drakor',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'indonesia',
                'cnt_writer': ''
            }
            # print(data)
            # print("=================================")

            dbResult = insertALL(data)
        else:
            for item in li:
                host_url = item['href']
                title = cnt_title+'_'+item.text.strip()
                title_null = titleNull(title)

                # r = requests.get(host_url)
                # c = r.content
                # soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                # origin_url = soup.find('div', 'movieplay').find('iframe')['data-lazy-src']
                # if origin_url.find('http') == -1:
                #     origin_url = 'https:'+origin_url
                # origin_osp = origin_url.split('//')[1].split('.')[0]
                # if origin_osp.find('www') != -1:
                #     origin_osp = origin_osp.split('www.')[1]

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'layar-drakor',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'indonesia',
                    'cnt_writer': ''
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
    except:
        pass

    dbInResult = dbUpdate(url)

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getUrl = gethost(osp_id)

    print("layar-drakor 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("layar-drakor 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
