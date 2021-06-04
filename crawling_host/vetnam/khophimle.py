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
        text = str(soup)
        nonce = text.split('nonce":"')[1].split('"')[0]
        url2 = soup.find('div', 'halim-watch-box').find('a')['href']

        r = requests.get(url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        id = soup.find('div', 'user-rate')['data-id']
        ajax_url = 'https://khophimle.net/wp-admin/admin-ajax.php'

        data = {
            'action': 'halim_ajax_show_all_eps_list',
            'episode': '1',
            'postid': id,
            'server': '1'
        }

        r = requests.post(ajax_url, data=data)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'halim-server show_all_eps')

        for item in div:
            li = item.find_all('li')
            for item in li:
                episode = item.find('span')['data-episode']
                server = item.find('span')['data-server']

                chu = url2.split('chu-')[1]
                num = url2.split('tap-')[1].split('-')[0]
                host_url = url2.replace('tap-'+num, 'tap-'+episode).replace('chu-'+chu, 'chu-'+server)
                title = cnt_title+'_'+episode
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'khophimle',
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

    print("khophimle 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("khophimle 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
