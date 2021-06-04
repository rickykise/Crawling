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
    link = 'https://a4.bclink.one/cate/'+site+'/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find('table', id='sampleTable').find_all('tr')

        try:
            for item in tr:
                if item.find('td'):
                    url = 'https://a4.bclink.one'+item.find_all('td')[1].find('a')['href']
                    cnt_num = url.split(site+'/')[1]
                    title = item.find_all('td')[1].find('a').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    form = soup.find_all('form', target="_blank")

                    for item in form:
                        host_url = item.find_all('input')[2]['value']
                        origin_url = host_url

                        if origin_url.find('https') == -1:
                            origin_url = 'https:'+origin_url
                        origin_osp = origin_url.split('//')[1]
                        if origin_osp.find('www') != -1:
                            origin_osp = origin_osp.split('www.')[1].split('.')[0]
                        else:
                            origin_osp = origin_osp.split('.')[0]

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'a4.bclink',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
                            'cnt_writer': '',
                            'origin_url': origin_url,
                            'origin_osp': origin_osp
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("a4.bclink 크롤링 시작")
    site = ['onairdrama', 'drama', 'comedy']
    for s in site:
        startCrawling(s)
    print("a4.bclink 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")