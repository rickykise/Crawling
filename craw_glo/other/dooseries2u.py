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
    i = 0;check = True
    link = "https://dooseries2u.com/series-korea/page/{}"
    while check:
        i = i+1
        if i == 7:
            break

        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        movie = soup.find('div', 'grid-movie').find_all('div','movie')

        try:
            for item in movie:
                url = item.find('a')['href']
                titleSub = item.find('div','m-title').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                host_url = url
                
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                title = soup.find('figure',  'thumb-movie').find('img')['alt'].strip()
                if title.find('(') != -1:
                    title = title.split('(')[0].strip()
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp': 'dooseries2u',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url': host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'other',
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

    print("dooseries2u 크롤링 시작")
    startCrawling()
    print("dooseries2u 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
