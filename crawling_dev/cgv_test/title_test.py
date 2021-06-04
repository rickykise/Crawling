# 페이스북 크롤링
import requests,re
import sys
import pymysql
import datetime,time
import pymysql
from datetime import date, timedelta
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from facebookFun import *

def startCrawling():
    content_check = '';pageKey = '메가박스';sns_subcontent = ''
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
        driver.get('https://www.facebook.com/pg/megaboxon/posts/')
        time.sleep(3)
        for i in range(2):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            except:
                pass
        try:
            driver.find_element_by_xpath('//*[@id="expanding_cta_close_button"]').click()
        except:
            pass
        html = driver.find_elements_by_class_name("_1xnd")[0].get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        div =  soup.find_all("div", "_4-u2")

        for item in div:
            if item.find("div","_1dwg").find("div","_5pbx"):
                sns_content = item.find("div","_1dwg").find("div","_5pbx").text.strip()
                len_content = len(sns_content.find_all(' '))
                # sns_content_test = str(sns_content).replace(" ", '').strip()


                sns_content = remove_emoji(sns_content)
                # sns_content_test = remove_emoji(sns_content_test)

                if content_check == sns_content:
                    continue
                content_check = sns_content

                print(sns_content)
                print(len_content)
                print("=================================")
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    startCrawling()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
