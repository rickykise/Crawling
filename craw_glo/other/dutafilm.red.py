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
    i = 0;end=15;check = True
    link = 'https://dutafilm.red/drama-korea/{}'
    while check:
        i = i+1
        if i == end:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        items = soup.find('div', 'mv-content-items').find_all('a')

        try:
            for item in items:
                url = item['href']
                titleSub = item['title'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                
                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'dutafilm.red',
                    'cnt_title': titleSub,
                    'cnt_title_null': title_check,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'china',
                    'cnt_writer': ''
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dutafilm.red 크롤링 시작")
    startCrawling()
    print("dutafilm.red 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
