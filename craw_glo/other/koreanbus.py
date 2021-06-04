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
    site = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for item in site:
        i = 0;check = True
        link = "https://koreanbus.su/letter/"+item
        while check:
            i = i+1
            if i == 2:
                break
            r = requests.get(link)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            if soup.find('div', 'TPTblCn TPTblCnMvs'):
                tr = soup.find('div', 'TPTblCn TPTblCnMvs').find('tbody').find_all('tr')
                try:
                    for item in tr:
                        url = item.find('a')['href']
                        titleSub = item.find_all('a')[1].text.strip()
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
                        div = soup.find_all('div', 'TPTblCn AA-cont')

                        for item in div:
                            tr = item.find_all('tr')
                            for item in tr:
                                host_url = item.find('td', 'MvTbTtl').find('a')['href']
                                title = titleSub+'_'+ item.find('td', 'MvTbTtl').find('a').text.strip()
                                title_null = titleNull(title)

                                data = {
                                    'cnt_id': cnt_id,
                                    'cnt_osp' : 'koreanbus',
                                    'cnt_title': title,
                                    'cnt_title_null': title_null,
                                    'host_url' : host_url,
                                    'host_cnt': '1',
                                    'site_url': url,
                                    'cnt_cp_id': 'sbscp',
                                    'cnt_keyword': cnt_keyword,
                                    'cnt_nat': 'other',
                                    'cnt_writer': ''
                                }
                                # print(data)
                                # print("=================================")

                                dbResult = insertALL(data)
                except:
                    continue
            else:
                break

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("koreanbus 크롤링 시작")
    startCrawling()
    print("koreanbus 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
