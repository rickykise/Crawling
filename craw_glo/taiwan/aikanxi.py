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
    link = 'https://aikanxi.org/kr/'
    r = requests.get(link)
    r.encoding = r.apparent_encoding
    c = r.text
    soup = BeautifulSoup(c,"html.parser")
    # 게시물 URL 크롤링
    sub = soup.find('ul','drama_rich').find_all('a',{'rel' : ['nofollow','noopener','noreferrer'],'onclick': lambda x: x and "xxx(" in x})
    cnts = []
    for item in sub:
        urlArr = item['onclick'].replace('xxx(','').replace('\'','').split(',')
        url = 'https://aikanxi.org/'+urlArr[0]+'/all.html'
        cnts.append(url)
    # 게시물 URL 중복제거
    cntSet = set(cnts)
    cntList = list(cntSet)

    for url in cntList:
        try:
            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            titleSub = soup.find('div',id='contain').find('h1').text.strip().replace(' 線上看','')
            title_check = titleNull(titleSub)

            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_check, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']

            playList = soup.find('div','items').find_all('a',{'rel' : ['nofollow','noopener','noreferrer'],'onclick': lambda x: x and "xxx(" in x})
            for item in playList:
                urlArr = item['onclick'].replace('xxx(','').replace('\'','').split(',')
                host_url = 'https://aikanxi.org/'+urlArr[0]+'/'+urlArr[1]+'.html'

                title = item.text.strip()
                title_null = titleNull(title)
                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'aikanxi',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'taiwan',
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

    print("aikanxi 크롤링 시작")
    startCrawling()
    print("aikanxi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
