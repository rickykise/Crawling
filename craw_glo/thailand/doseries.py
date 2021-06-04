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
    link = 'https://web.doseries.com/category_1?page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'products').find_all('div', 'col-md-3')

        try:
            for item in div:
                url = 'https://web.doseries.com'+item.find('div', 'movie-item-title').find('a')['href']
                getid = item.find('div', 'movie-item-title').find('a')['href'].split('view_')[1]
                titleSub = item.find('div', 'movie-item-title').find('a').text.strip()
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
                text = str(soup)
                appds_id = text.split('"appds_id": "')[1].split('",')[0]
                url2 = 'https://web.doseries.com/load_ep.php?appds_id='+appds_id+'&id='+getid

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find_all('a')

                for item in sub:
                    host_url = 'https://web.doseries.com'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'doseries',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("doseries 크롤링 시작")
    startCrawling()
    print("doseries 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
