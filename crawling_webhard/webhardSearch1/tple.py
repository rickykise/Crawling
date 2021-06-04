import requests,re
import pymysql,time,datetime
import urllib.parse
import pyautogui
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

LOGIN_INFO = {
    'userid': 'up0001',
    'userpw': 'up0001',
    'backupr': 'Lw==',
    'todo': 'login_exec'
}

def startCrawling(key):
    print(key)
    encText = key.encode('euc-kr')
    encText = urllib.parse.quote(encText)
    with requests.Session() as s:
        login_req = s.post('https://www.tple.co.kr/login/', data=LOGIN_INFO)
        headers = {'Cookie': 'PHPSESSID=efglmlf1uh5h69c5068n2e5nn5; CA=MTU0NTc5NjQxMQ%3D%3D; SC=dHBsZS5jby5rcg%3D%3D; specialbonus_event_sub=1; layerPopClose=1; listcnt=100; autopayEventFlag=1; loginUserId=up0001; loginAdult=0; LK=90b9fd9caff980e0c5dc869b8c2b21eea04eca22; specialbonus_event=1'}

        i = 0;check = True
        link = 'http://www.tple.co.kr/storage/?s=&d=180719&code=&listScale=&searchTopCode=&searchTopField=title&searchTopValue='+encText+'&subSearch='
        while check:
            i = i+1
            if i == 2:
                break
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            table = soup.find('table', 'storageListTable')
            if table == None:
                continue
            td = table.find_all('td', 'txtLeft')
            try:
                for item in td:
                    cnt_num = item.find('a')['href'].split(", '")[1].split("'")[0]
                    url = 'http://www.tple.co.kr/storage/index.php?todo=view&source=W&idx='+cnt_num

                    post_one  = s.get(url)
                    tags = bs(post_one.text, 'html.parser')
                    cnt_chk = 0

                    title = tags.find('div', 'infoTitle').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('tple',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('tple',title,title_null,url)
                    #     continue
                    cnt_writer = tags.find('span', id='memberLayerMenu'+cnt_num).text.strip()
                    if tags.find('div', 'noticeArea'):
                        text = tags.find('div', 'noticeArea').text.strip()
                        if text.find('제휴업체') != -1:
                            cnt_chk = 1

                    Page = {
                        'idx': cnt_num,
                        'source': 'W',
                        'todo': 'viewFile'
                    }
                    url2 = 'http://www.tple.co.kr/storage/index.php'

                    post_two  = s.post(url2, data=Page)
                    tags2 = bs(post_two.text, 'html.parser')
                    returnValue = []

                    td = tags2.find_all('td', 'textRight')
                    for item in td:
                        price = item.text.strip()
                        if price.find('P') != -1:
                            cnt_price = int(price.split("P")[0].replace(",",""))
                            returnValue.append(cnt_price)
                    for i in range(int(int(len(td)) / 2)-1):
                        cnt_price = returnValue[i]+cnt_price
                    cnt_vol = tags2.find_all('td', 'textRight')[1].text.strip()
                    fname = tags2.find('td', 'textLeft').find('span')['alt']
                    format1 = tags2.find('td', 'textLeft').find('span').text.strip()
                    if format1 == '':
                        fname = tags2.find_all('td', 'textLeft')[1].find('span')['alt']
                        format1 = tags2.find_all('td', 'textLeft')[1].find('span').text.strip()
                        format2 = tags2.find_all('td', 'textLeft')[1].text.strip().split(format1)[1]
                    else:
                        format2 = tags2.find('td', 'textLeft').text.strip().split(format1)[1]
                    fname = fname+format2

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'tple',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("tple 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("tple 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
