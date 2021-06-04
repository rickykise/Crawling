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
    'Origin': 'http://www.filekok.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True
    with requests.Session() as s:
        Data = {
            'act': 'get_token'
        }
        token_req = s.post('http://www.filelon.com/ajax_controller.php', data=Data, headers=headers)
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
        login_req = s.post('https://ssl.filelon.com/loginClass.php', data=LOGIN_INFO, headers=headers)
        while check:
            i = i+1
            if i == 4:
                break
            link = "http://www.filelon.com/main/storage.php?" + site + "liststate=&list_count=&search_sort=&p="
            post_one  = s.get(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            table = soup.find('table', 'table_list')
            tr = table.find('tbody').find_all("tr")
            try:
                for item in tr:
                    adult = item.find('td', 'tit')['onclick'].split("','")[1].split("')")[0]
                    if adult == '1':
                        continue
                    cnt_writer = item.find_all('td', 'kor')[1].find('span').text.strip()
                    cnt_num = item.find('input', 'list_check')['value']
                    url = 'http://www.filelon.com/main/popup.php?doc=bbsInfo&idx=' + cnt_num

                    post_two  = s.get(url, headers=headers)
                    soup2 = bs(post_two.text, 'html.parser')
                    table = soup2.find_all('table', 'pop_base')[1]
                    table2 = soup2.find('table', 'pop_detail').find('tbody')
                    cnt_chk = 0

                    title = soup2.find('title').text.strip().split("다운로드 > ")[1]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('filelon',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('filelon',title,title_null,url)
                        continue
                    cnt_price = table.find('td', 'txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("/")[1].split("P")[0]
                    if soup2.find('b', class_=None):
                        cnt_price = soup2.find('b', class_=None).text.strip().replace(",", "").split("P")[0]
                    cnt_vol = table.find('td', 'txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip().split("/")[0]
                    cnt_fname = table2.find('tr')['title']
                    if table.find('td', 'txt').find('span', 'ic_alliance'):
                        jehu = table.find('td', 'txt').find('span', 'ic_alliance').text.strip()
                        if jehu == '제휴':
                            cnt_chk = 1

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

                    conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                        insertDB('filelon',title,title_null,url)
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn2.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("filelon 크롤링 시작")
    site = ['','search_type=MOV&','search_type=DRA&','search_type=MED&','search_type=ANI&']
    for s in site:
        startCrawling(s)
    print("filelon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
