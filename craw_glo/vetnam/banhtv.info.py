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
    link = 'http://banhtv.info/quoc-gia/kr/trang-{}.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'last-film-box').find_all('li')

        try:
            for item in li:
                url = item.find('a',{'class':['movie-item','m-block']})['href']
                titleSub = item.find('a',{'class':['movie-item','m-block']})['title']
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
                host_url = soup.find('div', 'movie-l-img').find('a','btn-red')['href']

                r = requests.get(host_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('ul', 'list-episode').find_all('li')

                for item in sub:
                    host_url = item.find('a','btn-episode')['href']
                    title = titleSub + '_' + item.find('a','btn-episode')['title'].strip()
                    title_null = titleNull(title)
                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'banhtv.info',
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
        except:
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("banhtv.info 크롤링 시작")
    startCrawling()
    print("banhtv.info 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
