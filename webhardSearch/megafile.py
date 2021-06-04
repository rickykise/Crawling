import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from tkinter.filedialog import askopenfilename
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from webhardFun import *

def startCrawling(key):
    i = 0;check = True
    key = key.replace(' ', '')
    print(key)
    encText = key.encode('euc-kr')
    encText = urllib.parse.quote(encText)
    link = 'http://www.megafile.co.kr/webhard/list.php?category=&topsearch='+encText+'&pagesize=50#'

    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get('http://www.megafile.co.kr/user/login.php')
        time.sleep(2)
        driver.find_element_by_id('loginid').send_keys('up0002')
        driver.find_element_by_id('passwd').send_keys('up0002')
        driver.find_element_by_xpath('//*[@id="body"]/form/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td[3]/input').click()
        time.sleep(2)

        try:
            WebDriverWait(driver, 1).until(EC.alert_is_present())
            Alert(driver).accept()
            time.sleep(2)
        except TimeoutException:
            pass

        while check:
            i = i+1
            if i == 4:
                break
            driver.get(link+str(i))
            time.sleep(3)
            html = driver.find_element_by_id("board").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            if soup.find('div', 'search_result_none'):
                break
            ul = soup.find_all('ul', id='list')

            for item in ul:
                text = str(item)
                if text.find('타사이트') != -1 or text.find('성인인증이 필요') != -1:
                    continue
                cnt_num = item.find('input')['value']
                idCheck = item.find('a')['onclick']
                if idCheck.find('OpenViewWindow2_new(') != -1:
                    id = item.find('a')['onclick'].split('OpenViewWindow2_new(')[1].split(' ,')[0]
                else:
                    id = item.find('a')['onclick'].split('OpenViewWindow2(')[1].split(' ,')[0]
                url = 'http://www.megafile.co.kr/webhard/view.php?WriteNum='+cnt_num+'&id='+id+'&fv='
                title = item.find('a')['title']
                title_null = titleNull(title)

                # 키워드 체크
                # getKey = getKeyword()
                # keyCheck = checkTitle(title_null, getKey)
                # if keyCheck['m'] == None:
                #     dbResult = insertDB('megafile',title,title_null,url)
                #     continue
                # keyCheck2 = checkTitle2(title_null, getKey)
                # if keyCheck2['m'] == None:
                #     dbResult = insertDB('megafile',title,title_null,url)
                #     continue

                id = item.find('a')['onclick']
                driver.execute_script(id)
                time.sleep(2)

                if len(driver.window_handles) == 2:
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)
                    html = driver.find_element_by_class_name("wrap").get_attribute('innerHTML')
                    soup = BeautifulSoup(html,'html.parser')
                    table1 = soup.find_all('table')[6]
                    table2 = soup.find_all('table')[5]
                    text = str(soup)
                    cnt_chk = 0

                    cnt_price = table1.find_all('td')[1].text.replace(",","").split('캐시')[0].strip()
                    cnt_writer = table2.find_all('td')[1].text.strip()
                    cnt_vol = table1.find_all('td')[4].text.replace(' ', '').strip()
                    fname = soup.find('td', 'file').text.strip()
                    if text.find('제휴업체로부터') != -1:
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'megafile',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print('=============================================')

                    dbResult = insertALL(data)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("megafile 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("megafile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
