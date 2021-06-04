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
    link = 'http://111.90.150.31/network/sbs/'
    
    r = requests.get(link)
    c = r.text
    soup = BeautifulSoup(c,"html.parser")
    article = soup.find_all('article', 'item tvshows')

    for item in article:
        try:
            url = item.find('h3').find('a')['href']
            titleSub = item.find('h3').find('a').text.strip()
            if titleSub.find('(') != -1:
                titleSub = titleSub.split('(')[0].strip()
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
            div = soup.find('ul','episodios').find_all('div','episodiotitle')
            for item in div:
                host_url = item.find('a')['href']
                title = titleSub+'_'+item.find('a').text.strip()
                title_null = titleNull(title)
                
                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'idlix',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'indonesia',
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

    print("idlix 크롤링 시작")
    startCrawling()
    print("idlix 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
