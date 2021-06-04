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
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    link = 'https://www.phim-homnay.net/phim-bo-han-quoc-pbn4.html'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    chrome_options.add_argument("SameSite=None")
    driver = webdriver.Chrome("c:\python36\driver\chromedriver",  chrome_options=chrome_options)

    try:
        driver.get(link)
        time.sleep(3)
        elem = driver.find_element_by_xpath('//*[@id="catalog_content"]')
        c = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find_all('div', 'ml-item')

        for item in div:
            try:
                url = item.find('a')['href']
                titleSub = item.find('a')['title'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                driver.get(url)
                elem = driver.find_element_by_xpath('//*[@id="film-content"]')
                c = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(c, "html.parser")
                url2 = soup.find('a','bwac-btn')['href']

                driver.get(url2)
                elem = driver.find_element_by_xpath('//*[@id="pas-list-list"]')
                c = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(c, "html.parser")
                li = soup.find('ul').find_all('li')

                for item in li:
                    host_url =  item.find('a')['href']
                    title = titleSub + '_' + item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'phim-homnay',
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
                    print(data)
                    print('===================================')

                    dbResult = insertALL(data)
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phim-homnay 크롤링 시작")
    startCrawling()
    print("phim-homnay 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
