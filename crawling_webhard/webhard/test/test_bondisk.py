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
    cnt_chk = 0

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
        'Cnt_vol' : cnt_vol,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def getWriter(url2):
    with requests.Session() as s:
        login_req = s.post('http://m.bondisk.com/member/login.html', data=LOGIN_INFO)
        # print(login_req.status_code)
        if login_req.status_code != 200:
            raise Exception('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요.')
        # print(LOGIN_INFO)

    r = requests.get(url2)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    cnt_writer = soup.find_all('li', 'info_a')[2].text.strip()

    return cnt_writer

def startCrawling(site):
    with requests.Session() as s:
        login_req = s.post('http://m.bondisk.com/member/login.html', data=LOGIN_INFO)
        # print(login_req.status_code)
        if login_req.status_code != 200:
            raise Exception('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요.')
        # print(LOGIN_INFO)

        i = 0;check = True
        while check:
            i = i+1
            if i == 4:
                break
            Page = {
                'mode': 'contents_list_sphinx',
                'page': i,
                'cate1': site,
                'cate2': '',
                'keyword': '',
                'slist': '20'
            }
            post_one  = s.post("http://m.bondisk.com/ajax/ajax.php", data=Page)
            soup = bs(post_one.text, 'html.parser')
            idx = soup.find_all('idx')
            try:
                for item in idx:
                    cnt_num = item.text.strip()
                    url = 'http://bondisk.com/main/popup/bbs_info.php?idx='+cnt_num
                    url2 = 'http://m.bondisk.com/board/board_view.html?idx='+cnt_num
                    cnt_writer  = getWriter(url2)
                    resultData = getContents(url)

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'bondisk',
                        'Cnt_title': resultData['Cnt_title'],
                        'Cnt_url': url,
                        'Cnt_price': resultData['Cnt_price'],
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : resultData['Cnt_vol'],
                        'Cnt_fname' : resultData['Cnt_fname'],
                        'Cnt_chk': resultData['Cnt_chk']
                    }
                    # print(data)

                conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                except Exception as e:
                    print(e)
                    pass
                finally :
                    conn.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("bondisk 크롤링 시작")
    site = ['','2','3','4','5']
    for s in site:
        startCrawling(s)
    print("bondisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
