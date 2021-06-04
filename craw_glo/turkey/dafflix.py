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


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,th;q=0.6',
    'cache-control': 'no-cache',
    'content-length': '2770',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': '__cfduid=dd681bc1e7fa51c8f5f93cfdeb87b5dfa1591173895; cf_clearance=fd606e494742d6150e7da86f50dd9aa4a31031d2-1591173905-0-150; level=1; _ga=GA1.2.1360308374.1591173908; _gid=GA1.2.880222761.1591173908; __dtsu=6D001588575559C5EF711BDF56AADE16; _ym_uid=1591173909918172371; _ym_d=1591173909; _ym_isad=2; goggaAds=1; f31b7244f69a37b2c23eba8595ac4d4d=1; 85333844bc62dc8b11814b68e94e6307=1; _gat_gtag_UA_162691880_1=1',
    'origin': 'https://www.dafflix.com',
    'pragma': 'no-cache',
    'referer': 'https://www.dafflix.com/kesfet/eyJzZXJpZXMiOiJhc3lhLWRpemlsZXJpLWl6bGUiLCJ0eXBlIjoic2VyaWVzIn0=/1',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

def startCrawling():
    i = 0;check = True
    link = 'https://www.dafflix.com/kesfet/eyJzZXJpZXMiOiJhc3lhLWRpemlsZXJpLWl6bGUiLCJ0eXBlIjoic2VyaWVzIn0=/{}'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("--disable-gpu")  # gpu 사용 안하도록 설정
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36")
    chrome_options.add_argument("SameSite=None")
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", options=chrome_options)
    try:
        while check:
            i = i+1
            if i == 12:
                break
            driver.get(link.format(str(i)))
            time.sleep(10)
            elem = driver.find_element_by_xpath('/html/body/section/div[2]/main/div[2]/div[2]/div[3]/div[2]')
            c = elem.get_attribute('innerHTML')
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find('div', 'filter-result').find_all('li','w-full')

            try:
                for item in li:
                    url = 'https://www.dafflix.com/'+item.find('div','filter-result-box-image').find('a')['href']
                    titleSub = item.find('div','filter-result-box-image').find('img')['alt'].strip()
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
                    elem = driver.find_element_by_xpath('/html/body/section/div[2]/main/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[1]')
                    c = elem.get_attribute('innerHTML')
                    soup = BeautifulSoup(c,"html.parser")
                    sub = soup.find('div','series-profile-episodes-areas').find_all('li','items-center')
                    if sub:
                        for item in sub:
                            host_url = 'https://www.dafflix.com/'+item.find('h6','truncate').find('a')['href']
                            title = item.find('h6','truncate').find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'dafflix',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'turkey',
                                'cnt_writer': ''
                            }
                            print(data)
                            print("=================================")

                            # dbResult = insertALL(data)
            except Exception as e:
                print(e)
                continue
    finally:
        driver.close()
if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dafflix 크롤링 시작")
    startCrawling()
    print("dafflix 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
