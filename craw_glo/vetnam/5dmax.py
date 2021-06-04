import requests
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
    driver.get('http://m.5dmax.vn/xem-them/film_series_199829')
    time.sleep(.5)
    try:
        while check:
            i = i+1
            if i == 3:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            time.sleep(.5)

        elem = driver.find_element_by_xpath('//*[@id="lazy-container"]')
        c = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(c, 'html.parser')
        div = soup.find_all('div', 'item grid-08')
        for item in div:
            try:
                url = 'http://m.5dmax.vn'+item.find('a','text')['href']
                titleSub = item.find('a','text').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                driver.get(url)
                time.sleep(.5)
                elem = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div')
                c = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find_all('a','item')
                for item in sub:
                    host_url = 'http://m.5dmax.vn'+item['href']
                    title = item.find('div','right-content').find('span','text').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : '5dmax',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
            except Exception as e:
                continue
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("5dmax 크롤링 시작")
    startCrawling()
    print("5dmax 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
