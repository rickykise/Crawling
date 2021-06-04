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

cnt_osp = 'wedisk'

def main():
    check = True
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    link = 'http://www.wedisk.co.kr/wediskNew/Home/contentsList.do?data=%7B%22searchType%22%3A%221%22%2C%22category%22%3A%2200%22%2C%22subCategory%22%3A%22%22%2C%22subKey%22%3A%22%22%2C%22searchArea%22%3A%2221%22%2C%22searchKeyword%22%3A%22%22%2C%22pageViewRowNumber%22%3A%2220%22%2C%22selectCategory%22%3A%2200%22%2C%22selectSubCategory%22%3A%22%22%2C%22pageViewPoint%22%3A%221%22%2C%22oldSearchOption%22%3A%22%22%2C%22sort%22%3A%220%22%2C%22chkMbc%22%3A%22%22%2C%22SubCategory%22%3A%22%22%2C%22keyword%22%3A%22%22%7D'
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get('https://www.wedisk.co.kr/common/html/member/loginForm.html?20180719')
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        driver.find_element_by_id('uid').send_keys('llim9898')
        driver.find_element_by_id('upw').send_keys('55085508lim')
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/form/input').click()
        time.sleep(2)
        driver.get(link)

        url = 'http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID=27799550'
        cnt_num = url.split('contentsID=')[1]
        id = "openDnWin("+cnt_num+",'N');"
        try:
            driver.execute_script(id)
            time.sleep(2)
            if len(driver.window_handles) == 2:
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)
                html = driver.find_element_by_class_name("register_top_area").get_attribute('innerHTML')
                soup = BeautifulSoup(html,'html.parser')

                cnt_price = soup.find('span', 'price').text.replace(',', '').split('캐시')[0].strip()
                table = soup.find('table').find('tbody')
                td = table.find_all('tr')[1].find_all('div')[1]['class']
                if len(td) == 1:
                    cnt_chk = 1
                else:
                    cnt_chk = 0
        except:
            pyautogui.hotkey('enter')
            print('에러')
            time.sleep(2)
            cnt_chk = 2
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)
        # dbUpdate(checkNum,cnt_chk,url)
        print(cnt_chk)
        print(cnt_price)
    except:
        pass
    finally:
        driver.close()
if __name__=='__main__':
    start_time = time.time()

    print("wedisk check 크롤링 시작")
    main()
    print("wedisk check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
