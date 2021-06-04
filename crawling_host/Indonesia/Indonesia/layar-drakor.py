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
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)


def startCrawling(site):
    i = 0;check = True
    link = 'https://layar-drakor.com/'+site+'/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'ml-item')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('span', 'mli-info').text.strip()
                title_check = titleNull(titleSub)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'les-content').find_all('a')

                for item in li:
                    host_url = item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    post_one  = requests.get(link)
                    c = post_one.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')

                    r = requests.get(host_url)
                    c = r.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                    origin_url = soup.find('div', 'movieplay').find('iframe')['data-lazy-src']
                    if origin_url.find('http') == -1:
                        origin_url = 'https:'+origin_url
                    origin_osp = origin_url.split('//')[1].split('.')[0]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1]

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

    print("layar-drakor 크롤링 시작")
    site = ['series','episode']
    for s in site:
        startCrawling(s)
    print("layar-drakor 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
