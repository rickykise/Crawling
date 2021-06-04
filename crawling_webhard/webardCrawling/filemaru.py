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

# 'm_id': 'dkdl1748@naver.com'
# 'm_pwd': 'ehgml65112'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'ko-KR',
    'Cache-Control' : 'no-cache',
    'Connection' : 'Keep-Alive',
    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=5pbjkp436dk47skjr7k0uj2is6; G_ENABLED_IDPS=google; viewContents=16761163; ch-veil-id=897f282e-9b1a-4f18-b8ef-1fd0b2622d55; ch-session-37430=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiIzNzQzMC02MDM2ZjQwOTQ1MTQzMDk4MTI1YSIsImlhdCI6MTYxNTUyOTE3MywiZXhwIjoxNjE4MTIxMTczfQ.4ZmQd_ROXnP_co9I0WC5me01ybu4o9RIaBtCXhFFSj0; m_grade=1; loginVer=60; upid=1993412; mid=0719i619a7193a19f6198719b619c719j6195919d919h919e9190a191719971927199719; nick=do.2; Usr=dkdl1748%40naver.com; ungrade=0; adult=1; total_cash=1940; cmn_cash=1880; bns_cash=60; coupon=0; memo_cnt=0; LogChk=Y; searchHistory=%5B%5B%227ZWY7Jqw7Iqk%22%2C%2203.12%22%2C%22DRA%22%2Cnull%2C%227ZWY7Jqw7Iqk%22%5D%2C%5B%227Y6c7YSw7ZWY7Jqw7Iqk%22%2C%2203.12%22%2C%22DRA%22%2Cnull%2C%227Y6c7YSw7ZWY7Jqw7Iqk%22%5D%2C%5B%227Yys7YSw%22%2C%2203.12%22%2C%22DRA%22%2Cnull%2C%227Yys7YSw%22%5D%5D',
    'Host' : 'www.filemaru.com',
    'Referer' : 'https://www.filemaru.com/',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'X-Requested-With': 'XMLHttpRequest'
}

headers_log = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'ko-KR',
    'Cache-Control' : 'no-cache',
    'Connection' : 'Keep-Alive',
    'Cookie': 'viewContents=16761163; ch-veil-id=897f282e-9b1a-4f18-b8ef-1fd0b2622d55; ch-session-37430=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiIzNzQzMC02MDRiMDQ2MmVjZjU4MGRhZjU5NiIsImlhdCI6MTYxNTUyOTA1OCwiZXhwIjoxNjE4MTIxMDU4fQ.ZPC2BniWM5fLwTVnInb-hOFNSnW_hV6LAD_aEhTc6Gw; cross-site-cookie=name',
    'Host' : 'ssl.filemaru.com',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    with requests.Session() as s:
        # safe_req = s.post('http://www.filemaru.com/proInclude/ajax/safezonePrc.php', data=Safe, headers=headers)
        login_req = s.get('https://ssl.filemaru.com/loginPrcMaru.php?callback=loginChkCall&email=dkdl1748@naver.com&key=ZWhnbWw2NTExMg==&log_save=&log_safe=&sns_chk=&sess=5pbjkp436dk47skjr7k0uj2is6&platType=p&_=1615529070994', headers=headers_log)
        i = 0;check = True
        link = "https://www.filemaru.com/?doc=list_sub&cate="+site+"&subCate=&sort=&listCnt=25&adtChk=&searchType=&searchVal=&p="
        while check:
            i = i+1
            if i == 4:
                break
            r = s.get(link+str(i), headers=headers)
            soup = bs(r.text, 'html.parser')
            table = soup.find('table', 'sbase_list')
            tr = table.find("tbody").find_all("tr", "choiceViewTr")

            try:
                for item in tr:
                    cnt_num = item.find('input')['idx']
                    url = 'https://www.filemaru.com/proInclude/ajax/view.php'
                    url2 = "https://www.filemaru.com/proInclude/ajax/view.php?idx="+cnt_num

                    Page = {
                        'ci': '5pbjkp436dk47skjr7k0uj2is6',
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

                    cnt_price = text.split('filePoint" : "')[1].split('"')[0].replace(",","")
                    cnt_writer = text.split('fileRegNick" : "')[1].split('"')[0]
                    cnt_vol = text.split('fileSize" : "')[1].split('"')[0]
                    cnt_fname = text.split('fileName" : "')[1].split('"')[0]
                    if text.find('files') != -1:
                        cnt_fname = text.split('fileName" : "')[2].split('"')[0]
                    jehu = text.split('fileAllianceChk" : "')[1].split('"')[0]
                    if jehu == "Y":
                        cnt_chk = 1

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
    site = ['DRA','MED','MOV','','ANI']
    for s in site:
        startCrawling(s)
    print("filemaru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
