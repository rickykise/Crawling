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
    link = 'https://danet.vn/go/AVOD'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
    try:
        driver.get(link)
        time.sleep(.5)
        for num in range(30):
            driver.execute_script('$(".right-arrow").click()')
            time.sleep(3)

        html = driver.find_element_by_xpath('//*[@id="app"]/div/span/div/div').get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        sub = soup.find_all('a','core-media__link')
        for item in sub:
            try:
                url = 'https://danet.vn'+item['href']
                title = item.find('h3','core-media__title')['title']
                title_null = titleNull(title)
                
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'danet',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'vetnam',
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

    print("danet 크롤링 시작")
    startCrawling()
    print("danet 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
