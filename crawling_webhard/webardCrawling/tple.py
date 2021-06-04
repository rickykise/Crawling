import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

LOGIN_INFO = {
    'backUrl': 'http%3A//www.tple.co.kr/indexNew.php',
    'flagSecret': '1',
    'loginTarget': 'i',
    'siteDomain': 'tple.co.kr',
    'userid': 'up0002',
    'userpw': 'up0002'
}

def startCrawling(site):
    with requests.Session() as s:
        login_req = s.post('https://www.tple.co.kr/_renew/memberShip.php?todo=execLogin', data=LOGIN_INFO)
        headers = {'Cookie': 'PHPSESSID=efglmlf1uh5h69c5068n2e5nn5; CA=MTU0NTc5NjQxMQ%3D%3D; SC=dHBsZS5jby5rcg%3D%3D; specialbonus_event_sub=1; layerPopClose=1; listcnt=100; autopayEventFlag=1; loginUserId=up0001; loginAdult=0; LK=90b9fd9caff980e0c5dc869b8c2b21eea04eca22; specialbonus_event=1'}

        i = 0;check = True
        link = "http://www.tple.co.kr/_renew/storage.php?code="+site+"&searchTopCode=4"
        while check:
            i = i+1
            if i == 2:
                check=False;break
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find_all('tr', id=re.compile("trList+"))

            try:
                for item in tr:
                    cnt_num = item['id'].split("trList")[1]
                    adult = item.find('a')['href'].split(cnt_num+',')[1].split(',')[0].strip()
                    if adult == '1':
                        continue
                    url = 'http://www.tple.co.kr/storage/index.php?todo=view&source=W&idx='+cnt_num
                    cnt_writer = item.find('span', 'tooltip')['alt']
                    title = item.find('a')['title']
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('tple',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('tple',title,title_null,url)
                        continue

                    Page = {
                        'idx': cnt_num,
                        'source': 'W',
                        'todo': 'viewFile'
                    }
                    url2 = 'http://www.tple.co.kr/storage/index.php'

                    cnt_chk = 0
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
                    if tags2.find('td', 'textLeft').find('img'):
                        cnt_chk = 1
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
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("tple 크롤링 시작")
    site = ['0','1','2','4']
    for s in site:
        startCrawling(s)
    print("tple 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
