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
    link = 'http://seasonvar.ru/'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
    try:
        driver.get(link)
        time.sleep(.5)
        driver.execute_script('document.querySelector("body > div.wrapper > div > div.sidebar.lside > div:nth-child(1) > div:nth-child(1) > div > div.lside-block > div.lside-blockg.lsidef > select").value="Корея Южная";')
        time.sleep(.5)
        driver.execute_script('document.querySelector("body > div.wrapper > div > div.sidebar.lside > div:nth-child(1) > div:nth-child(1) > div > div.lside-block > div:nth-child(4) > div > select").value = "8";')
        time.sleep(.5)
        driver.execute_script('document.querySelector("body > div.wrapper > div > div.sidebar.lside > div:nth-child(1) > div.btn.lside-btn").click();')
        time.sleep(5)

        html = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div').get_attribute('innerHTML')
    finally:
        driver.close()

    if html == None:
        return False

    soup = BeautifulSoup(html,'html.parser')
    sub = soup.find_all('a')
    for item in sub:
        try:
            url = 'http://seasonvar.ru'+item['href']
            title = item.text.strip().replace('\n','')
            title_null = titleNull(title)
            
            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_null, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']
            li = soup.find_all('li')
            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'seasonvar.ru',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'ukraine',
                'cnt_writer': ''
            }
            # print(data)
            # print("=================================")
            dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("seasonvar.ru 크롤링 시작")
    startCrawling()
    print("seasonvar.ru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
