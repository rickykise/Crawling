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
    link = 'https://mycima.life/language/الكورية/list/series/'

    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    div = soup.find_all('div',  'GridItem')

    for item in div:
        try:
            url = item.find('a')['href']
            titleSub = item.find('a')['title'].strip()
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
            sub = soup.find('div',  'Seasons--Episodes').find_all('a')

            for item in sub:
                host_url = item['href']
                title = titleSub+'_'+item.text.strip()
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp': 'mycima.life',
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
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("mycima.life 크롤링 시작")
    startCrawling()
    print("mycima.life 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
