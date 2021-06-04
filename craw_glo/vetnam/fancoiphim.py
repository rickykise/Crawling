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
    i = 0;check = True;arr = [];getKey = getKeyword()
    link = 'http://fancoiphim.net/the-loai/phim-han-quoc/'
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('headless')  # headless 모드 설정
    # chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver",  chrome_options=chrome_options)
    driver.get(link)
    try:
        while True:
            i = i+1
            if i == 14:
                break
            try:
                elem = driver.find_element_by_xpath('//*[@id="product"]')
                c = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(c, "html.parser")
                div = soup.find_all('div', id="product_body")
                for item in div:
                    titleTag = item.find('h2').find('a')
                    titleChk =  item.find('h3').text.strip()

                    # 키워드 체크
                    keyCheck = checkTitle(titleChk,  getKey)
                    if keyCheck['m'] == None:
                        continue
                    arr.append(item)
            except Exception as e:
                print(e)
                continue
            finally:
                driver.execute_script("$('.current_number_"+str(i+1)+"').click()")
                time.sleep(3)

        for item in arr:
            try:
                titleTag = item.find('h2').find('a')
                url = titleTag['href']
                titleSub = titleTag['title']

                # 키워드 체크
                keyCheck = checkTitle(titleSub,  getKey)
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                driver.get(url)
                elem = driver.find_element_by_xpath('//*[@id="center"]/div[4]')
                c = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(c, "html.parser")
                sub = soup.find_all('div','chon_tap_all')

                for item in sub:
                    host_url = item.find('a')['href']
                    title = titleSub+'_'+item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'fancoiphim',
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
                    print("=================================")

                    dbResult = insertALL(data)
            except:
                continue
    except Exception as e:
        print(e)
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("fancoiphim 크롤링 시작")
    startCrawling()
    print("fancoiphim 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")

