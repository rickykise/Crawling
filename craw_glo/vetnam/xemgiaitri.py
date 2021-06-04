import requests
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
from selenium import webdriver
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    ''
    link = 'https://xemgiaitri.net/category.php?cat=phim-han-quoc&page={}'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
    try:
        while check:
            i = i+1
            if i == 300:
                break
            try:
                driver.get(link.format(str(i)))
                elem = driver.find_element_by_xpath('//*[@id="content"]/div[2]')
                c = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'caption')

                for item in div:
                    if item.find('a'):
                        url = item.find('a')['href']
                        titleSub = item.find('a')['title']
                        if titleSub.find(' - Phim') != -1:
                            titleSub = titleSub.split(' - Phim')[0].strip()
                        if titleSub.find('(') != -1:
                            titleSub = titleSub.split('(')[0].strip()
                        title_check = titleNull(titleSub)

                        # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_check, getKey)
                        if keyCheck['m'] == None:
                            continue

                        cnt_id = keyCheck['i']
                        cnt_keyword = keyCheck['k']
                        host_url = url
                        title = titleSub
                        title_null = titleNull(title)
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'xemgiaitri',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'vietnam',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
            except Exception as e:
                print(e)
                continue
    finally:
        driver.close()
if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("xemgiaitri 크롤링 시작")
    startCrawling()
    print("xemgiaitri 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")

