import requests
import time
import sys, os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    link = 'https://asiantaxi.su/series/list-mode/'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    series = soup.find_all('a', 'series')
    for item in series:
        try:
            url = item['href']
            titleSub = item.text.strip()
            title_check = titleNull(titleSub)

            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_check,  getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']

            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c, "html.parser")
            epl = soup.find('div', 'eplister').find_all('a')

            for item in epl:
                host_url = item['href']
                title = titleSub+'_'+item.find('div','epl-num').text.strip()
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp': 'asiantaxi.su',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url': host_url,
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
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("asiantaxi.su 크롤링 시작")
    startCrawling()
    print("asiantaxi.su 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
