import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
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
    link = 'http://phimmoizvn.net/phim-bo-han-quoc/trang-{}'
    while check:
        i = i+1
        if i == 10:
            break

        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find_all('div',  'product-wrap')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('img')['alt']
                title_null = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null,  getKey)
                
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                url2 = soup.find('a', 'btn-product')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                
                tapStr = soup.find('ul',  'list-type-check').find_all('li')[1].text.replace('Số tập:','').replace(' ','')
                if tapStr == '' or tapStr == 'Đangcậpnhật':
                    continue
                
                tapNum = int(tapStr)
                for i in range(1, tapNum):
                    host_url = url2+'/tap-'+str(i)
                    title_num = str(i)
                    title = titleSub+'_'+title_num
                    title_null = titleNull(title)
                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'phimmoizvn',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
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
        except Exception as e:
            print(e)
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phimmoizvn 크롤링 시작")
    startCrawling()
    print("phimmoizvn 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
