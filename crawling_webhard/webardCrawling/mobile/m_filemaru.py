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
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://m.filemaru.com',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'viewContents=16747737; ch-veil-id=76952a55-ffad-4b56-b22d-8493e05dbc70; ch-session-37430=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiIzNzQzMC02MDQ1YjE1ZTc3YWM5YjY0NmU2ZCIsImlhdCI6MTYxNTE4MDEzMywiZXhwIjoxNjE3NzcyMTMzfQ.1HtpypF1HcSg0rmg-7VCP_5QSBIUSRg6fGJ_7Z1yn0Y; m_grade=1; loginVer=60; upid=1993412; mid=0719i619a7193a19f6198719b619c719j6195919d919h919e9190a191719971927199719; nick=do.2; Usr=dkdl1748%40naver.com; ungrade=0; adult=0; total_cash=1920; cmn_cash=1880; bns_cash=40; coupon=0; memo_cnt=0; LogChk=Y; PHPSESSID=dbrohfn9rgip2sh9efg0jba2t5; G_ENABLED_IDPS=google',
    'Host': 'm.filemaru.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

headers2 = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'ko-KR',
    'Cache-Control' : 'no-cache',
    'Connection' : 'Keep-Alive',
    'Cookie': 'PHPSESSID=79p4oijitdr2tsnpkko5lnvbd3; G_ENABLED_IDPS=google; ch-veil-id=76952a55-ffad-4b56-b22d-8493e05dbc70; ch-session-37430=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiIzNzQzMC02MDQ1YWU0ZjUzNDkxNTE2ODhkYSIsImlhdCI6MTYxNTE3OTM0MywiZXhwIjoxNjE3NzcxMzQzfQ.tjOwff9ZpVOR3fMYSjT-0TORI7N_mC3bpR17nWm1B_o; m_grade=1; loginVer=60; upid=1993412; mid=0719i619a7193a19f6198719b619c719j6195919d919h919e9190a191719971927199719; nick=do.2; Usr=dkdl1748%40naver.com; ungrade=0; adult=1; total_cash=1920; cmn_cash=1880; bns_cash=40; coupon=0; memo_cnt=0; LogChk=Y',
    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host' : 'www.filemaru.com',
    'Referer' : 'http://www.filemaru.com/',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'X-Requested-With': 'XMLHttpRequest'
}

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            Data = {
                'adtChk': '0'
            }
            adult = s.post('https://m.filemaru.com/proInclude/ajax/adtCtl.php', headers=headers, data=Data)
            i = i+1
            if i == 4:
                break
            link = "https://m.filemaru.com/proInclude/scroll/infScroll.php?doc=submenu_cate&mSec="+site+"&sSec=&p="+str(i)+"&sort=&searchVal=&searchType=&searchChk="
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find_all('li', 'list_box ctrView')
            try:
                for item in li:
                    cnt_num = item.find('a')['idx']
                    url = 'https://m.filemaru.com/proInclude/ajax/view.php'
                    url2 = "https://m.filemaru.com/proInclude/ajax/view.php"+cnt_num
                    Page = {
                        'idx': cnt_num
                    }
                    post_one  = s.post(url, headers=headers, data=Page)
                    soup = bs(post_one.text, 'html.parser')
                    text = str(soup)
                    cnt_chk = 0

                    title = text.split('fileTitle" : "')[1].split('"')[0]
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    cnt_vol = text.split('fileSize" : "')[1].split('"')[0]
                    cnt_writer = text.split('fileRegNick" : "')[1].split('"')[0]
                    cnt_fname = text.split('fileName" : "')[1].split('"')[0]
                    if text.find('files') != -1:
                        cnt_fname = text.split('fileName" : "')[2].split('"')[0]
                    cnt_price = text.split('filePoint" : "')[1].split('"')[0].replace(",","")

                    jehuUrl = 'https://www.filemaru.com/proInclude/ajax/view.php'
                    Page = {
                        'ci': '79p4oijitdr2tsnpkko5lnvbd3',
                        'idx': cnt_num
                    }
                    post_two  = s.post(jehuUrl, data=Page, headers=headers2)
                    soup2 = bs(post_two.text, 'html.parser')
                    text2 = str(soup2)
                    jehu = text2.split('fileAllianceChk" : "')[1].split('"')[0]
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

    print("m_filemaru 크롤링 시작")
    site = ['DRA','MED','MOV','ANI']
    for s in site:
        startCrawling(s)
    print("m_filemaru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
