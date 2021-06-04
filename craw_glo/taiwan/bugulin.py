import requests
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    link = 'https://bugulin.net/kr/'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
    try:
        driver.get(link)
        html = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        div = soup.find_all('div','drama')
        for item in div:
            try:
                url = 'https://bugulin.net'+item.find('a')['href']
                titleSub = item.find('a').get("title")
                if titleSub == None:
                    titleSub = item.find('a').text.split('(')[0]
                time.sleep(.5)
                driver.get(url)
                title_check = titleNull(titleSub)
                
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                html = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[2]").get_attribute('innerHTML')
                soup = BeautifulSoup(html,"html.parser")
                sub = soup.find_all('a')
                for item in sub:
                    host_url = 'https://bugulin.net'+item['href']
                    title = item.text.strip()
                    title_null = titleNull(title)
                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'bugulin',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'taiwan',
                        'cnt_writer': ''
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

    print("bugulin 크롤링 시작")
    startCrawling()
    print("bugulin 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
