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
    link = 'http://kshow123.net/show/'

    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find_all('div', 'col-md-6 col-sm-6')
    for item in div:
        try:
            url = item.find('a')['href']
            titleSub = item.find('a').text.strip()
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
            td = soup.find('tbody', 'list-episode').find_all('td',class_=False)

            for item in td:
                host_url = item.find('a')['href']
                title = item.find('a')['title'].strip()
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'kshow123',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kshow123 크롤링 시작")
    startCrawling()
    print("kshow123 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
