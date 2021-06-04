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
    i = 0;check = True;a = 1
    link = 'https://myasietv.net/category/drama-coreen/page/'
    while check:
        i = i+1
        if i == 50:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'moviefilm')

        try:
            for item in div:
                imgUrl = item.find('img')['src']
                url = item.find('a')['href']
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

                if soup.find('div', 'keremiya_part').find('a'):
                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'myasietv',
                        'cnt_title': titleSub,
                        'cnt_title_null': title_check,
                        'host_url' : url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'france',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)

                    sub = soup.find('div', 'keremiya_part').find_all('a')

                    for item in sub:
                        host_url = item['href']
                        title = titleSub+'_'+item.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'myasietv',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'france',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
                else:
                    div = soup.find('div', 'filmicerik').find_all('p')

                    for item in div:
                        if item.find('iframe'):
                            host_url = item.find('iframe')['src']

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'myasietv',
                                'cnt_title': titleSub,
                                'cnt_title_null': title_check,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'france',
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

    print("myasietv 크롤링 시작")
    startCrawling()
    print("myasietv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")