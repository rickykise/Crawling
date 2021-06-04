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
    i = 0;check = True
    link = "http://www.filecast.co.kr/www/contents/#!/"+site+"/0/"
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            if i == 1:
                driver.find_element_by_xpath('//*[@id="leftContents"]/div[1]/ul[1]/li[4]').click()
                time.sleep(2)
            html = driver.find_element_by_id("contentsListTbody").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break
            try:
                for item in tr:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    title = item.find('span', 'fc-contents-list-tit').text.strip()
                    cnt_price = item.find('div', 'three').text.strip().split("P")[0].replace(",","")
                    cnt_vol = item.find('div', 'two').text.strip()
                    cnt_writer = item.find('em', 'nickname').text.strip()
                    cnt_num = item.find('a', 'view_link')['href'].split("/view/")[1].split("/category/")[0]
                    url = "http://www.filecast.co.kr" + item.find('a', 'view_link')['href']

                    driver.get(url)
                    time.sleep(3)
                    htmll = driver.find_element_by_id('nonClickViewWrap').get_attribute('innerHTML')
                    tags = BeautifulSoup(htmll,'html.parser')
                    cnt_chk = 0

                    cnt_fname = tags.find('span', 'file_name').text.strip()
                    if tags.find('span', 'ico_partner on'):
                        cnt_chkCh = tags.find('span', 'ico_partner on').text.strip()
                        if cnt_chkCh.find('제휴') != -1:
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filecast',
                        'Cnt_title': title,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_regdate' : now,
                        'Cnt_chk': cnt_chk
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

    print("filecast 크롤링 시작")
    site = ['1','2','3']
    for s in site:
        startCrawling(s)
    print("filecast 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
