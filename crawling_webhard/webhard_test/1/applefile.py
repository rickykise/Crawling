import requests,re
import pymysql,time,datetime
import urllib.parse
import os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    cnt_chk = 0

    cnt_fname = soup.find('div', 'filelist').find('li', 'li_filename').text.strip()
    if soup.find('li', 'icon').find('img'):
        cnt_chkCh = soup.find('li', 'icon').find('img')['title']
        if cnt_chkCh.find('제휴') != -1:
            cnt_chk = 1
    # print('=======================')

    data = {
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "https://applefile.com/contents/?category1="+site+"&category2=&show_type=0&rows=20&page="
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        table = soup.find('table', 'boardtype1')
        tr = table.find("tbody").find_all("tr")
        if len(tr) < 2:
            check = False
            print("게시물없음\n========================")
            break
        # try:
        for item in tr:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            title = item.find('td', 'title').find('a')['title']
            title_null = titleNull(title)
            url = 'http://applefile.com'+item.find('td', 'title').find('a')['href']
            cnt_num = url.split("idx=")[1]

            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle('여자의 비밀', getKey)
            if keyCheck['m'] == None:
                # dbResult = insertDB('applefile',title,title_null,url)
                continue
            print(keyCheck)
            # keyCheck2 = checkTitle2(title_null, getKey)
            # if keyCheck2['m'] == None:
            #     dbResult = insertDB('applefile',title,title_null,url)
            #     continue

            cnt_vol = item.find_all('td', 'da1')[1].text.strip()
            cnt_price = item.find_all('td', 'da1')[2].text.strip().split("P")[0].replace(",","")
            cnt_writer = item.find_all('td', 'da2')[1].find('a').text.strip()
            resultData = getContents(url)

            data = {
                'Cnt_num' : cnt_num, #게시물 번호
                'Cnt_osp' : 'applefile', #사이트
                'Cnt_title': title, #제목
                'Cnt_title_null': title_null,
                'Cnt_url': url, #url
                'Cnt_price': cnt_price, #가격
                'Cnt_writer' : cnt_writer, #작성
                'Cnt_vol' : cnt_vol, #용량
                'Cnt_fname' : resultData['Cnt_fname'], #파일명
                'Cnt_regdate' : now, #등록일
                'Cnt_chk': resultData['Cnt_chk']
            }
            print(data)
            print('================================')
            # checkCntNum = getSearchCheckNum(data['Cnt_osp'])
            # cntCheck = checkCheckNum(cnt_num, checkCntNum)
            # print(cntCheck)
            # if cntCheck == None:
                # dbResult = insertALL(data)

        # except:
        #     continue

if __name__=='__main__':
    start_time = time.time()

    print("applefile 크롤링 시작")
    site = ['','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("applefile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
