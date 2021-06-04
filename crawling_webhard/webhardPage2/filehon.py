import requests,re
import pymysql,time,datetime
import urllib.parse
import pyautogui
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
    'sReturnUri': 'http%3A%2F%2Ffilehon.com%2F',
    'x': '22',
    'y': '25'
}

def startCrawling(site):
    with requests.Session() as s:
        login_req = s.post('http://filehon.com/member/loginCheck.php', data=LOGIN_INFO)
        soup = bs(login_req.text, 'html.parser')
        i = 0;check = True
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
                    fname = soup.find('div', 'fileList').find('li').find('span', 'capacity').text.strip()
                    cnt_fname = soup.find('div', 'fileList').find('li').text.strip().split(fname)[0]
                    table = soup.find('table', 'ctnVtbl').find_all('td')[3]
                    cnt_writer = soup.find('a', 'user_info').text.strip()
                    cnt_price = table.find('span', 'price').text.strip().replace(",","")
                    if table.find('img'):
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filehon',
                        'Cnt_title': title,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
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

    print("filehon 크롤링 시작")
    site = ['','category1=MVO','category1=DRA','category1=MED','category1=ANI']
    for s in site:
        startCrawling(s)
    print("filehon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
