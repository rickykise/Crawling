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

def startCrawling(tid):
    i = 0;check = True
    link = 'https://www.516ys.com/search.php?page={}&searchtype=5&tid={}&area=%E9%9F%A9%E5%9B%BD'
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link.format(str(i), tid))
        c = r.text
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find('ul',  'vodlist').find_all('li', 'vodlist_item')
        try:
            for item in li:
                url = 'https://www.516ys.com'+item.find('a')['href']
                titleSub = item.find('a')['title'].strip()
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
                ul = soup.find('ul',  'playlink')
                if ul:
                    sub = ul.find_all('a', href=lambda x: x and "/v/" in x)
                    for item in sub:
                        host_url = 'https://www.516ys.com'+item['href']
                        title = titleSub+'_'+item.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': '516ys',
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
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("516ys 크롤링 시작")
    for item in ['21', '3']:
        startCrawling(item)
        
    print("516ys 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
