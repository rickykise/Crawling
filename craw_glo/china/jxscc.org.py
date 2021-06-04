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
    link = 'http://jxscc.org/maccms10/index.php/vod/show/area/%E9%9F%A9%E5%9B%BD/id/11/page/{}.html'
    while check:
        i = i+1
        if i == 13:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('li', 'fed-list-item')

        try:
            for item in li:
                url = 'http://jxscc.org'+item.find('a','fed-list-title')['href']
                titleSub = item.find('a', 'fed-list-title').text.strip()
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
                div = soup.find_all('div', {'class':['fed-tabs-item','fed-drop-info']})

                for item in div:
                    li = item.find_all('li',{'class':['fed-padding','fed-col-xs3','fed-col-md2','fed-col-lg1']})
                    for item in li:
                        if item.find('a','fed-btns-info') == None:
                            continue
                        host_url = 'http://jxscc.org'+item.find('a','fed-btns-info')['href']
                        title = titleSub+'_'+item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'jxscc.org',
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

    print("jxscc.org 크롤링 시작")
    startCrawling()
    print("jxscc.org 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
