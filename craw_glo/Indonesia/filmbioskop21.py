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
    link = 'https://filmbioskop21.com/movie/category/country/south-korea/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'recent-posts').find_all('li', 'post')

        try:
            for item in li:
                cnt_num = item['id'].split('-')[1].strip()
                titleSub = item.find('div', 'post-content').find('h2').text.split('Film')[1].split('(')[0].strip()
                title_check = titleNull(titleSub)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                url = item.find('a')['href']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find('div', id='content').find_all('a', 'btn')

                for item in div:
                    host_url = item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    text = str(soup)

                    origin_url = text.split('<iframe')[1].split('src=')[1].split('"')[1].split('"')[0]
                    if origin_url.find('https') == -1:
                        origin_url = 'https:'+origin_url
                    origin_osp = origin_url.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    else:
                        origin_osp = origin_osp.split('.')[0]


                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'filmbioskop21',
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

    print("filmbioskop21 크롤링 시작")
    startCrawling()
    print("filmbioskop21 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
