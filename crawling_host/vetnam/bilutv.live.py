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
    url = url;cnt_id = keyItem[0];cnt_osp = keyItem[1];cnt_title = keyItem[2];cnt_nat = keyItem[3];cnt_keyword = ''

    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        nonce = text.split('nonce":"')[1].split('"')[0]
        id = str(soup.find('body')['class']).split('postid-')[1].split("'")[0]
        data = {
            'action': 'itfs_ajax_show_all_eps_list',
            'episode': '1',
            'postid': id,
            'server': '1'
        }
        link = 'https://bilutv.live/wp-admin/admin-ajax.php'

        r = requests.post(link, data=data)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('li', 'itfs-episode')

        for item in li:
            episode = item.find('span')['data-episode']
            server = item.find('span')['data-server']
            postid = item.find('span')['data-post-id']

            host_url = 'https://bilutv.live/wp-admin/admin-ajax.php?action=itfs_ajax_player&nonce='+nonce+'&episode='+episode+'&server='+server+'&postid='+postid
            title = cnt_title+'_'+item.find('span').text.strip()
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'bilutv.live',
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

    print("bilutv.live 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("bilutv.live 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
