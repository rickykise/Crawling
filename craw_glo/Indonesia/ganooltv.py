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
    link = "http://www.ganooltv.com/tv/page/{}/"
    while check:
        i = i+1
        if i == 24:
            break
        try:
            r = requests.get(link.format(str(i)))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            article = soup.find('div', id='gmr-main-load').find_all('article')
            for item in article:
                url = item.find('div','content-thumbnail').find('a')['href']
                titleSub = item.find('h2', 'entry-title').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                print(titleSub)
                print(keyCheck)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                print(url)
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('main', id='main').find('div', 'gmr-listseries').find_all('a','button')
                for item in sub:
                    r1 = requests.get(item['href'])
                    c = r1.content
                    soup = BeautifulSoup(c,"html.parser")
                    server = soup.find('ul','muvipro-player-tabs').find_all('a')
                    for s in server:
                        title = titleSub+'_'+item.text.strip()
                        title_null = titleNull(title)
                        host_url = s['href']
                        if host_url == '#':
                            host_url = item['href']
                        elif host_url.find('https:') == -1:
                            host_url = 'http://www.ganooltv.com'+host_url
                        
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'ganooltv',
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
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("ganooltv 크롤링 시작")
    startCrawling()
    print("ganooltv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
