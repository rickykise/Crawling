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


    title = soup.find('div', 'file_title').find('span').text.strip()
    cnt_fname = soup.find('td', 'td_tit').text.strip()

    if soup.find('td', 'td_tit').find('img'):
        aaa = soup.find('td', 'td_tit').find('img')['src']
        if aaa.find('icon_alli') != -1:
            cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.mfile.co.kr/storage.php?section="+site+"&nPage="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id('ContentsList').get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break
            try:
                for item in tr:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if item.find('td', 'subject').find('a').find('img'):
                        img = item.find('td', 'subject').find('a').find_all('img')
                        if len(img) == 1:
                            if item.find('td', 'subject').find('a').find_all('img')[0]['src'].find('adult') != -1:
                                continue
                        elif len(img) == 2:
                            if item.find('td', 'subject').find('a').find_all('img')[1]['src'].find('adult') != -1:
                                continue
                    # title = item.find('td', 'subject').find('span').text.strip()
                    cnt_price = item.find('td', 'point_l').text.strip().split(" P")[0].replace(",","")
                    cnt_vol = item.find('td', 'byte').text.strip()
                    cnt_writer = item.find('td', 'nicname').find('span').text.strip()
                    cnt_num = item.find('td', 'subject').find('a')['onclick'].split("winBbsInfo('")[1].split("','")[0]
                    url = 'http://www.mfile.co.kr/storage.php?act=view&idx='+cnt_num+'&search_sort=undefined'
                    resultData = getContents(url)

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'mfile',
                        'Cnt_title': resultData['Cnt_title'],
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : resultData['Cnt_fname'],
                        'Cnt_regdate' : now,
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
    # except:
    #     pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("mfile 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("mfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
