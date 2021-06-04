import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True
    link = "http://www.filecast.co.kr/www/contents/page_contents_list/"+site+"/0/"
    link2 = "?select_order=is_non_adult"
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find_all('tr')
        try:
            for item in tr:
                if item.find('a'):
                    cnt_num = item.find('a')['onclick'].split("View(")[1].split(",this")[0]
                    url = 'http://filecast.co.kr/www/contents/view/'+cnt_num
                    urlSub = 'http://www.filecast.co.kr/www/contents/view/'+cnt_num+'/1/'
                    cnt_chk = 0
                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")

                    title = soup.find('span', 'txt').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('filecast',title,urlSub)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('filecast',title,urlSubs)
                        continue
                    cnt_price = soup.find('span', 'txt_blue txt_block').find('b').text.replace(",","").strip()
                    cnt_writer = soup.find('a', 'btn_memo')['onclick'].split("('")[1].split("')")[0]
                    cnt_vol = soup.find('li', 'l4').find('span', 'txt_block').text.replace(" ","").strip()
                    cnt_fname = soup.find('span', 'file_name').text.strip()
                    ico = soup.find('span', 'ico_partner')['class']
                    if ico[1] == 'on':
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filecast',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': urlSub,
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

    print("filecast 크롤링 시작")
    site = ['1','2','3']
    for s in site:
        startCrawling(s)
    print("filecast 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
