import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import pyautogui
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from checkFun import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

cnt_osp = 'megafile'

def main():
    check = True
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    link = 'http://www.megafile.co.kr/webhard/list.php?category=1&pagesize=20'
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get('http://www.megafile.co.kr/user/login.php')
        time.sleep(2)
        driver.find_element_by_id('loginid').send_keys('up0001')
        driver.find_element_by_id('passwd').send_keys('up0001')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="body"]/form/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td[3]/input').click()
        time.sleep(2)
        driver.get(link)
        time.sleep(2)

        url = 'http://www.megafile.co.kr/webhard/view.php?WriteNum=18272855&id=15272855&fv='
        cnt_num = url.split('WriteNum=')[1].split('&')[0]
        sub_num = url.split('id=')[1].split('&')[0]
        time.sleep(2)
        id = "OpenViewWindow2_new("+sub_num+' , '+cnt_num+",'')"
        driver.execute_script(id)
        if len(driver.window_handles) == 2:
            print(len(driver.window_handles))
            driver.switch_to.window(driver.window_handles[-1])
            try:
                # alert창 체크
                WebDriverWait(driver, 1).until(EC.alert_is_present())
                alert = driver.switch_to.alert()
                alert.accept()
                print('alert창이 있어 건너뜁니다.')
                cnt_chk = 2
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)
                return
            except TimeoutException:
                print('alert창이 없습니다.')
                pass

            html = driver.find_element_by_class_name("wrap").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            print(soup)
            text = str(soup)
            table = soup.find_all('table')[6]
            cnt_chk = 0

            cnt_price = table.find_all('td')[1].text.replace(",","").split('캐시')[0].strip()
            if text.find('제휴업체로부터') != -1:
                cnt_chk = 1

            print(cnt_price)
            print(cnt_chk)
    # except:
    #     pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    print("megafile check 크롤링 시작")
    main()
    print("megafile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
