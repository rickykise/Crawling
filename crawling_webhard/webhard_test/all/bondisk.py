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
    'mode': 'login_exec',
    'wmode': 'noheader',
    'id': 'up0001',
    'pw': 'up0001',
    'login_backurl': ''
}

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup)
    cnt_chk = 0

    cnt_writer = text.split("target_nick=")[1].split('","')[0]
    title = soup.find('title').text.strip()
    cnt_vol = soup.find('td', 'infotable_td2').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(" ", "").replace(",","").strip().split("/")[1]
    cnt_price = soup.find('td', 'infotable_td2').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(" ", "").replace(",","").strip().split("P")[0]
    cnt_fname = soup.find('td', 'infotable_td3')['title']
    if soup.find('td', 'infotable_list_td1'):
        cnt_fname = soup.find('td', 'infotable_list_td1').text.strip()
    if soup.find('td', 'infotable_td2').find('img'):
        cnt_chkCh = soup.find('td', 'infotable_td2').find('img')['title']
        if cnt_chkCh.find('제휴') != -1:
            cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_fname' : cnt_fname,
        'Cnt_price' : cnt_price,
        'Cnt_writer' : cnt_writer,
        'Cnt_vol' : cnt_vol,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    with requests.Session() as s:
        login_req = s.post('http://m.bondisk.com/member/login.html', data=LOGIN_INFO)
        i = 0;check = True
        while check:
            i = i+1
            if i == 2:
                break
            if site == '':
                link = 'http://bondisk.com/main/doc/storage/list_ajax.php?list_count=100'
            else:
                link = 'http://bondisk.com/main/doc/storage/list_ajax.php?section='+site+'&list_count=100'
            post_one  = s.get(link)
            soup = bs(post_one.text, 'html.parser')
            td = soup.find_all('td', 'storage_title')
            try:
                for item in td:
                    a = item.find('a')['onclick']
                    if a.find('alert') != -1 or a.find('openSanction') != -1:
                        continue
                    cnt_num = a.split("winBbsInfo('")[1].split("','")[0]
                    url = 'http://bondisk.com/main/popup/bbs_info.php?idx='+cnt_num
                    try:
                        resultData = getContents(url)
                    except:
                        continue
                    title_null = titleNull(resultData['Cnt_title'])

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('bondisk',resultData['Cnt_title'],title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('bondisk',resultData['Cnt_title'],title_null,url)
                        continue

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'bondisk',
                        'Cnt_title': resultData['Cnt_title'],
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': resultData['Cnt_price'],
                        'Cnt_writer' : resultData['Cnt_writer'],
                        'Cnt_vol' : resultData['Cnt_vol'],
                        'Cnt_fname' : resultData['Cnt_fname'],
                        'Cnt_chk': resultData['Cnt_chk']
                    }
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("bondisk 크롤링 시작")
    site = ['','MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("bondisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
