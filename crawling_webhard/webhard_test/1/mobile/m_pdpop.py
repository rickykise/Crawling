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

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Content-Length': '88',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'pdpopnet=0; connect_log=Y; _ga=GA1.2.1597594914.1553564520; _gid=GA1.2.1381734089.1553564520; _gat=1; cookie_id=up0001; age=45; auth=1; adult=1; uid=24412936; id=up0001%40pdpop.com; name=%EC%84%9C%EB%AF%BC%EC%8A%B9; clubsex=2; nickname=up0001; ero_birth=751031; ero_sex=2; domain=pdpop.com; PDPOP=LGbkAwc7pmb0BvWxLKEyVwgmBwL6VeaZipKQhlV7pmbmBvW1nJDvB3Z6BQbvZwD0ZGV5ZmLvB3Z6ZwbvnJDvB3Z6ZGL6VaIjZQNjZHOjMUOipP5wo20vB3Z6AwbvpTSmp3qxVwgmBwL0BvWyLmpmZQLkLwywZwt1ZQR1ZGZ5MzL3AQDmZGV0A2L4BTD1ZTSvZTEuAQyvZQp4AmDlZGHjBGZkBJR5AwIxAmuwVwgmBwD6Vz5uoJHvB3Z6BGbv7VFp66%2B87Vd5VwgmBwt6Vz5cL2ghLJ1yVwgmBwL6VaIjZQNjZFV7pmb1BvWfMKMyoPV7pmbkBvV5VwgmBwL6VzufMKMyoPV7pmblBvVjZFV7pmb1BvWvnKW0nPV7pmbkZQbvZGx3AF0kZP0mZFV7pmbmBvWuM2HvB2x6AQH7pmb1BvWuMUIfqPV7nGbkB3Z6AQbvLKI0nPV7nGbkB3Z6Zmbvp2I4VwgcBwV7pmb1BvWyoJScoPV7pmblZGbvpKqypwRlZmENpKqypwRlZmDhL29gVwgmBwL6VzEioJScovV7pmb5BvWjMUOipP5wo20vB3Z6ZGZ6VaOlo2McoTIsnJ1uM2HvB047sD%3D%3D; PHPSESSID=auuho4fi50um40trrf8h7equ60; changepay_notice=Y',
    'Host': 'm.pdpop.com',
    'Referer': 'http://m.pdpop.com',
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
    'X-Requested-With': 'XMLHttpRequest'
}

def getContents(url, Data):
    with requests.Session() as s:
        post_two  = s.get(url, headers=headers, data=Data)
        soup = bs(post_two.text, 'html.parser')
        text = str(soup)
        div = soup.find('div', 'list').find_all('input')
        cnt_chk = 0;cnt_price = 0;returnValue = []

        if text.find('본 자료에는 제휴 컨텐츠') != -1:
            cnt_chk = 1
        title = soup.find('div', 'ctn_name').text.strip()
        title_null = titleNull(title)
        for item in div:
            if cnt_chk == 1:
                cnt_price = int(item['packet'])
            else:
                cnt_price = int(item['packet1'])
            returnValue.append(cnt_price)
        for i in range(len(div)-1):
            cnt_price = returnValue[i]+cnt_price
        cnt_fname = soup.find('div', 'filelist_text').text.strip()

        data = {
            'Cnt_title': title,
            'Cnt_title_null': title_null,
            'Cnt_price': cnt_price,
            'Cnt_writer' : '',
            'Cnt_vol' : '',
            'Cnt_fname' : cnt_fname,
            'Cnt_chk': cnt_chk
        }
        # print(data)
        return data

def startCrawling(site):
    i = 0;a = 2;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 2:
                break
            Page = {
                'cate1': site,
                'cate2': '',
                'cName': 'boardData',
                'mode': 'list',
                'rows': '100',
                'stitle': '',
                'tList': 'default',
                'userid': ''
            }
            link = 'http://m.pdpop.com/_module/board.enroll.php'
            post_one  = s.post(link, headers=headers, data=Page)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup).split('"idx":[')[1].split('],')[0]
            # try:
            for item in text:
                if a == 101:
                    a = 0
                    break
                if a == 0:
                    cnt_num = text.split('"')[1].split('","')[0]
                else:
                    cnt_num = text.split('","')[a].split('","')[0]
                a = a+1
                url = 'http://m.pdpop.com/?doc=board_view&idx='+cnt_num+'&mPage=1'

                Data = {
                    'doc': 'board_view',
                    'idx': cnt_num,
                    'mPage': '1'
                }
                resultData = getContents(url, Data)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(resultData['Cnt_title_null'], getKey)
                if keyCheck['m'] == None:
                    continue
                keyCheck2 = checkTitle2(resultData['Cnt_title_null'], getKey)
                if keyCheck2['m'] == None:
                    continue

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'pdpop',
                    'Cnt_title': resultData['Cnt_title'],
                    'Cnt_title_null': resultData['Cnt_title_null'],
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : resultData['Cnt_writer'],
                    'Cnt_vol' : resultData['Cnt_vol'],
                    'Cnt_fname' : resultData['Cnt_fname'],
                    'Cnt_chk': resultData['Cnt_chk']
                }
                # print(data)

                dbResult = insertALL(data)
            # except:
            #     continue

if __name__=='__main__':
    start_time = time.time()

    print("m_pdpop 크롤링 시작")
    site = ['A001_B001','A001_B007','A001_B003']
    for s in site:
        startCrawling(s)
    print("m_pdpop 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
