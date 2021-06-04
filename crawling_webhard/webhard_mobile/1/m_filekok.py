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

Page = {
    'act': 'get_token'
}
Cookie = {
    'check_cookie_skidSafeFlag': 'Y'
}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://www.filekok.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def startCrawling(site):
    i = 0;check = True
    token = ''
    with requests.Session() as s:
        login_req = s.post('http://m.filekok.com/ajax_controller.php', data=Page, headers=headers)
        soup = bs(login_req.text, 'html.parser')
        text = str(soup)
        token = text.split('"result":"')[1].split('","')[0]

    LOGIN_INFO = {
        'browser': 'm',
        'isSSL': 'Y',
        'mb_id': 'up0001',
        'mb_pw': 'up0001',
        'repage': 'reload',
        'token': token,
        'url': '/main/module/loginClass.php',
        'url_ssl': 'https://ssl.filekok.com/loginClass.php'
    }
    with requests.Session() as s:
        login_req = s.post('https://ssl.filekok.com/loginClass.php', data=LOGIN_INFO, headers=headers)
        while check:
            i = i+1
            if i == 4:
                break
            link = "http://m.filekok.com/storage.php?act=list&mSec="+site+"&sSec=all&Search=&SearchKey=&Limit=20&s_nickname=&copyrsalechk=&Page="+str(i)+"&tSec=#Topsubtitle"
            post_one  = s.post(link, cookies=Cookie, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            table = soup.find('div',  id='list_contents').find_all('table')

            try:
                for item in table:
                    cnt_num = item.find_all('td')[1]['onclick'].split("('")[1].split("',")[0]
                    url = 'http://m.filekok.com/storage.php?act=view&idx='+cnt_num+'&mSec='+site+'&sSec=all'
                    url2 = "http://www.filekok.com/main/popup.php?doc=bbsInfo&idx="+cnt_num

                    post_two  = s.post(url2, headers=headers)
                    soup = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('title').text.strip().split('파일콕 > 다운로드 > ')[1]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    # checkPrice = str(keyCheck['p'])
                    cnt_vol = soup.find_all('td', 'txt')[4].text.replace("\n","").replace("\t","").replace(" ","").strip().split(" / ")[0]
                    cnt_writer = soup.find_all('td', 'txt')[5].find('span').text.strip()
                    cnt_fname = soup.find('td', colspan='4').find_all('span', 'fl')[1]['title']
                    if soup.find('table', 'pop_detail'):
                        cnt_fname = soup.find('table', 'pop_detail').find('tbody').find('tr')['title']
                    cnt_price = soup.find_all('td', 'txt')[4].text.replace("\n","").replace("\t","").replace(" ","").replace(",","").strip().split(" / ")[1].split("P")[0]
                    if soup.find('font', color='#77777'):
                        cnt_price = soup.find('b', class_=False).text.strip().replace(",","").split("P")[0]
                    if soup.find_all('td', 'txt')[4].find('img'):
                        jehu = soup.find_all('td', 'txt')[4].find('img')['alt']
                        if jehu == '제휴컨텐츠':
                            cnt_chk= 1
                    # if checkPrice == cnt_price:
                    #     cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filekok',
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

    print("m_filekok 크롤링 시작")
    site = ['all','MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_filekok 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
