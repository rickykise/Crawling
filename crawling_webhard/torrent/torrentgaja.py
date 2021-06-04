import requests,re
import pymysql,time,datetime
import urllib.parse
from webhardFun import *
from urllib.parse import unquote
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Host': 'torrentgaja.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            link = "https://torrentgaja.com/bbs/board.php?bo_table="+site+"&page="+str(i)
            post_one  = s.get(link, headers=headers)
            content = post_one.content
            soup = bs(content.decode('utf8','replace'), 'html.parser')
            try:
                if site == 'movie_kor' or site == 'animovie':
                    div = soup.find('div', 'list-webzine').find_all('div', 'list-media')
                    for item in div:
                        title = item.find('div', 'media-body').find('a').text.strip()
                        if item.find('div', 'media-body').find('span'):
                            spanText = item.find('div', 'media-body').find('span').text.strip()
                            title = title.split(spanText)[1].strip()
                        title_null = titleNull(title)
                        # # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_null, getKey)
                        if keyCheck['m'] == None:
                            continue
                        keyCheck2 = checkTitle2(title_null, getKey)
                        if keyCheck2['m'] == None:
                            continue
                        cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')
                        url = item.find('div', 'media-body').find('a')['href']
                        if url.find('page') != -1:
                            url = url.split('&page')[0]

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'tabomtorrent',
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
                elif site == 'past_movie':
                    div = soup.find('div', 'list-board').find_all('li', 'list-item')
                    for item in div:
                        title = item.find('div', 'wr-subject').find('a').text.strip()
                        if item.find('div', 'wr-subject').find('a'):
                            spanText = item.find('div', 'wr-subject').find('span').text.strip()
                            if spanText != '':
                                title = title.split(spanText)[1].strip()
                        title_null = titleNull(title)
                        # # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_null, getKey)
                        if keyCheck['m'] == None:
                            continue
                        keyCheck2 = checkTitle2(title_null, getKey)
                        if keyCheck2['m'] == None:
                            continue
                        cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')
                        url = item.find('div', 'wr-subject').find('a')['href']
                        if url.find('page') != -1:
                            url = url.split('&page')[0]

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'torrentgaja',
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
                    tr = soup.find('div', 'list-wrap').find('tbody').find_all('tr')
                    for item in tr:
                        title = item.find('td', 'list-subject').find('a').text.strip()
                        if title.find('접속이 안될경우') != -1:
                            continue
                        if item.find('td', 'list-subject').find('a'):
                            spanText = item.find('td', 'list-subject').find('span').text.strip()
                            if spanText != '':
                                title = title.split(spanText)[1].strip()
                        title_null = titleNull(title)
                        # # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_null, getKey)
                        if keyCheck['m'] == None:
                            continue
                        keyCheck2 = checkTitle2(title_null, getKey)
                        if keyCheck2['m'] == None:
                            continue
                        cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')
                        url = item.find('td', 'list-subject').find('a')['href']
                        if url.find('page') != -1:
                            url = url.split('&page')[0]

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'torrentgaja',
                            'Cnt_title': title,
                            'Cnt_title_null': title_null,
                            'Cnt_url': url,
                            'Cnt_price': '',
                            'Cnt_writer' : '',
                            'Cnt_vol' : '',
                            'Cnt_fname' : '',
                            'Cnt_chk': 0
                        }
                        print(data)
                        print('=============================================')

                        # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("torrentgaja 크롤링 시작")
    site = ['movie_kor','animovie','past_movie','tv_docu','tv_drama','tv_ent','animation']
    for s in site:
        startCrawling(s)
    print("torrentgaja 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
