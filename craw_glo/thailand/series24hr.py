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
    link = 'https://www.series24hr.com/category/ซีรี่ย์เกาหลี-korean-series/page/'
    while check:
        i = i+1
        if i == 30:
            break
        try:
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            div = soup.find('div', 'items').find_all('div', 'item')

            for item in div:
                cnt_num = item['id'].split('-')[1].strip()
                url = item.find('a')['href']
                titleSub = item.find('div', 'fixyear').find('h2').text.strip()
                if titleSub.find('[') != -1:
                    titleSub = titleSub.split('[')[0].strip()
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
                div = soup.find('div', 'entry-content').find_all('a')

                for item in div:
                    host_url = item['href']
                    title = item.text.strip()
                    title_null = titleNull(title)

                    # r = requests.get(host_url)
                    # c = r.content
                    # soup = BeautifulSoup(c,"html.parser")
                    # server_url = soup.find('div', 'entry-content').find('iframe')['src']
                    #
                    # r = requests.get(server_url)
                    # c = r.content
                    # soup2 = BeautifulSoup(c,"html.parser")
                    # host_cnt = 1

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'series24hr',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
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

    print("series24hr 크롤링 시작")
    startCrawling()
    print("series24hr 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
