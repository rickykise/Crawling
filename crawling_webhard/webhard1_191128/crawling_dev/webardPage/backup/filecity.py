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
    soup = BeautifulSoup(c.decode('euc-kr','replace'),"html.parser")
    cnt_chk = 0

    title = soup.find('li', 'name01').text.strip()
    cnt_price = soup.find('span', 'txt_bold01').text.strip().split("P")[0].replace(",","")
    cnt_writer = soup.find('span', 'f_left').text.strip()
    cnt_fname = soup.find('div', 'list').text.strip()
    if soup.find('img', 'jehyu'):
        cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_price': cnt_price,
        'Cnt_writer' : cnt_writer,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0; a = 1;check = True
    link = "http://renew.filecity.co.kr/module/contents_search_sphinx2.php?tab="+site+"&pn=0&view=list&limit=&not_view=0&sale=0&sale2=0&pn="
    while check:
        # # 페이지 0부터 시작
        if i == 3:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        i = i+1

        try:
            for item in text:
                if a == 21:
                    a = 1
                cnt_num = text.split('"idx":"')[a].split('","')[0]
                adult = text.split('"adult_chk":"')[a].split('","')[0]
                cnt_vol = text.split('"size":"')[a].split('","')[0]
                url = "http://renew.filecity.co.kr/contents/view.html?idx="+cnt_num
                a = a+1
                if adult == "1":
                    continue
                resultData = getContents(url)
                title_null = titleNull(resultData['Cnt_title'])
                # 키워드 체크
                getKey = getKeyword(conn,curs)
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    dbResult = insertDB('filecity',resultData['Cnt_title'],title_null,url)
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    dbResult = insertDB('filecity',resultData['Cnt_title'],title_null,url)
                    continue

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filecity',
                    'Cnt_title': resultData['Cnt_title'],
                    'Cnt_title_null': title_null,
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : resultData['Cnt_writer'],
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : resultData['Cnt_fname'],
                    'Cnt_chk': resultData['Cnt_chk']
                }
                # print(data)

                conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                try:
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    insertDB('filecity',resultData['Cnt_title'],title_null,url)
                except Exception as e:
                    print(e)
                    pass
                finally :
                    conn2.close()
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("filecity 크롤링 시작")
    site = ['BD_MV','BD_DM','BD_UC','BD_AN']
    for s in site:
        startCrawling(s)
    print("filecity 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
