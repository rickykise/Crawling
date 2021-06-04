import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    cnt_chk = 0

    title = soup.find('title').text.strip().split("- ")[1]
    cnt_price = soup.find('div', 'td_point').find('li', 'text').text.replace(" ","").replace(",","").strip().split("P")[0]
    cnt_vol = soup.find('div', 'td_point').find('li', 'text').text.replace(" ","").strip().split("P/")[1]
    cnt_writer = soup.find('div', 'td_num').find('span').text.strip()
    cnt_fname = soup.find('li', 'li_filename')['title']
    if soup.find('div', 'td_point').find('img'):
        img = soup.find('div', 'td_point').find('img')['title']
        if img.find('제휴') != -1:
            cnt_chk = 1

    data = {
        'Cnt_title' : title,
        'Cnt_price': cnt_price,
        'Cnt_writer' : cnt_writer,
        'Cnt_vol' : cnt_vol,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;start = 0;a = 1;check = True
    link = "http://www.yesfile.com/ajax/ajax_list.php?code="+site+"&page="
    link2 = "&start="
    link3 = "&list_scale=20"
    while check:
        i = i+1
        if i == 4:
            break
        start = start+1
        startnum = (start-1) * 20
        # print(link+str(i)+link2+str(startnum)+link3)
        r = requests.get(link+str(i)+link2+str(startnum)+link3)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        try:
            for item in text:
                if a == 21:
                    a = 1
                cnt_num = text.split('"idx":"')[a].split('","')[0]
                adult = text.split('"adult":"')[a].split('","')[0]
                code = text.split('"catecode":"')[a].split('","')[0]
                url = "http://www.yesfile.com/board/board_view.php?pg_mode=view_popup&idx="+cnt_num+"&code="+code
                a = a+1
                if adult == "Y":
                    continue
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'yesfile',
                    'Cnt_title': resultData['Cnt_title'],
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : resultData['Cnt_writer'],
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

    print("yesfile 크롤링 시작")
    site = ['_BD&sec=0','BD_MV&sec=1','BD_DM&sec=2','BD_UC&sec=3','BD_AN&sec=5']
    for s in site:
        startCrawling(s)
    print("yesfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
