import requests
import time
import json
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
    link = 'https://trymobile.ru/MobileSerial/Doramy/items.php?page={}'
    while check:
        i = i+1
        if i == 30:
            break

        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div','m0001')
        try:
            for item in div:
                url = 'https://trymobile.ru/MobileSerial/Doramy/' + item.find('a')['href']
                title = item.find('img')['alt'].strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

            
                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'trymobile.ru',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'russia',
                    'cnt_writer': '',
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("trymobile.ru 크롤링 시작")
    startCrawling()
    print("trymobile.ru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
