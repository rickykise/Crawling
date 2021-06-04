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

def startCrawling(link):
    i = 0;check = True
    r = requests.get(link)
    r.encoding = r.apparent_encoding
    c = r.text
    soup = BeautifulSoup(c, 'html.parser')
    sub = soup.find('div', 'list_alone').find_all('a','sizing')
    for item in sub:
        try:
            url = 'https://bigdramas.com'+item['href']
            titleSub = item.text.strip()
            title_check = titleNull(titleSub)

            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_check, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']

            r = requests.get(url)
            r.encoding = r.apparent_encoding
            c = r.text
            soup = BeautifulSoup(c,"html.parser")

            episode = soup.find('div','album_list').find_all('a')
            for item in episode:
                host_url = 'https://bigdramas.com'+item['href']
                title = titleSub+'_'+item.text.strip()
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'bigdramas',
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
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("bigdramas 크롤링 시작")
    site = ['https://bigdramas.com/%E9%9F%93%E5%8A%87/','https://bigshows.org/%E9%9F%93%E7%B6%9C/']
    for item in site:
        startCrawling(item)
        
    print("bigdramas 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
