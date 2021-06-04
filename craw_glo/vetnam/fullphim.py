import requests
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
import ssl
import urllib3
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://www.fullphim.net/the-loai/phim-bo?d5307828_page='
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        block = soup.find_all('a', 'item-block-title')
        try:
            for item in block:
                url = 'https://www.fullphim.net'+item['href']
                titleSub = item.text.strip()
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
                url2 = 'https://www.fullphim.net'+soup.find('a', 'button_xemphim')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div','collection-item')

                for item in div:
                    host_url = 'https://www.fullphim.net'+item.find('a')['href']
                    titleNum = item.find('a').text.strip()
                    title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'fullphim',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
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

    print("fullphim 크롤링 시작")
    startCrawling()
    print("fullphim 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
