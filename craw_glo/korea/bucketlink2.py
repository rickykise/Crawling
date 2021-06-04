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
    link = 'http://bucketlink2.net/cate/'+site+'/page/'
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
                    url = 'http://bucketlink2.net'+item.find_all('td')[1].find('a')['href']
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
                        cnt_writer = item.find('a').text.strip()
                        if cnt_writer.find('링크') != -1:
                            cnt_writer = cnt_writer.split('링크')[0].strip()

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'bucketlink2',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
                            'cnt_writer': cnt_writer
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("bucketlink2 크롤링 시작")
    site = ['onairdrama', 'drama']
    for s in site:
        startCrawling(s)
    print("bucketlink2 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
