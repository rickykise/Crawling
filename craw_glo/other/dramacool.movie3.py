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
    link = 'https://www3.dramacool.movie/most-popular-drama?page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'list-episode-item').find_all('li')

        try:
            for item in li:
                imgUrl = item.find('img')['data-original']
                url = 'https://www3.dramacool.movie' + item.find('a')['href']
                titleSub = item.find('a')['title']
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
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
                li = soup.find('ul', 'all-episode').find_all('li')

                for item in li:
                    host_url = 'https://www3.dramacool.movie' + item.find('a')['href']
                    if host_url.find('episode') == -1:
                        continue
                    title = item.find('h3', 'title').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'dramacool.movie3',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dramacool.movie3 크롤링 시작")
    startCrawling()
    print("dramacool.movie3 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
