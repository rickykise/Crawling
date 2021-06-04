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

    cnt_price = soup.find('span', 'b_price').text.strip().split("P")[0].replace(",","")
    cnt_vol = soup.find('span', 'f_tahoma11').text.strip().replace("/ ","")
    cnt_writer = soup.find('span', 'name_s').text.strip()
    cnt_fname = soup.find('td', 'td_tit').text.strip()
    if soup.find_all('td', 'point_vol')[2].find('img'):
        img = soup.find_all('td', 'point_vol')[2].find('img')['src']
        if img.find('ico_jehu2') != -1:
            cnt_chk = 1

    data = {
        'Cnt_price': cnt_price,
        'Cnt_vol': cnt_vol,
        'Cnt_writer': cnt_writer,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }

    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://sedisk.com/storage.php?section=" + site + '&nLimit=100'
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get(link)
    time.sleep(3)
    try:
        while check:
            i = i+1
            if i == 2:
                break
            html = driver.find_element_by_id("contentList_Table").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                adultLen = item.find('span', 'txt').find_all('img')
                if len(adultLen) != 1:
                    adult = item.find('span', 'txt').find_all('img')[1]['src']
                    if adult.find('ico_19_03') != -1:
                        continue
                endDay = item.find('td', 'c_title').find('a')['onclick']
                if endDay.find('만료되었습니다') != -1:
                    continue
                title = item.find('span', 'txt-over').find('font').text.strip()
                cnt_num = item['data-idx']
                url = 'http://sedisk.com/storage.php?act=view&idx=' + cnt_num
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'sedisk',
                    'Cnt_title': title,
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
                    # pass
                finally :
                    conn.close()
    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("sedisk 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("sedisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
