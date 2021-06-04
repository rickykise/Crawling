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
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(url, keyItem):
    url = url;cnt_id = keyItem[0];cnt_osp = keyItem[1];cnt_title = keyItem[2];cnt_nat = keyItem[3];cnt_keyword = ''

    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', id='playeroptionsul').find_all('li')

        for item in li:
            host_link = 'https://dofreefree.com/wp-admin/admin-ajax.php'
            nume = item['data-nume']
            if nume == 'trailer':
                continue
            post = item['data-post']
            type = item['data-type']
            data = {
                'action': 'doo_player_ajax',
                'nume': nume,
                'post': post,
                'type': type
            }

            r = requests.post(host_link, data=data)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            host_url = soup.find('iframe')['src'].strip()
            if host_url == '' or host_url.find('kdramahood') != -1:
                continue
            if host_url.find('http') == -1:
                host_url = 'https:'+host_url

            title = item.find('span', 'title').text.strip()
            if title.find('EP.') != -1:
                num_check = title.split('EP.')[1]
                host_url = host_url+num_check
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'dofreefree',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'thailand',
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

    print("dofreefree 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("dofreefree 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
