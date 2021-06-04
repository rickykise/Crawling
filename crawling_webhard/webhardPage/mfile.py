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
    cnt_price = soup.find('span', id='chkPacket').text.replace(",","").strip()
    cnt_writer = soup.find('font', 'name_s').text.strip()
    cnt_vol = soup.find('span', id='chkSize').text.replace(",","").strip()
    cnt_fname = soup.find('td', 'td_tit').text.strip()

    if soup.find('td', 'td_tit').find('img'):
        aaa = soup.find('td', 'td_tit').find('img')['src']
        if aaa.find('icon_alli') != -1:
            cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_price': cnt_price,
        'Cnt_writer' : cnt_writer,
        'Cnt_vol' : cnt_vol,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.mfile.co.kr/storage.php?section="+site+"&liststate=&nPage="
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        a = soup.find_all('a', href='#storage_view')
        try:
            for item in a:
                cnt_num = item['onclick'].split("winBbsInfo('")[1].split("','")[0]
                url = 'http://www.mfile.co.kr/storage.php?act=view&idx='+cnt_num+'&search_sort=undefined'
                img = item.find_all('img')
                if len(img) == 1:
                    if item.find_all('img')[0]['src'].find('adult') != -1:
                        continue
                elif len(img) == 2:
                    if item.find_all('img')[1]['src'].find('adult') != -1:
                        continue
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'mfile',
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

    print("mfile 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("mfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
