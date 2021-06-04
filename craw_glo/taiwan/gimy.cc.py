import requests
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.py')[0]
getDel = ospCheck(osp_id)

def startCrawling(craw):
    i = 0;check = True
    while check:
        i = i+1
        if i == craw['end']:
            break
        
        r = requests.get(craw['link'].format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'stui-vodlist').find_all('li')
        try:
            for item in li:
                url = 'https://gimy.cc'+item.find('a','lazyload')['href']
                titleSub = item.find('a','lazyload')['title']
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
                btn = soup.find('div','tab-content').find_all('a',href=lambda x: x and "/video/" in x)

                for item in btn:
                    host_url = 'https://gimy.cc'+item['href']
                    title = titleSub + '_' + item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'gimy.cc',
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

    print("gimy.cc 크롤링 시작")
    site = [{'link':'https://gimy.cc/vodshow/krdr-%E9%9F%93%E5%9C%8B--/page/{}.html','end':30},{'link':'https://gimy.cc/vodshow/variety-%E9%9F%93%E5%9C%8B--/page/{}.html','end':23}]
    for item in site:
        startCrawling(item)
    print("gimy.cc 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
