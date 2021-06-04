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
    link = 'https://kan1990.com/vodshow/lianxuju-%E9%9F%A9%E5%9B%BD-------{}---/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul','fed-list-info').find_all('li')
        try:
            for item in li:
                url = 'https://kan1990.com'+item.find('a','fed-list-title')['href']
                titleSub = item.find('a','fed-list-title').text
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('ul','fed-part-rows')
                for item in div:
                    sub = item.find_all('a','fed-btns-info')
                    for item in sub:
                        host_url = 'https://kan1990.com'+item['href']
                        title = titleSub + '_' + item.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'kan1990',
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

    print("kan1990 크롤링 시작")
    startCrawling()
    print("kan1990 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
