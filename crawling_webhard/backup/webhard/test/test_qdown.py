import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from webhardFun import *

def startCrawling(site):
    i = 0;check = True
    link = "http://www.qdown.com/main/storage.php?section="+site
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            driver.get(link)
            time.sleep(2)
            html = driver.find_element_by_id('listdiv').get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find('td', height='27').find('table')
            tr = table.find('tbody').find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                td = item.find_all('td')
                if len(td) != 7:
                    continue
                    # title = item.find('span', 'storage_title')['title']
                    # print(title)
                # now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # td = item.find_all('td')
                # print(len(td))
                # title = item.find('span', 'storage_title')['title']
                # cnt_num = item.find('a')['id'].split("title_")[1]
                # url = "http://www.withdisk.com/contents/view.htm?idx="+cnt_num
                # print(title)

            # td = soup.find('table').find('tbody').find_all('tr')[2].find('td').find('table').find('tbody').find('tr').find_all('td')[4].find_all('a')
            # print(len(td))
                driver.find_element_by_xpath('//*[@id="listdiv"]/table/tbody/tr[2]/td/table/tbody/tr/td[22]/a').click()
                time.sleep(5)

            # if
            # if len(div) == 12:
            #     driver.find_element_by_xpath('//*[@id="list_sort"]/div[2]/div/div/a[11]').click()
            #     time.sleep(2)
            # else:
            #     driver.find_element_by_xpath('//*[@id="list_sort"]/div[2]/div/div/a[12]').click()
            #     time.sleep(2)
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("qdown 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("qdown 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
