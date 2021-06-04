import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from checkFun import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException

def main():
    check = True
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    link = 'http://www.wedisk.co.kr/wediskNew/Home/contentsList.do?data=%7B%22searchType%22%3A%221%22%2C%22category%22%3A%2200%22%2C%22subCategory%22%3A%22%22%2C%22subKey%22%3A%22%22%2C%22searchArea%22%3A%2221%22%2C%22searchKeyword%22%3A%22%22%2C%22pageViewRowNumber%22%3A%2220%22%2C%22selectCategory%22%3A%2200%22%2C%22selectSubCategory%22%3A%22%22%2C%22pageViewPoint%22%3A%221%22%2C%22oldSearchOption%22%3A%22%22%2C%22sort%22%3A%220%22%2C%22chkMbc%22%3A%22%22%2C%22SubCategory%22%3A%22%22%2C%22keyword%22%3A%22%22%7D'
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
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

        url = 'http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID=54654564'

        cnt_num = url.split('contentsID=')[1]
        id = "openDnWin("+cnt_num+",'N');"

        driver.execute_script(id)
        # time.sleep(2)
        len(driver.window_handles)


        if len(driver.window_handles) == 2:
            driver.switch_to.window(driver.window_handles[-1])

            r = new Robot()
            s = r.keyPress(KeyEvent.VK_ENTER)
            s = r.keyRelease(KeyEvent.VK_ENTER)



            html = driver.find_element_by_class_name("register_top_area").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            print(soup)

            table = soup.find('table').find('tbody')
            td = table.find_all('tr')[1].find_all('div')[1]['class']
            if len(td) == 1:
                cnt_chk = 1
            else:
                cnt_chk = 0

            if td[0] != 'no_jw':
                td = table.find_all('tr')[1].find_all('div')[5]['class']
                if len(td) == 1:
                    cnt_chk = 1
                else:
                    cnt_chk = 0
            print(cnt_chk)
            print('완료')



    # else:
    #     print('에러')
    #     cnt_chk = 2
    #     driver.switch_to.window(driver.window_handles[0])
    #     time.sleep(2)
        # except:
        #     print('에러')
        #     cnt_chk = 2
        #     driver.switch_to.window(driver.window_handles[0])
        #     time.sleep(2)
        # dbUpdate(checkNum,cnt_chk,url)
    # except:
    #     pass
    # except TimeoutException:    # 예외 처리
    #     print('해당 페이지에 연극 정보가 존재하지 않습니다.')
    finally:
        driver.close()
if __name__=='__main__':
    start_time = time.time()

    print("wedisk check 크롤링 시작")
    main()
    print("wedisk check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
