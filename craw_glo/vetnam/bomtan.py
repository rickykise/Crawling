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
    link = 'https://bomtan.net/quoc-gia/phim-han-quoc-'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'list-film').find_all('li', 'film-item')

        try:
            for item in li:
                url = 'http://bomtan.net'+item.find('a')['href']
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

                titleEng = soup.find('div', 'film-info').find('h2', 'real-name').text.strip()
                if titleEng.find('(') != -1:
                    titleEng = titleEng.split('(')[0].strip()
                url2 = 'https://bomtan.net'+soup.find('a', 'btn-see')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'episodes').find('ul', 'list-episode').find_all('li')

                for item in li:
                    host_url = 'https://bomtan.net' + item.find('a')['href']
                    if host_url.find('#') != -1:
                        continue
                    title = titleSub + titleEng + '_' + item.find('a').text.strip()
                    title_null = titleNull(title)
                    # host_cnt = len(soup.find('div', 'list-server').find_all('span', 'btn'))

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'bomtan',
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

    print("bomtan 크롤링 시작")
    startCrawling()
    print("bomtan 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
