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

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': '',
    'Cookie': '__cfduid=dfb327726259d268599e268b1cc7240421587454340; PHPSESSID=71e8eb63e4885f41774d06bb8662e491; _ga=GA1.2.1544374972.1587454342; _gid=GA1.2.2001870129.1587454342; sign=21960; __cfduld=NGY5N2Q4ZTc4OGJjZmMyOTdiY2JiMTQ0YmVhZjllYjQ%3D; vietnamese=true',
    'Host': 'xomphimhay.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(url, keyItem):
    url = url;cnt_id = keyItem[0];cnt_osp = keyItem[1];cnt_title = keyItem[2];cnt_nat = keyItem[3];cnt_keyword = ''

    try:
        r = requests.get(url, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        url2 = soup.find('a', 'btn-danger')['href']

        r = requests.get(url2, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'htmlwrap')

        for item in div:
            li = item.find_all('li', 'xpo-episode')
            for item in li:
                host_url = item.find('a')['href']
                titleNum = item.find('a').text.strip()
                title = cnt_title+'_'+titleNum
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'xomphimhay',
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

    print("xomphimhay 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("xomphimhay 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
