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
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'PHPSESSID=3ce0qltrtsjsp7dgs5dlu8raf0; check_cookie_skidSafeFlag=Y; _ga=GA1.2.535339707.1552614974; _gid=GA1.2.1236219188.1552614974; dspbase=; dsptarget=; type_chk=N',
    'Host': 'm.filelon.com',
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
}

pcHeaders = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://www.filelon.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}


def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        Data = {
            'act': 'get_token'
        }
        token_req = s.post('http://www.filelon.com/ajax_controller.php', data=Data, headers=pcHeaders)
        soup = bs(token_req.text, 'html.parser')
        token = str(soup).split('"result":"')[1].split('","')[0]

        LOGIN_INFO = {
            'browser': 'pc',
            'isSSL': 'Y',
            'mb_id': 'up0001',
            'mb_pw': 'up0001',
            'repage': 'reload',
            'token': token,
            'url': '/main/module/loginClass.php',
            'url_ssl': 'https://ssl.filelon.com/loginClass.php'
        }
        login_req = s.post('https://ssl.filelon.com/loginClass.php', data=LOGIN_INFO, headers=pcHeaders)
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.filelon.com/storage.php?act=list&mSec='+site+'&sSec=all&Search=&SearchKey=&Limit=20&s_nickname=&copyrsalechk=&Page='+str(i)
            post_one  = s.get(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find('table', 'tb_list01').find_all('tr')
            try:
                for item in tr:
                    cnt_num = item['onclick'].split("('")[1].split("',")[0]
                    url = 'http://m.filelon.com/storage.php?act=view&idx='+cnt_num
                    url2 = 'http://www.filelon.com/main/popup.php?doc=bbsInfo&idx='+cnt_num

                    post_two  = s.get(url2, headers=pcHeaders)
                    soup2 = bs(post_two.text, 'html.parser')
                    table = soup2.find_all('table', 'pop_base')[1]
                    table2 = soup2.find('table', 'pop_detail').find('tbody')
                    cnt_chk = 0

                    title = soup2.find('title').text.strip().split("다운로드 > ")[1]
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
                    cnt_writer = soup2.find('span', style="cursor:pointer;").text.strip()
                    cnt_price = table.find('td', 'txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("/")[1].split("P")[0]

                    if table.find('span', 'price_arrow'):
                        cnt_price = soup2.find_all('b', class_=None)[2].text.strip().replace(",", "").split("P")[0]
                    cnt_vol = table.find('td', 'txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip().split("/")[0]
                    cnt_fname = table2.find('tr')['title']
                    if table.find('td', 'txt').find('span', 'ic_alliance'):
                        jehu = table.find('td', 'txt').find('span', 'ic_alliance').text.strip()
                        if jehu == '제휴':
                            cnt_chk = 1
                    # if checkPrice == cnt_price:
                    #     cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filelon',
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

    print("m_filelon 크롤링 시작")
    site = ['all','MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_filelon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
