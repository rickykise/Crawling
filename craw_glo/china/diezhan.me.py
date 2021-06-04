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
    link = "http://www.diezhan.me/rihan/index{}.html"
    
    while check:
        i = i+1
        if i == 11:
            break
        
        if i == 1:
            link = link.format('')
        else:
            link = link.format(str(i))

        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find('ul',  'myui-vodlist').find_all('li')
        try:
            for item in li:
                url = 'http://www.diezhan.me'+item.find('a', 'myui-vodlist__thumb')['href']
                titleSub = item.find('a', 'myui-vodlist__thumb')['title'].strip()
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
                li = soup.find('div', 'tab-content').find_all('li')

                for item in li:
                    host_url = 'http://www.diezhan.me'+item.find('a')['href']
                    title = titleSub+'_'+item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'diezhan.me',
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
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("diezhan.me 크롤링 시작")
    startCrawling()
    print("diezhan.me 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
