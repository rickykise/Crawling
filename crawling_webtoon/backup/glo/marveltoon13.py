import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    i = 0;check = True
    link = 'https://marveltoon13.com/'
    while check:
        i = i+1
        if i == 2:
            break
        try:
            driver = webdriver.Chrome("c:\python36\driver\chromedriver")
            driver.get(link)
            time.sleep(10)
            html = driver.find_element_by_class_name("homelist").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            div = soup.find_all('div', 'section-item-title')

            try:
                for item in div:
                    url = 'https://marveltoon13.com'+item.find('a')['href'].replace('..', '')
                    title = item.find('a').text.strip()
                    title_check = titleNull(title)

                    driver.get(url)
                    time.sleep(3)
                    html = driver.find_element_by_class_name("bt-table").get_attribute('innerHTML')
                    soup = BeautifulSoup(html,'html.parser')
                    tr = soup.find('tbody').find_all('tr')

                    for item in tr:
                        craw_url = 'https://marveltoon13.com'+item.find('td', class_=None).find('a')['href'].replace('..', '')
                        title_numCh = item.find('td', class_=None).find('a').text.replace(' ', '').replace(',', '').strip()
                        title_num = title_numCh.split(title_check)[1].split('화')[0].strip()
                        if title_num.find('-') != -1:
                            title_num = title_num.split('-')[1].strip()

                        data = {
                            'craw_osp_id': 'marveltoon13',
                            'craw_domain': 'com',
                            'craw_title': title,
                            'craw_site_url' : url,
                            'craw_url': craw_url,
                            'craw_title_num': title_num
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
            except:
                continue
        except:
            pass
        finally:
            driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("marveltoon13 크롤링 시작")
    startCrawling()
    print("marveltoon13 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
