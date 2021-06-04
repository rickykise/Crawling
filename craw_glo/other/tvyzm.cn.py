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

def startCrawling(link):
    i = 0;check = True
    while check:
        i = i+1
        if i == link[1]:
            break
        r = requests.get(link[0].format(str(i)))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find_all('li',  'fed-list-item')

        try:
            for item in li:
                url = 'http://tvyzm.cn'+item.find('a', 'fed-list-title')['href']
                titleSub = item.find('a',  'fed-list-title').text.strip()
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
                div = soup.find_all('div',  'fed-drop-boxs fed-drop-btms fed-matp-v')
                for item in div:
                    li = item.find_all('li', {'class':['fed-padding', 'fed-col-xs3', 'fed-col-md2', 'fed-col-lg1']})
                    for item in li:
                        if item.find('a', 'fed-btns-info') == None:
                            continue
                        host_url = 'http://tvyzm.cn'+item.find('a', 'fed-btns-info')['href']
                        title = titleSub+'_'+item.find('a', 'fed-btns-info').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'tvyzm.cn',
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
                        print(data)
                        print("=================================")

                        dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("tvyzm.cn 크롤링 시작")
    site=[('http://tvyzm.cn/index.php/vod/show/id/15/page/{}.html', 27), ('http://tvyzm.cn/index.php/vod/show/id/31/page/{}.html', 10)]
    for item in site:
        startCrawling(item)
    print("tvyzm.cn 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
