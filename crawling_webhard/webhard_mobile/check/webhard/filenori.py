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

cnt_osp = 'filenori'

def main(getUrl):
    check = True
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    link = 'http://www.filenori.com/noriNew/Contents/contentsList.do?data=%7B%22searchType%22%3A%221%22%2C%22etcSearchType%22%3A%22%22%2C%22category%22%3A%2200%22%2C%22subCategory%22%3A%22%22%2C%22subOption%22%3A%22%22%2C%22searchCategory%22%3A%2202%22%2C%22searchSubCategory%22%3A%22%22%2C%22searchArea%22%3A%2221%22%2C%22searchKeyword%22%3A%22%22%2C%22searchSort%22%3A%225%22%2C%22pageViewRow%22%3A%2220%22%2C%22pageViewPoint%22%3A%221%22%2C%22pageTotal%22%3A%2297000%22%2C%22pageBaseID%22%3A%2268117031%22%7D'
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get('https://www.filenori.com/common/html/member/loginForm.html?20181005')
        time.sleep(2)
        print('새로고침중.../')
        driver.refresh()
        time.sleep(2)
        driver.find_element_by_id('userID').send_keys('up555')
        driver.find_element_by_id('userPW').send_keys('djq5555555')
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div/form/ul/li[2]/input').click()
        time.sleep(2)
        driver.get(link)
        for url, checkNum in getUrl.items():
            checkNum = '3' if checkNum[0] == '0' else '2'
            checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
            if now >= checkDate:
                cnt_num = url.split('contentsID=')[1]
                id = "contentsList_View(true, "+cnt_num+",'N');"
                try:
                    driver.execute_script(id)
                    time.sleep(2)
                    if len(driver.window_handles) == 2:
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(2)
                        html = driver.find_element_by_id("body_view").get_attribute('innerHTML')
                        soup = BeautifulSoup(html,'html.parser')
                        cnt_chk = 0

                        if soup.find('div', 'cooperateIcon'):
                            cnt_chk = 1
                    else:
                        continue
                except:
                    pyautogui.hotkey('enter')
                    print('에러')
                    time.sleep(2)
                    cnt_chk = 2
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)
                dbUpdate(checkNum,cnt_chk,url)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("filenori check 크롤링 시작")
    main(getUrl)
    print("filenori check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
