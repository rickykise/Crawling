import requests
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://dizilla.net/kanal/sbs/'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    sub = soup.find('div', 'verticalList').find_all('a')

    for item in sub:
        url = item['href']
        titleSub = item['title']
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
        palyList = soup.find('div', 'tab-content').find_all('a',href=lambda x: x and "https://dizilla.net" in x,title=lambda x: x and "#" not in x)

        for item in palyList:
            host_url = item['href']
            title = item['title'].strip()
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'dizilla',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'turkey',
                'cnt_writer': ''
            }
            print(data)
            print("=================================")

            # dbResult = insertALL(data)

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dizilla 크롤링 시작")
    startCrawling()
    print("dizilla 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
