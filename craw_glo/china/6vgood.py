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
    while check:
        i = i+1
        if i == 30:
            break
        link = 'http://www.6vgood.com/rj'
        if i != 1:
            link = 'http://www.6vgood.com/rj/index_{}.html'.format(str(i))
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'listBox').find('ul').find_all('li')

        try:
            for item in div:
                url = item.find('div','listInfo').find('a')['href']
                title = item.find('div','listInfo').find('a')['title'].strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                host_url = url
                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : '6vgood',
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
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("6vgood 크롤링 시작")
    startCrawling()
    print("6vgood 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
