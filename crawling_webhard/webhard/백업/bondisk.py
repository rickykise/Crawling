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

    cnt_price = soup.find('td', 'infotable_td2').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(" ", "").replace(",","").strip().split("P")[0]
    cnt_fname = soup.find('td', 'infotable_td3')['title']
    if soup.find('td', 'infotable_td2').find('img'):
        cnt_chkCh = soup.find('td', 'infotable_td2').find('img')['title']
        if cnt_chkCh.find('제휴') != -1:
            cnt_chk = 1

    data = {
        'Cnt_fname' : cnt_fname,
        'Cnt_price' : cnt_price,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.bondisk.com/main/storage.php?section=" + site + "&pageViewType=bbsType"
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get(link)
    time.sleep(3)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            html = driver.find_element_by_id("listdiv").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find_all('table')[3]
            tr = table.find("tbody").find_all("tr", height="29", bgcolor=False)
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('td', 'storage_title').find('a').find('img'):
                    continue
                title = item.find('td', 'storage_title').find('span')['title']
                cnt_vol = item.find_all('td')[3].text.strip()
                cnt_writer = item.find_all('td')[5].text.strip()
                cnt_num = item.find('td', 'storage_title').find('a')['onclick'].split("winBbsInfo('")[1].split("','")[0]
                url = 'http://www.bondisk.com/main/popup/bbs_info.php?idx='+cnt_num
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'bondisk',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
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

            driver.find_element_by_xpath('//*[@id="q_right_arrow"]').click()
            time.sleep(2)

    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("bondisk 크롤링 시작")
    site = ['','MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("bondisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
