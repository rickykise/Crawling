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
    i = 0;check = True;a = 1;aSub = 1;subI = 0;check_Title = '';firstCheck = True
    link = 'https://www.hodutv3.top/tvshow/'+site+'?page='
    while check:
        checkSub = True
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)

        try:
            for item in text:
                if a == 49:
                    a = 1
                    break
                url = 'https://www.hodutv3.top'+text.split('<div class="bao">')[a].split('<div class="middle">')[0].split('<a href="')[1].split('">')[0]+'?page='
                title = text.split('<div class="bao">')[a].split('<div class="middle">')[0].split('alt = "')[1].split('">')[0]
                title_null = titleNull(title)
                a = a+1

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

                while checkSub:
                    subI = subI+1
                    if subI == 10:
                        subI = 0
                        break;checkSub=False
                    r = requests.get(url+str(subI))
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    text = str(soup)

                    try:
                        for item in text:
                            host_url = text.split('<div class="thumbnail1">')[aSub].split('</strong')[0].split('<a href="')[1].split('">')[0].replace('hodutv2', 'hodutv3')
                            if host_url.find('&amp') != -1:
                                host_url = host_url.split('&amp')[0]
                            title = text.split('<div class="thumbnail1">')[aSub].split('</strong')[0].split('<strong>')[1].strip()
                            title_null = titleNull(title)
                            aSub = aSub+1

                            r = requests.get(host_url)
                            c = r.content
                            soup = BeautifulSoup(c,"html.parser")
                            textOrigin = str(soup)
                            origin_url = textOrigin.split('<iframe ')[1].split('</iframe')[0].split('src="')[1].split('"')[0]

                            if origin_url.find('https') == -1:
                                origin_url = 'https:'+origin_url
                            origin_osp = origin_url.split('//')[1]
                            if origin_osp.find('www') != -1:
                                origin_osp = origin_osp.split('www.')[1].split('.')[0]
                            else:
                                origin_osp = origin_osp.split('.')[0]

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'hodutv3',
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
                            print(data)
                            print("=================================")

                            # dbResult = insertALL(data)
                    except:
                        aSub = 1
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("hodutv3 크롤링 시작")
    site = ['drama', 'entertainment']
    for s in site:
        startCrawling(s)
    print("hodutv3 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
