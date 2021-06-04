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

def startCrawling(site):
    i = 0; b = 1;check = True
    while check:
        i = i+1
        if i == 4:
            break
        link = "https://torrentwal.com/"+site+"/torrent"+str(i)+".htm"
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find('table', 'board_list').find_all('tr')
        try:
            for item in tr:
                title = item.find('a').text.strip()
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue
                # cnt_num = item.find('a')['href'].split('torrent_movie/')[1].split('.html')[0]
                cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')
                url = 'https://torrentwal.com'+item.find('a')['href'].split('..')[1]

                # r = requests.get(url)
                # c = r.content
                # soup = BeautifulSoup(c,"html.parser")
                # div2 = soup.find('div', id='writeContents')
                # text = str(div2)
                # if text.find('Info Hash') == -1:
                #     continue
                # div = soup.find('div', id='main_body')
                #
                # title = div.find_all('div')[1].text.strip()
                # title_null = titleNull(title)
                # cnt_vol = text.split('파일크기: ')[1].split('<li>')[0].replace(' ', '').strip()
                # cnt_fname = text.split('Info Hash: ')[1].split('<li>')[0].replace(' ', '').strip()

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'torrentwal',
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

    print("torrentwal 크롤링 시작")
    site = ['torrent_movie','torrent_variety','torrent_tv','torrent_ani']
    for s in site:
        startCrawling(s)
    print("torrentwal 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
