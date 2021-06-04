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
    link = 'https://kissasianwatch.com/'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    listArr = soup.find('div', id='categories-4').find('div','widget-container').find_all('a')
    for item in listArr:
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
            article = soup.find('div',id="main-content").find_all('article', 'item-list')
            
            for item in article:
                host_url = item.find('h2','post-box-title').find('a')['href']
                title = item.find('h2','post-box-title').text.strip()
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp': 'kissasianwatch',
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

    print("kissasianwatch 크롤링 시작")
    startCrawling()
    print("kissasianwatch 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
