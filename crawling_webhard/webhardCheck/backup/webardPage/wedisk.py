import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from webhardFun import *

def startCrawling(site):
    i = 0;check = True
    link = 'http://www.wedisk.co.kr/wediskNew/Home/contentsList.do?data=%7B%22searchType%22%3A%221%22%2C%22category%22%3A%22'+site+'%22%2C%22subCategory%22%3A%22%22%2C%22subKey%22%3A%22%22%2C%22searchArea%22%3A%2221%22%2C%22searchKeyword%22%3A%22%22%2C%22pageViewRowNumber%22%3A%2220%22%2C%22selectCategory%22%3A%2200%22%2C%22selectSubCategory%22%3A%22%22%2C%22pageViewPoint%22%3A%22'
    link2 = '%22%2C%22oldSearchOption%22%3A%22%22%2C%22sort%22%3A%220%22%2C%22chkMbc%22%3A%22%22%2C%22SubCategory%22%3A%22%22%2C%22keyword%22%3A%22%22%7D'
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get('https://www.wedisk.co.kr/common/html/member/loginForm.html?20180719')
        time.sleep(2)
        print('새로고침중.../')
        driver.refresh()
        time.sleep(2)
        driver.find_element_by_id('uid').send_keys('llim9898')
        driver.find_element_by_id('upw').send_keys('55085508lim')
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/form/input').click()
        time.sleep(2)
        while check:
            i = i+1
            if i == 4:
                break
            driver.get(link+str(i)+link2)
            html = driver.find_element_by_class_name("data_list").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                titleCheck = item.find('a', 'list_title').text.strip()
                title_nullCheck = titleNull(titleCheck)
                cnt_num = item.find('td')['id'].split("c")[1]
                url = "http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID="+cnt_num
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_nullCheck, getKey)
                if keyCheck['m'] == None:
                    dbResult = insertDB('wedisk',titleCheck,title_nullCheck,url)
                    continue
                keyCheck2 = checkTitle2(title_nullCheck, getKey)
                if keyCheck2['m'] == None:
                    dbResult = insertDB('wedisk',titleCheck,title_nullCheck,url)
                    continue
                id = item.find('td')['id'].replace(" ","")
                cnt_vol = item.find('td', 'data_byte').text.strip()
                cnt_price = item.find('td', 'data_price').text.replace("캐시","").replace(" ","").replace(",","").strip()
                cnt_writer = item.find('td', 'data_user').find('a').text.strip()
                title = ''
                cnt_chk = 0
                if item.find('div', 'data_title adult_check'):
                    continue
                time.sleep(2)
                # driver.find_element_by_xpath('//*[@id="'+id+'"]/div/div[1]/a').click()
                driver.execute_script("openDnWin("+cnt_num+","+id+");")
                time.sleep(2)
                if len(driver.window_handles) == 2:
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)
                    html = driver.find_element_by_class_name("register_top_area").get_attribute('innerHTML')
                    soup = BeautifulSoup(html,'html.parser')

                    if cnt_price == "가격할인":
                        cnt_price = soup.find('span', 'price').text.replace("캐시","").replace(" ","").replace(",","").split("/")[0].strip()
                    title = soup.find('div', 'register_title')['title']
                    title_null = titleNull(title)
                    fname = soup.find('ul', 'file_info').find('li', 'file_title').text.strip()
                    if soup.find('li', 'file_type00'):
                        fname = soup.find('li', 'file_type00')['title']

                    table = soup.find('table').find('tbody')
                    td = table.find_all('tr')[1].find_all('div')[1]['class']
                    if len(td) == 1:
                        cnt_chk = 1
                    else:
                        cnt_chk = 0
                    if td[0] != 'no_jw':
                        td = table.find_all('tr')[1].find_all('div')[5]['class']
                        if len(td) == 1:
                            cnt_chk = 1
                        else:
                            cnt_chk = 0
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)
                elif len(driver.window_handles) == 1:
                    continue
                elif title == '':
                    continue

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'wedisk',
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

                dbResult = insertALL(data)
    except:
        pass
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
