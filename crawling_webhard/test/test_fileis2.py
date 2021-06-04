import requests,re
import pymysql,time,datetime
import urllib.parse
import pyautogui
import sys,os
import datetime
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from webhardFun import *

b = 'icestar1'
userId = 'undersd'
userPw = 'undersd1234'
cnt_num = '14258758'

def startCrawling():
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True;
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        driver.get('http://cp.fileis.com/')
        time.sleep(2)
        driver.find_element_by_name('vcID').send_keys(userId)
        driver.find_element_by_name('vcPwd').send_keys(userPw)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="LoginCorner"]/form/table/tbody/tr[1]/td[3]/input').click()
        time.sleep(2)

        driver.get('http://cp.fileis.com/log/purchaseLog.php?aRight=&search=nContentNo&keyword='+cnt_num+'&sDate='+now+'&eDate='+now)
        html = driver.find_element_by_xpath('/html/body/table[2]').get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find_all('tr')
        time.sleep(5)
        if len(tr) != 1:
            for a in range(1,len(tr)+1):
                buyer = soup.find_all('tr')[a].find_all('td')[5].text.strip()
                print(buyer)
                if buyer == b:
                    ACC_Cnt_Title = soup.find_all('tr')[a].find_all('td')[6].text.strip()
                    ACC_pay = soup.find_all('tr')[a].find_all('td')[7].text.strip()
                    ACC_Admin_Date = soup.find_all('tr')[a].find_all('td')[8].text.strip()

                    data = {
                        'ACC_Cnt_Title' : ACC_Cnt_Title,
                        'ACC_pay' : ACC_pay,
                        'ACC_Admin_Date': ACC_Admin_Date,
                        'ACC_Admin_State': '1'
                    }
                    print(data)
                    break
                else:
                    continue
        else:
            ACC_Admin_State = 0
        time.sleep(10)

    # except:
    #     pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    startCrawling()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
