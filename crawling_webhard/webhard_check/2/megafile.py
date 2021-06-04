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

cnt_osp = 'megafile'

def main(getUrl):
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
        for url, checkNum in getUrl.items():
            checkNum = '3' if checkNum[0] == '0' else '2'
            checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
            if now >= checkDate:
                cnt_num = url.split('WriteNum=')[1].split('&')[0]
                sub_num = url.split('id=')[1].split('&')[0]
                time.sleep(2)
                id = "OpenViewWindow2_new("+sub_num+' , '+cnt_num+",'')"
                driver.execute_script(id)
                if len(driver.window_handles) == 2:
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(3)
                    pyautogui.hotkey('enter')
                    try:
                        html = driver.find_element_by_class_name("wrap").get_attribute('innerHTML')
                        soup = BeautifulSoup(html,'html.parser')
                        text = str(soup)
                        cnt_chk = 0

                        if text.find('제휴업체로부터') != -1:
                            cnt_chk = 1
                    except:
                        print('삭제')
                        time.sleep(2)
                        cnt_chk = 2
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(2)
                else:
                    continue
                dbUpdate(checkNum,cnt_chk,url)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("megafile check 크롤링 시작")
    main(getUrl)
    print("megafile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
