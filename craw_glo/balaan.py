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

def startCrawling():
    i = 0;check = True
    while check:
        try:
            i = i+1
            if i == 3:
                break; check=False
            link = 'https://www.balaan.co.kr/m2/goods/list.php?brandno=&keyword=&f_category=010&f_brandno%5B%5D=38&f_delivery=&searchType=filter&f_naver_lowest_price=N&f_lowest_goods=N&f_logistics=N&oneday_delivery=N&sort=popular&page='
            driver = webdriver.Chrome("c:\python36\driver\chromedriver")
            driver.get(link+str(i))
            time.sleep(3)

            driver.switch_to_frame('ifr')
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,'html.parser')
            div = soup.find('div', 'container_goods').find_all('div', 'item')

            for item in div:
                url = 'https://www.balaan.co.kr/shop/pc2m.php?landing_url='+item.find('a', 'list-goods-link')['href']
                brandnm = item.find('div', 'brandnm').text.strip()
                price = item.find('div', 'price').text.replace(',', '').strip()
                no_sale_price = item.find('div', 'no_sale_price').text.replace(',', '').strip()

                driver.get(url)
                time.sleep(3)

                driver.switch_to_frame('ifr')
                page_source = driver.page_source
                soup = BeautifulSoup(page_source,'html.parser')
                div = soup.find('section', 'accordion').find('div', 'content')

                balaancode = div.find('div', 'row').find_all('div')[1].text.strip()
                goodsnm = div.find_all('div', 'row')[2].find_all('div')[1].text.strip()
                # goodscode = div.find_all('div', 'row')[3].find_all('div')[1].text.strip()
                # season = div.find_all('div', 'row')[4].find_all('div')[1].text.strip()
                # material = div.find_all('div', 'row')[5].find_all('div')[1].text.strip()
                # color = div.find_all('div', 'row')[6].find_all('div')[1].text.strip()

                data = {
                    'url': url,
                    'brandnm': brandnm,
                    'price' : price,
                    'no_sale_price': no_sale_price,
                    'balaancode': balaancode,
                    'goodsnm': goodsnm
                    # 'goodscode': goodscode,
                    # 'season': season,
                    # 'material': material,
                    # 'color': color
                }
                print(data)
                print("=================================")

        # except:
        #     pass
        finally:
            driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("balaan 크롤링 시작")
    startCrawling()
    print("balaan 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
