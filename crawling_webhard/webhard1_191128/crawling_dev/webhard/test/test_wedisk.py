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

# def getContents(url):
#
#     driver = webdriver.Chrome("c:\python36\driver\chromedriver")
#     driver.get(url)
#     time.sleep(2)
#
#     # title = soup.find('td', 'td_tit').text.strip()
#     print('===================================================================')
#
#     data = {
#         'Cnt_fname' : ''
#     }
#     # print(data)
#     return data

def startCrawling(site):
    i = 0;check = True

    link = 'http://www.wedisk.co.kr/wediskNew/Home/contentsList.do?data=%7B"searchType"%3A"2"%2C"category"%3A"'+site+'"%2C"subCategory"%3A""%2C"subKey"%3A""%2C"searchArea"%3A"21"%2C"searchKeyword"%3A""%2C"pageViewRowNumber"%3A"20"%2C"selectCategory"%3A"05"%2C"selectSubCategory"%3A""%2C"pageViewPoint"%3A"'
    link2 = '"%2C"oldSearchOption"%3A""%2C"sort"%3A"0"%2C"chkMbc"%3A""%2C"SubCategory"%3A""%2C"keyword"%3A""%7D'
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            driver.get(link+str(i)+link2)
            time.sleep(2)
            html = driver.find_element_by_class_name("data_list").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            b = 0
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item.find('div', 'data_title')['title']
                print(title)
                print("=================================")
                # cnt_num = item.find('td')['id'].split("c")[1]
                # url = "http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID="+cnt_num


                # resultData = getContents(url)
    finally:
        driver.close()


if __name__=='__main__':
    start_time = time.time()

    print("wedisk 크롤링 시작")
    site = ['00','01','02','03','05']
    for s in site:
        startCrawling(s)
    print("wedisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
