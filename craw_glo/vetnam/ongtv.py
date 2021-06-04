import requests
import time
import sys, os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
from selenium import webdriver
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True;a = 1
    link = 'https://www.ongtv.net/search/label/phim-han-quoc?v=theloai&page='
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver",  chrome_options=chrome_options)
    try:
        while check:
            i = i+1
            if i == 12:
                break
            driver.get(link+str(i))
            elem = driver.find_element_by_xpath('//*[@id="outer-wrapper"]/div[2]/ul')
            c = elem.get_attribute('innerHTML')
            soup = BeautifulSoup(c, "html.parser")
            li = soup.find_all('li',  'movie-item')
            try:
                for item in li:
                    url = item.find('a')['href']
                    titleSub = item.find('a')['title']
                    title_check = titleNull(titleSub)
                    
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check,  getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    driver.get(url)
                    elem = driver.find_element_by_xpath('//*[@id="anc_tp"]')
                    c = elem.get_attribute('innerHTML')
                    soup = BeautifulSoup(c, "html.parser")
                    sub = soup.find('div',  id="list_tap").find_all('a', id=re.compile("ep_+"))

                    for item in sub:
                        host_url = url+item['href']
                        title = titleSub+'_'+item.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'ongtv',
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
    print("ongtv 크롤링 시작")
    startCrawling()
    print("ongtv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
