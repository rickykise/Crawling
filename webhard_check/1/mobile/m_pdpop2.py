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

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup)
    cnt_chk = 0;cnt_price = 0;returnValue = []

    ul = str(soup.find('ul', 'dnld_lstcon'))
    li = soup.find('ul', 'dnld_lstcon').find_all('li')

    for item in li:
        if item.find('span', 'packet'):
            cnt_price = int(item.find('span', 'packet').text.strip().replace(',', '').split("P")[0])
        returnValue.append(cnt_price)
    for i in range(len(li)-1):
        cnt_price = returnValue[i]+cnt_price

    title = soup.find('div', 'fspop_title').find('h4').text.strip()
    cnt_writer = soup.find('div', 'fsview_table').find('strong').text.strip()
    cnt_vol = soup.find('strong', id='chkSize').text.strip()
    fname = soup.find('ul', 'dnld_lstcon').find('span', 'sbj')['class']
    if len(fname) == 1:
        cnt_fname = soup.find('ul', 'dnld_lstcon').find_all('span', 'sbj')[0].text.strip()
    else:
        cnt_fname = soup.find('ul', 'dnld_lstcon').find_all('span', 'sbj')[1].text.strip()

    if soup.find('div', 'dnld_lstbtn').find('span', 'cine'):
        span = soup.find('div', 'dnld_lstbtn').find('span', 'cine').text.strip()
        if span.find('제휴콘텐츠') != -1:
            cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_price': cnt_price,
        'Cnt_writer' : cnt_writer,
        'Cnt_vol' : cnt_vol,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;a = 0;check = True
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
            text2 = str(soup).split('"nickname":[')[1].split('],')[0]

            c = '\ud1b0\uacfc\uc81c'
            tes = c.encode("utf-8")

            print(tes)

            # for item in text:
            #     if a == 101:
            #         a = 0
            #         break
            #     if a == 0:
            #         cnt_num = text.split('"')[1].split('","')[0]
            #         cnt_writer = text2.split('"')[1].split('","')[0]
            #     else:
            #         cnt_num = text.split('","')[a].split('","')[0]
            #         cnt_writer = text2.split('","')[a].split('","')[0]
            #     a = a+1
            #     print(urllib.parse.quote(cnt_writer, ''))
                # url = 'http://m.pdpop.com/?doc=board_view&idx='+cnt_num
                #
                # url = 'http://m.pdpop.com/?doc=board_view&idx=136034'
                # print(url)
                # Data = {
                #     'doc': 'board_view',
                #     'idx': cnt_num,
                #     'mPage': ''
                # }
                # post_two  = s.get(url, headers=headers, data=Data)
                # soup = bs(post_two.text, 'html.parser')
                # print(soup)
                #
                # title = soup.find('div', 'ctn_name').text.strip()
                # title_null = titleNull(title)
                # # cnt_price =
                # # cnt_writer
                # # cnt_vol
                # # cnt_fname
                # # cnt_chk
                # # print(title)
                # break
                #
                # data = {
                #     'Cnt_num' : cnt_num,
                #     'Cnt_osp' : 'pdpop',
                #     'Cnt_title': title,
                #     'Cnt_title_null': title_null,
                #     'Cnt_url': url,
                #     'Cnt_price': cnt_price,
                #     'Cnt_writer' : cnt_writer,
                #     'Cnt_vol' : cnt_vol,
                #     'Cnt_fname' : cnt_fname,
                #     'Cnt_chk': cnt_chk
                # }
                # print(data)







            #
            # try:
            #     for item in text:
            #         adult = text.split('"adult":"')[a].split('","')[0]
            #         mobile = text.split('"mobile":"')[a].split('","')[0]
            #         cnt_num = text.split('"no":')[a].split(',')[0]
            #         a = a+1
            #         if a == 51:
            #             a = 1
            #             break
            #         if adult == 'Y':
            #             continue
            #         if mobile == 'N':
            #             continue
            #         url = 'http://bbs.pdpop.com/board_re.php?mode=view&code=F_'+site+'&no='+cnt_num
            #
            #         resultData = getContents(url)
            #         title_null = titleNull(resultData['Cnt_title'])
            #         # 키워드 체크
            #         getKey = getKeyword()
            #         keyCheck = checkTitle(title_null, getKey)
            #         if keyCheck['m'] == None:
            #             continue
            #         keyCheck2 = checkTitle2(title_null, getKey)
            #         if keyCheck2['m'] == None:
            #             continue
            #
            #         data = {
            #             'Cnt_num' : cnt_num,
            #             'Cnt_osp' : 'pdpop',
            #             'Cnt_title': resultData['Cnt_title'],
            #             'Cnt_title_null': title_null,
            #             'Cnt_url': url,
            #             'Cnt_price': resultData['Cnt_price'],
            #             'Cnt_writer' : resultData['Cnt_writer'],
            #             'Cnt_vol' : resultData['Cnt_vol'],
            #             'Cnt_fname' : resultData['Cnt_fname'],
            #             'Cnt_chk': resultData['Cnt_chk']
            #         }
            #         # print(data)
            #
            #         dbResult = insertALL(data)
            # except:
            #     continue

if __name__=='__main__':
    start_time = time.time()

    print("m_pdpop 크롤링 시작")
    # site = ['A001_B001','A001_B007','A001_B003']
    site = ['A001_B001']
    for s in site:
        startCrawling(s)
    print("m_pdpop 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
