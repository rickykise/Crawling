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
    'Frame_login': 'Ok',
    'idSave': '1',
    'm_id': 'up0001',
    'm_pwd': 'up0001',
    'sReturnUri': 'http%3A%2F%2Ffilehon.com%2F'
}

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        login_req = s.post('http://filehon.com/member/loginCheck.php', data=LOGIN_INFO)
        soup = bs(login_req.text, 'html.parser')
        link = "http://filehon.com/contents/index.php?"+site+"&show_type=0&adult_del_check=Y&cp_del_check=N&rows=50&page="
        while check:
            i = i+1
            if i == 4:
                break
            post_one  = s.get(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find('table', 'bbslist3').find("tbody").find_all("tr", class_=None)
            try:
                for item in tr:
                    cnt_vol = item.find_all('td', 'smfont')[2].text.strip()
                    cnt_num = item.find('input')['value']
                    url = "http://filehon.com/contents/view.php?idx="+cnt_num
                    post_two  = s.get(url)
                    soup = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('h1').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('filehon',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('filehon',title,title_null,url)
                        continue
                    fname = soup.find('div', 'fileList').find('li').find('span', 'capacity').text.strip()
                    cnt_fname = soup.find('div', 'fileList').find('li').text.strip().split(fname)[0]
                    table = soup.find('table', id='js-note').find_all('td')[4]
                    cnt_writer = soup.find('a', 'user_info').text.strip()
                    cnt_price = soup.find('span', 'price').text.strip().replace(",","")
                    if table.find('img'):
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filehon',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("filehon 크롤링 시작")
    site = ['','category1=MVO','category1=DRA','category1=MED','category1=ANI']
    for s in site:
        startCrawling(s)
    print("filehon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
