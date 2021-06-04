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
    i = 0;check = True
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver",  chrome_options=chrome_options)
    link = 'http://www.phymhan.com/theloai/phim-truyen-hinh-han-quoc-z{}.html'
    try:
        for i in range(1,3):
            driver.get(link.format(str(i)))
            try:
                for i in range(1,30):
                    try:
                        driver.execute_script('document.querySelector("#load-more > button").click()');
                        time.sleep(5)
                    except:
                        break

                elem = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div/div[2]/div[1]')
                c = elem.get_attribute('innerHTML')
                soup = BeautifulSoup(c, "html.parser")
                div = soup.find_all('div',  'list-movie-box')

                for item in div:
                    if item.find('a'):
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

                        try:
                            r = requests.get(url)
                            c = r.text
                            soup = BeautifulSoup(c, "html.parser")
                            div = soup.find('div', "list-episode-content")
                            if div:
                                li = div.find_all('li')
                                for item in li:
                                    host_url = item.find('a')['href']
                                    title = titleSub+'_'+item.find('a').text.strip()
                                    title_null = titleNull(title)

                                    data = {
                                        'cnt_id': cnt_id,
                                        'cnt_osp': 'phymhan',
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
                continue
    finally:
        driver.close()
if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phymhan 크롤링 시작")
    startCrawling()
    print("phymhan 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
