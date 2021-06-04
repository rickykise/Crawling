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

Safe = {
    'safe': 'on'
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://www.filemaru.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def startCrawling(key):
    print(key)
    with requests.Session() as s:
        safe_req = s.post('http://www.filemaru.com/proInclude/ajax/safezonePrc.php', data=Safe, headers=headers)
        i = 30;check = True
        link = "http://www.filemaru.com/?doc=list_sub&cate=&subCate=&sort=&listCnt=25&adtChk=&searchType=all&section=&searchVal="+key+"&searchCate=&p="
        while check:
            i = i+1
            print('페이지: ',i)
            if i == 50:
                break
            try:
                r = s.get(link+str(i), headers=headers)
                soup = bs(r.text, 'html.parser')
                table = soup.find('table', 'sbase_list')
                tr = table.find("tbody").find_all("tr", "choiceViewTr")
                print(len(tr))
                # if len(tr) < 2:
                #     print('게시물없음')
                #     break


                for item in tr:
                    cnt_num = item.find('input')['idx']
                    url = 'http://www.filemaru.com/proInclude/ajax/view.php'
                    url2 = "http://www.filemaru.com/proInclude/ajax/view.php?idx="+cnt_num
                    Page = {
                        'idx': cnt_num
                    }
                    post_one  = s.post(url, data=Page, headers=headers)
                    soup = bs(post_one.text, 'html.parser')
                    text = str(soup)
                    cnt_chk = 0

                    title = text.split('fileTitle" : "')[1].split('"')[0]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('filemaru',title,title_null,url2)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('filemaru',title,title_null,url2)
                        continue
                    # checkPrice = str(keyCheck['p'])
                    cnt_price = text.split('filePoint" : "')[1].split('"')[0].replace(",","")
                    cnt_writer = text.split('fileRegNick" : "')[1].split('"')[0]
                    cnt_vol = text.split('fileSize" : "')[1].split('"')[0]
                    cnt_fname = text.split('fileName" : "')[1].split('"')[0]
                    if text.find('files') != -1:
                        cnt_fname = text.split('fileName" : "')[2].split('"')[0]
                    # cnt_chk = text.split('fileTitle" : "')[1].split('"')[0]

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filemaru',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url2,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("filemaru 크롤링 시작")
    site = ['1박2일', '슈퍼맨이 돌아왔다', '인간극장', '개그콘서트', '99억의 여자', '우아한 모녀', '사랑은 뷰티풀 인생은 원더풀']
    for s in site:
        startCrawling(s)
    print("filemaru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
