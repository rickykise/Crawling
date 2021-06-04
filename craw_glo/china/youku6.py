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

def startCrawling(param):
    i = 0;check = True
    link = "http://youku6.com/"+param[0]
    while check:
        i = i+1
        if i == param[1]:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'fed-list-info').find_all('li')

        try:
            for item in li:
                url = 'http://youku6.com'+item.find('a','fed-list-title')['href']
                titleSub = item.find('a','fed-list-title').text.strip()
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
                sub = soup.find('div','fed-play-item fed-drop-item fed-visible').find_all('ul',class_='fed-part-rows')[1].find_all('li')

                for item in sub:
                    host_url = 'http://youku6.com'+item.find('a')['href']
                    title = titleSub+'_'+item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'youku6',
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
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("youku6 크롤링 시작")
    page = {
        'o':['o/3--------{}---.html',23],
        'y':['y/20-{}.html',12]
    }
    for item in page.values():
        startCrawling(item)
    print("youku6 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
