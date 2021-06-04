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
    link = 'https://dofreefree.com/genre/ซีรีย์-เกาหลี/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', id=re.compile('post-+'))

        try:
            for item in article:
                imgUrl = item.find('img')['src']
                url = item.find('a')['href']
                url = urllib.parse.unquote(url)
                titleSub = item.find('img')['alt']
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
                li = soup.find('ul', id='playeroptionsul').find_all('li')

                for item in li:
                    host_url = url
                    title = item.find('span', 'title').text.strip()
                    if title.find('EP.') != -1:
                        num_check = title.split('EP.')[1]
                        host_url = host_url+num_check
                    title_null = titleNull(title)


                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'dofreefree',
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

    print("dofreefree 크롤링 시작")
    startCrawling()
    print("dofreefree 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
