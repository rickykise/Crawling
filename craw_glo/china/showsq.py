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
    i = 0;end=30;check = True
    link = 'https://u8online.com/kr/'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find('div','thumb').find_all('div','drama')
    for item in div:
        try:
            url = 'https://u8online.com/'+item.find('a')['href'].split('/')[1]+'/all.html'
            titleSub = item.find('a').get("title")
            if titleSub == None:
                titleSub = item.find('a').text.split('(')[0]
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
            sub = soup.find('div','items').find_all('a')
            for item in sub:
                host_url = 'https://u8online.com'+item['href']
                title = item.text.strip()
                title_null = titleNull(title)
                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'showsq',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("showsq 크롤링 시작")
    startCrawling()
    print("showsq 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")