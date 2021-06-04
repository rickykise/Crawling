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

def startCrawling(link):
    i = 0;check = True
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
    driver.get(link)
    time.sleep(.5)
    try:
        while check:
            i = i+1
            if i == 30:
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            time.sleep(.5)

        elem = driver.find_element_by_xpath('//*[@id="root_wrapper"]/div/div[3]/div/div[2]/ul')
        c = elem.get_attribute('innerHTML')
        soup = BeautifulSoup(c, 'html.parser')
        li = soup.find_all('li', 'poster-item')
        for item in li:
            try:
                url = 'https://www.wekan.tv'+item.find('a','poster')['href']
                titleSub = item.find('a','poster')['title']
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
                elem = driver.find_element_by_xpath('//*[@id="root_wrapper"]/div[1]/div/div[1]/div[2]/div/div[3]/ul')
                c = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find_all('a')
                for item in sub:
                    host_url = 'https://www.wekan.tv'+item['href']
                    title = titleSub + '_' + item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'wekan',
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

    print("wekan 크롤링 시작")
    site = ['https://www.wekan.tv/filter-tvdrama-10202-0-0-hot','https://www.wekan.tv/filter-show-10202-0-0-hot']
    for item in site:
        startCrawling(item)
        
    print("wekan 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
