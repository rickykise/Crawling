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
        text = str(soup)

        drt = text.split("drt:'")[1].split("',")[0].strip()
        mid = text.split('mid:"')[1].split('",')[0].strip()
        num = text.split('",num:')[1].split(',')[0].strip()
        pos = int(soup.find('li', 'eps_list_tab_div').find('a')['data-pos'])*10-1
        idx = str(pos)
        range = soup.find('li', 'eps_list_tab_div').find('a')['data-range']
        sort = text.split("sort:'")[1].split("',")[0].strip()
        inchd = text.split("inchd:'")[1].split("',")[0].strip()
        end_idx = soup.find('li', 'eps_list_tab_div').find('a')['data-eidx']

        ajax_url = 'https://stats.phimnhanh.tv/content/subitems?drt='+drt+'&mid='+mid+'&num='+num+'&idx='+idx+'&range='+range+'&sort='+sort+'&inchd='+inchd+'&end_idx='+end_idx

        r = requests.get(ajax_url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup).replace('\\', '')

        for item in text:
            host_url = text.split("ntthref='"+'"')[a].split('"')[0]
            title = cnt_title+'_'+text.split("<a")[a].split('"="')[0].strip()
            title_null = titleNull(title)
            a = a+1

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'phimnhanh.tv',
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

    dbInResult = dbUpdate(url)

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getUrl = gethost(osp_id)

    print("phimnhanhtv 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("phimnhanhtv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
