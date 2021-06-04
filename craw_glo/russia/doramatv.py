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
        link = "https://doramatv.live/list/country/south_korea?sortType=updated"
        i = i+1
        if i == 30:
            break
        
        if i != 1:
            link = link+'&offset={}' 
            r = requests.get(link.format(str(i)))
        else:
            r = requests.get(link)

        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'tiles').find_all('div','tile')

        try:
            for item in div:
                if item.find('span','mangaEmpty'):
                    continue
                url = 'https://doramatv.live'+item.find('h3').find('a')['href']
                titleSub = item.find('h4')['title']
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
                sub = soup.find('div', 'chapters-link').find_all('a')

                for item in sub:
                    host_url = 'https://doramatv.live'+item['href']
                    title = item.text.replace('\n','').replace('                     ','').replace('         ','').replace('новое','').strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'doramatv',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'russia',
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

    print("doramatv 크롤링 시작")
    startCrawling()
    print("doramatv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")