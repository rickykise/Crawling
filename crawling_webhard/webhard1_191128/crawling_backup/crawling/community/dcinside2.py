import requests,re
import pymysql,time,datetime
import pyautogui
import urllib.parse
from commonFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : ",key)
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    for i in range(1,6):
        try:
            link = "http://search.dcinside.com/post/p/"+str(i)+"/q/"+key
            driver = webdriver.Chrome("c:\python36\driver\chromedriver")
            driver.get(link)
            driver.set_window_position(0, 0)
            driver.set_window_size(1080, 1000)
            time.sleep(2)
            html = driver.find_element_by_class_name("search-result-right").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            all = soup.find("div",{"class","search-list-group"})
            searchDIV = all.find_all("div",{"class","thumb_txt"})

            for item in searchDIV:
                conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item.find('a','lnk_tit').text.strip()
                href = item.find('a','lnk_tit')['href']
                board_number = href.split("&no=")[1]
                timech = item.find('span', 'date').text.strip()
                datetime.datetime.strptime(timech, "%Y.%m.%d %H:%M").strftime('%Y.%m.%d %H:%M')
                timecheck = datetime.datetime.strptime(timech, "%Y.%m.%d %H:%M").strftime('%Y-%m-%d')

                driver.get(href)
                if href.find("dcinside") != -1:
                    pyautogui.hotkey('ctrl', '-')
                    time.sleep(2)
                    pyautogui.typewrite(['right', 'right'])
                time.sleep(2)
                page_main = driver.find_element_by_id("dgn_content_de").get_attribute('innerHTML')
                tags = BeautifulSoup(page_main,'html.parser')
                writer = tags.find('span', 'user_nick_nm').text
                ip = tags.find('li', 'li_ip').text
                print(ip)
        except:
            pass
        finally:
            driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("dcinside 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '아이유':
            startCrawling(k)
        # startCrawling(k)
    print("dcinside 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
