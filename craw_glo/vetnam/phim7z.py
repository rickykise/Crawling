import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    i = 0;check = True
    link = 'https://phim7z.tv/phim-bo/page/{}'
    while check:
        i = i+1
        if i == 69:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find('div', 'movies-list').find_all('div', 'ml-item')
        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('a')['oldtitle'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']


                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                url2 = soup.find('a','btn-watch')['href']

                driver = webdriver.Chrome("c:\python36\driver\chromedriver",  chrome_options=chrome_options)
                try:
                    driver.get(url2)
                    time.sleep(3)
                    elem = driver.find_element_by_xpath('//*[@id="list-eps"]')
                    c = elem.get_attribute('innerHTML')
                finally:
                    driver.close()
                soup = BeautifulSoup(c, "html.parser")
                les = soup.find('div',  'les-content').find_all('a')

                for item in les:
                    host_url =  'https://phim7z.tv'+item['href']
                    title = titleSub + '_' + item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'phim7z',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
                        'cnt_writer': ''
                    }
                    # print(data)
                    dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phim7z 크롤링 시작")
    startCrawling()
    print("phim7z 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
