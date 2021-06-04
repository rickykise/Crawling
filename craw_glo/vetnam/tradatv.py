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
    i = 1;check = True
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
    try:
        while check:
            try:
                i = i + 1
                if i == 29:
                    break
                link = 'http://tradatv.com/phim-han-quoc/trang-{}/'
                r = requests.get(link.format(str(i)))
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                div = soup.find('div', 'wrapper mt-3').find_all('div', 'col-lg-3 col-md-6 col-sm-6 col-6')

                for item in div:
                    url = item.find('a')['href']
                    titleSub = item.find('h2', 'title').text.strip()
                    title_check = titleNull(titleSub)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    driver.get(url)
                    time.sleep(5)
                    elem = driver.find_element_by_xpath('//*[@id="eps"]')
                    c = elem.get_attribute('innerHTML')
                    soup = BeautifulSoup(c, "html.parser")
                    sub = soup.find_all('a', 'movie-eps-item')
                    for item1 in sub:
                        host_url = item1['href']
                        title = titleSub + '_' + item1['title']
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'tradatv',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url': host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'vietnam',
                            'cnt_writer': '',
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
            except:
                continue
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("tradatv 크롤링 시작")
    startCrawling()
    print("tradatv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
