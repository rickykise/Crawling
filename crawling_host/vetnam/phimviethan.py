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
    'Accept-Language': 'ko-KR',
    'Host': 'phimviethan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(url, keyItem):
    url = url;cnt_id = keyItem[0];cnt_osp = keyItem[1];cnt_title = keyItem[2];cnt_nat = keyItem[3];cnt_keyword = ''

    try:
        r = requests.get(url, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        url2 = soup.find('a', 'btn btn-red')['href']

        r = requests.get(url2, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        ul = soup.find_all('ul', 'list-episode')

        for item in ul:
            li = item.find_all('li')
            for item in li:
                host_url = item.find('a')['href']
                title = cnt_title + '_' + item.find('a').text.strip()
                title_null = titleNull(title)

                r = requests.get(host_url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                if soup.find('iframe'):
                    origin_url = soup.find('iframe')['src']
                    if origin_url.find('api.') != -1:
                        origin_check = origin_url.replace('api.', '')
                    origin_osp = origin_check.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    else:
                        origin_osp = origin_osp.split('.')[0]
                else:
                    origin_url = ''
                    origin_osp = ''

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'phimviethan',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'vietnam',
                    'cnt_writer': '',
                    'origin_url': origin_url,
                    'origin_osp': origin_osp
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

    print("phimviethan 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("phimviethan 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
