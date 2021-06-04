import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

# ==================불법 업체==================

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    cnt_price = soup.find('span', 'b_price').text.strip().split("P")[0].replace(",","")
    cnt_writer = soup.find('table', 'file_detail').find_all('tr')[0].find_all('td', 'point_vol')[1].text.strip()
    cnt_fname = soup.find('td', 'file_f').text.strip()
    # print(cnt_writer)

    data = {
        'Cnt_price': cnt_price,
        'Cnt_writer' : cnt_writer,
        'Cnt_fname' : cnt_fname
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.jdisk.com/board?section="+site+"&nLimit=20"
    print(link)
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get(link)
    time.sleep(3)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            html = driver.find_element_by_id("contentList_Table").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                titlesub = item.find('td', 'c_title').find('a').find('span', 'txt').find_all('img')
                if len(titlesub) == 2:
                    continue
                title = item.find('td', 'c_title').find('a').find('span', 'txt').text.strip()
                cnt_num = item['data-idx']
                url = "http://www.jdisk.com/board.php?act=bbs_info&idx="+cnt_num
                cnt_vol = item.find_all('td', 'c_data')[1].text.strip()
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'jdisk',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : resultData['Cnt_writer'],
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : resultData['Cnt_fname'],
                    'Cnt_regdate' : now,
                    'Cnt_chk': '0'
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

            driver.find_element_by_xpath('//*[@id="pn_r"]').click()
            time.sleep(2)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("jdisk 크롤링 시작")
    site = ['ALL','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    # startCrawling()
    print("jdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
