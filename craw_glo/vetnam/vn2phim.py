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
    link = 'http://vn2phim.com/danh-muc/p/'+site+'/'
    link2 = '.aspx'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'boxrightmid').find_all('div', 'Form2')

        try:
            for item in div:
                url = 'http://vn2phim.com'+item.find('a')['href']
                titleSub = item.find('img')['alt']
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
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
                url2 = soup.find('div', 'playphim').find('a')['href'].replace('..', 'http://vn2phim.com/xem')
                print(url2)

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'box_film_title')

                for item in div:
                    if item.find('a'):
                        sub = item.find_all('a')
                        for item in sub:
                            host_url = 'http://vn2phim.com'+item['href']
                            title = titleSub+'_'+item.text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'vn2phim',
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
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("vn2phim 크롤링 시작")
    site = ['10', '19']
    for s in site:
        startCrawling(s)
    print("vn2phim 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
