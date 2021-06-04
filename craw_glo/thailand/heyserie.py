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
    link = "https://www.heyserie.com/category/1?page="
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'halim_box').find_all('div', 'grid-item')

        try:
            for item in div:
                url = 'https://www.heyserie.com'+item.find('a')['href']
                titleSub = item.find('div', 'halim-post-title').text.strip()
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
                div = soup.find_all('script', type='text/javascript')
                for item in div:
                    text = str(item)
                    if text.find('appds_id') != -1:
                        appds_id = text.split('"appds_id": "')[1].split('",')[0]
                        getid = url.split('v')[1]
                        url2 = 'https://www.heyserie.com/load_ep.php?appds_id='+appds_id+'&id='+getid

                        r = requests.get(url2)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        li = soup.find_all('li')

                        for item in li:
                            host_url = 'https://www.heyserie.com'+item.find('a')['href']
                            title = titleSub+'_'+item.find('a').text.strip()
                            if title.find('Teaser') != -1:
                                continue
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'heyserie',
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

    print("heyserie 크롤링 시작")
    startCrawling()
    print("heyserie 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
