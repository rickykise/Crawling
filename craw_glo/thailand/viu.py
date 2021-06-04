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
    link = 'https://www.viu.com/ott/th/th?r=search&screen=Home&keyword=SBS&user_input=SBS&keyword_group='
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
    try:
        driver.get(link)
        time.sleep(.5)
        for num in range(30):
            driver.execute_script("loadMore('series')")
            time.sleep(3)

        html = driver.find_element_by_xpath('//*[@id="search_list_series"]').get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        div = soup.find_all('div','grid')
        for item in div:
            try:
                url = item.find('a')['onclick']
                titleSub = item.find('div','figure-title').text
                title_check = titleNull(titleSub)
                
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                driver.execute_script(url)
                site_url = driver.current_url
                time.sleep(.5)
                
                html = driver.find_element_by_xpath('//*[@id="select-episode"]/div/ul').get_attribute('innerHTML')
                soup = BeautifulSoup(html,'html.parser')
                li = soup.find_all('li')
                for item2 in li:
                    host_url = 'https://www.viu.com'+item2.find('a')['href']
                    title = titleSub+'_'+item2.find('p','video-num').text.strip()
                    title_null = titleNull(title)
                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'viu',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': site_url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")
                    dbResult = insertALL(data)
            except Exception as e:
                continue
            finally:
                driver.get(link)
    except Exception as e:
        print(e)
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("viu 크롤링 시작")
    startCrawling()
    print("viu 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
