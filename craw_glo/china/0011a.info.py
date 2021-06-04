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

def startCrawling():
    i = 0;check = True
    link = 'http://www.0011a.info/zdse/----韩国------{}---.html'
    while check:
        i = i+1
        if i == 16:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find('ul',  'stui-vodlist').find_all('li')
        try:
            for item in li:
                url = 'http://www.0011a.info'+item.find('a', 'lazyload')['href']
                titleSub = item.find('a', 'lazyload')['title']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                ul = soup.find_all('ul', 'myui-content__list')

                for item1 in ul:
                    a = item1.find_all('a')
                    for item2 in a:
                        host_url = 'http://www.0011a.info'+item2['href']
                        title = titleSub + '_' + item2.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': '0011a.info',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url': host_url,
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

    print("0011a.info 크롤링 시작")
    startCrawling()
    print("0011a.info 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
