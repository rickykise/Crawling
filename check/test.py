import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
import requests, json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def startCrawling(url):
    link = 'http://www.wedisk.co.kr/wediskNew/Home/contentsList.do?data=%7B%22searchType%22%3A%221%22%2C%22category%22%3A%2200%22%2C%22subCategory%22%3A%22%22%2C%22subKey%22%3A%22%22%2C%22searchArea%22%3A%2221%22%2C%22searchKeyword%22%3A%22%22%2C%22pageViewRowNumber%22%3A%2220%22%2C%22selectCategory%22%3A%2200%22%2C%22selectSubCategory%22%3A%22%22%2C%22pageViewPoint%22%3A%221%22%2C%22oldSearchOption%22%3A%22%22%2C%22sort%22%3A%220%22%2C%22chkMbc%22%3A%22%22%2C%22SubCategory%22%3A%22%22%2C%22keyword%22%3A%22%22%7D'

    driver = webdriver.Chrome("c:\python36\driver\chromedriver")

    try:
        driver.get(link)
        driver.refresh()
        time.sleep(2)

        a = 0
        cnt_num = url.split('contentsID=')[1]
        id = "openDnWin("+cnt_num+",'N');"
        driver.execute_script(id)
        driver.get(url)
        driver.refresh()
        driver.set_page_load_timeout(3)

        driver.switch_to.window(driver.window_handles[-1])
        html = driver.find_element_by_class_name("register_top_area").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        print(soup)
        # time.sleep(2)
    except TimeoutException as e:
        print('얼럿')
        driver.quit()
    finally:
        driver.close()


    # try:
    #     result = driver.switch_to.alert
    #     print("yes")
    # except:
    #     print("no")
    #     driver.close()


    #     alert = driver.switch_to.alert
    #     alert.accept()
    #     time.sleep(2)
    #     print('aaa')
    # except:
    #     print('dddd')
    #
    # finally:
    #     driver.close()
        # if len(driver.window_handles) == 2:
        #     driver.switch_to.window(driver.window_handles[-1])
        #
        #     html = driver.find_element_by_class_name("register_top_area").get_attribute('innerHTML')
        #     soup = BeautifulSoup(html,'html.parser')
        #     print(soup)
        #
        #     table = soup.find('table').find('tbody')
        #     td = table.find_all('tr')[1].find_all('div')[1]['class']
        #     if len(td) == 1:
        #         cnt_chk = 1
        #     else:
        #         cnt_chk = 0
        #
        #     if td[0] != 'no_jw':
        #         td = table.find_all('tr')[1].find_all('div')[5]['class']
        #         if len(td) == 1:
        #             cnt_chk = 1
        #         else:
        #             cnt_chk = 0
        #     print(cnt_chk)
        #     print('완료')
        #     print('dfsdfsdf')
            # pass

if __name__=='__main__':
    start_time = time.time()
    getUrl = ['http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID=30038517', 'http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID=546546']
    for u in getUrl:
        startCrawling(u)
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
