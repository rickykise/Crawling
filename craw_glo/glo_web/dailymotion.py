import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from gloFun import *
from bs4 import BeautifulSoup
import pymysql,time,datetime

def startCrawling(key, keyItem):
    Y = 250;keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://www.dailymotion.com/search/'+keyword+'/videos'
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        for i in range(5):
            try:
                driver.execute_script("window.scrollTo(0, "+str(Y)+");")
                Y += 250
                time.sleep(3)
            except:
                pass
        html = driver.find_element_by_class_name("Section__section___yEfVV").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        div = soup.find_all("div", 'Grid Grid__grid___U2CEO')

        for item in div:
            title = item.find('div', 'Details__title___1qhDj Video__title___2PurE').text.strip()
            # googleCheck = googleCheckTitle(title, key, cnt_id)
            # if googleCheck == None:
            #     continue
            title_null = titleNull(title)
            keywordCh = keyword.replace(' ', '')
            if title_null.find(keywordCh) == -1:
                continue
            cnt_writer = item.find('div', 'Video__channel___3TYCL').find('div')['title']
            url = 'https://www.dailymotion.com'+item.find('a')['href']

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'dailymotion',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'france',
                'cnt_writer': cnt_writer,
                'origin_url': '',
                'origin_osp': '',
                'cnt_keyword_nat': k_nat
            }
            # print(data)
            # print("=================================")

            dbResult = insertALLKey(data)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeyword()

    print("dailymotion 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("dailymotion 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
