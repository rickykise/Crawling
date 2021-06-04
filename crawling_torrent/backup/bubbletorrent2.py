import requests,re
import pymysql,time,datetime
import urllib.parse
from webhardFun import *
from urllib.parse import unquote
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Host': 'bubbletorrent2.site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    link = 'https://bubbletorrent2.site/bbs/board.php?bo_table='+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        try:
            if site == 'mov1':
                div = soup.find_all('div', 'list-row')
                for item in div:
                    title = item.find('div', 'list-desc').find('a').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    url = item.find('a')['href']
                    if url.find('&page=') != -1:
                        url = url.split('&page=')[0].strip()
                    cnt_num = url.split('wr_id=')[1].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'buckstorrent2',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': '',
                        'Cnt_writer' : '',
                        'Cnt_vol' : '',
                        'Cnt_fname' : '',
                        'Cnt_chk': 0
                    }
                    # print(data)
                    # print('=============================================')

                    dbResult = insertALL(data)
            else:
                li = soup.find('div', 'list-board').find('ul', 'list-body').find_all('li')
                for item in li:
                    title = item.find('a', 'item-subject').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    url = item.find('a', 'item-subject')['href']
                    if url.find('&page=') != -1:
                        url = url.split('&page=')[0].strip()
                    cnt_num = url.split('wr_id=')[1].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'bubbletorrent2',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': '',
                        'Cnt_writer' : '',
                        'Cnt_vol' : '',
                        'Cnt_fname' : '',
                        'Cnt_chk': 0
                    }
                    # print(data)
                    # print('=============================================')

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("bubbletorrent2 크롤링 시작")
    site = ['mov1', 'kortv1', 'kortv2', 'animation']
    for s in site:
        startCrawling(s)
    print("bubbletorrent2 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
