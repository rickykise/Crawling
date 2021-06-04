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
    link = 'https://www.phimoxy.com/quoc-gia/han-quoc'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    li = soup.find_all('li', 'item-phim')
    for item in li:
        try:
            url = item.find('a')['href']
            titleSub = item.find('div', 'post-title').find('p').text.strip()
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
            url2 = 'https://www.phimoxy.com'+soup.find('a',  'btn-see btn btn-danger')['href']
            
            r = requests.get(url2)
            c = r.content
            soup = BeautifulSoup(c, "html.parser")
            sub = soup.find_all('a', 'page larger')
            sub.insert(0, {'href':url2, 'title':'Tập 1'})

            for item in sub:
                host_url = item['href']
                title = titleSub+'_'+item['title'].strip()
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp': 'phimoxy',
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

    print("phimoxy 크롤링 시작")
    startCrawling()
    print("phimoxy 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
