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

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    token = ''
    with requests.Session() as s:
        login_req = s.post('http://www.filekok.com/ajax_controller.php', data=Page)
        soup = bs(login_req.text, 'html.parser')
        text = str(soup)
        token = text.split('{"result":"')[1].split('","')[0]

    LOGIN_INFO = {
        'browser': 'pc',
        'isSSL': 'Y',
        'mb_id': 'up0001',
        'mb_pw': 'up0001',
        'repage': 'reload',
        'token': token,
        'url': '/main/module/loginClass.php',
        'url_ssl': 'https://ssl.filekok.com/loginClass.php'
    }
    with requests.Session() as s:
        login_req = s.post('https://ssl.filekok.com/loginClass.php', data=LOGIN_INFO)
        i = 0;check = True
        link = "http://www.filekok.com/main/storage.php?" + site + "liststate=&list_count=&search_sort=&p="
        while check:
            i = i+1
            if i == 4:
                break
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            tr = soup.find('table', 'table_list').find('tbody').find_all('tr')

            try:
                for item in tr:
                    adult = item.find_all('td')[1]['onclick'].split("','")[1].split("')")[0]
                    if adult == '1':
                        continue
                    cnt_num = item.find('input', 'list_check')['value']
                    url = "http://www.filekok.com/main/popup.php?doc=bbsInfo&idx="+cnt_num

                    post_one  = s.post(url)
                    soup = bs(post_one.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('title').text.strip().split('파일콕 > 다운로드 > ')[1]
                    title_null = titleNull(title)
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

                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

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

                    conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn2.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("filekok 크롤링 시작")
    site = ['','search_type=MOV&','search_type=DRA&','search_type=MED&','search_type=ANI&']
    for s in site:
        startCrawling(s)
    print("filekok 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
