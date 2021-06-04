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

def startCrawling():
    i = 0;check = True
    link = "https://alldorama.com/korejskie-serialy/page/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'mov clearfix')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
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
                span = soup.find('div', 'series-list').find_all('span')

                for item in span:
                    if item.find('a'):
                        host_url = item.find('a')['href']
                        title_num = item.find('a').text.strip()
                        title = titleSub+'_'+title_num
                        title_null = titleNull(title)
                    else:
                        host_url = url
                        title_num = item.text.strip()
                        title = titleSub+'_'+title_num
                        title_null = titleNull(title)

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    origin_url = str(soup).split("uvk.player('")[1].split("'")[0].replace('amp;', '')

                    if origin_url.find('http') == -1:
                        origin_url = 'https:'+origin_url
                    origin_osp = origin_url.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    elif origin_osp.find('myqcloud') != -1:
                        origin_osp = 'myqcloud'
                    else:
                        origin_osp = origin_osp.split('.')[0]


                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'alldorama',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'russia',
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

    print("alldorama 크롤링 시작")
    startCrawling()
    print("alldorama 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
