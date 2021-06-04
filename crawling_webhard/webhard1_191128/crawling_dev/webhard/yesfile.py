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

    title = soup.find('div', 'title').text.strip()
    cnt_fname = soup.find('li', 'li_filename')['title']
    if soup.find('div', 'td_point').find('img'):
        img = soup.find('div', 'td_point').find('img')['title']
        if img.find('제휴') != -1:
            cnt_chk = 1

    data = {
        'Cnt_title' : title,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    site2 = site.split("&")[0]
    link = "https://www.yesfile.com/board/list.php?code="+site+"#"+site2+"&"
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id("cList").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            div = soup.find_all("div", "list_row")
            if len(div) < 2:
                check = False
                print("게시물없음\n========================")
                break
            try:
                for item in div:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cnt_vol = item.find('li', 'byte').text.strip()
                    cnt_price = item.find('li', 'payprice').text.strip().split("P")[0].replace(",","")
                    cnt_writer = item.find('li', 'name').text.strip()
                    url = "http://www.yesfile.com"+item.find('li', 'c_title').find('a')['href']
                    cnt_num = url.split("&idx=")[1].split("&code")[0]
                    resultData = getContents(url)

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'yesfile',
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

    print("yesfile 크롤링 시작")
    site = ['_BD&sec=0','BD_MV&sec=1','BD_DM&sec=2','BD_UC&sec=3','BD_AN&sec=5']
    for s in site:
        startCrawling(s)
    print("yesfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
