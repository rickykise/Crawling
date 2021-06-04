import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import pyautogui
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from webhardFun import *

def startCrawling(site):
    i = 0;check = True

    link = 'http://www.wedisk.co.kr/wediskNew/Home/contentsList.do?data=%7B"searchType"%3A"2"%2C"category"%3A"'+site+'"%2C"subCategory"%3A""%2C"subKey"%3A""%2C"searchArea"%3A"21"%2C"searchKeyword"%3A""%2C"pageViewRowNumber"%3A"20"%2C"selectCategory"%3A"05"%2C"selectSubCategory"%3A""%2C"pageViewPoint"%3A"'
    link2 = '"%2C"oldSearchOption"%3A""%2C"sort"%3A"0"%2C"chkMbc"%3A""%2C"SubCategory"%3A""%2C"keyword"%3A""%7D'
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            driver.get(link+str(i)+link2)
            time.sleep(2)
            html = driver.find_element_by_class_name("data_list").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            b = 0
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                b = b + 1
                if b == 21:
                    b = 1
                print(b)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # pyautogui.hotkey('F5')
                # time.sleep(2)
                cnt_num = item.find('td')['id'].split("c")[1]
                url = "http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID="+cnt_num
                cnt_vol = item.find('td', 'data_byte').text.strip()
                cnt_price = item.find('td', 'data_price').text.replace("캐시","").replace(" ","").replace(",","").strip()
                cnt_writer = item.find('td', 'data_user').find('a').text.strip()
                if item.find('div', 'data_title adult_check'):
                    continue
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="data_list"]/tr['+str(b)+']').click()
                time.sleep(2)
                print('스위치!!:',len(driver.window_handles))
                if len(driver.window_handles) == 2:
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)
                    html = driver.find_element_by_class_name("register_top_area").get_attribute('innerHTML')
                    soup = BeautifulSoup(html,'html.parser')

                    title = soup.find('div', 'register_title')['title']
                    fname = soup.find('ul', 'file_info').find('li', 'file_title').text.strip()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'wedisk',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : fname,
                    'Cnt_regdate' : now
                    # 'Cnt_chk': resultData['Cnt_chk']
                }
                print(data)


                # print(driver.current_url)
                # r = requests.get(driver.current_url)
                # c = r.content
                # soup = BeautifulSoup(c,"html.parser")
                # print(soup)
                # if driver.find_element_by_class_name("register_top_area"):
                #     html = driver.find_element_by_class_name("register_top_area").get_attribute('innerHTML')
                #     soup = BeautifulSoup(html,'html.parser')
                #     fname = soup.find('ul', 'file_info').find('li', 'file_title').text.strip()
                #     print(fname)
                #     print('===================================================================')

                # title = item.find('div', 'data_title')['title']
                # # print(title)
                # # print("=================================")

                # resultData = getContents(url)
                # print(url)


                # resultData = getContents(url)
    # except:
    #     pass
    finally:
        driver.close()


if __name__=='__main__':
    start_time = time.time()

    print("wedisk 크롤링 시작")
    site = ['00','01','02','03','05']
    for s in site:
        startCrawling(s)
    print("wedisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
