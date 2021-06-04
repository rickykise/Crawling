import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

# def getContents(url):
#     r = requests.get(url)
#     c = r.content
#     soup = BeautifulSoup(c,"html.parser")
#     div = soup.find('div', id='left_contents')
#     table = div.find('table', 'pop_base')
#
#     title = table.find('thead').find('span').text.strip()
#     cnt_fname = div.find('table', 'pop_detail').find('tbody').find_all('td')[0].text.strip()
#     cnt_price = table.find('tbody').find('td', 'txt')
#     print(cnt_price)
#
#     data = {
#         'Cnt_title': title,
#         'Cnt_fname' : cnt_fname
#     }
#     # print(data)
#     return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.filekok.com/main/storage.php?" + site + "liststate=&list_count=&search_sort=&p="
    # print(link)
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get('http://www.filekok.com/')
    time.sleep(3)
    driver.find_element_by_name('mb_id').send_keys('up0001')
    driver.find_element_by_name('mb_pw').send_keys('up0001')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="leftLoginFrm"]/ul/li[2]/span/img').click()
    time.sleep(2)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_class_name("contents_wrapper").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find_all('table')[1]
            tr = table.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                adult = item.find_all('td')[1].find_all('div')[0]
                if adult.find('span', 'adult19'):
                    continue
                cnt_vol = item.find_all('td')[3].text.strip()
                cnt_writer = item.find_all('td')[5].find('span').text.strip()
                cnt_num = item.find('input', 'list_check')['value']
                url = "http://www.filekok.com/main/popup.php?doc=bbsInfo&idx="+cnt_num

                driver.get(url)
                time.sleep(3)
                htmll = driver.find_element_by_id('wrap_pop').get_attribute('innerHTML')
                tags = BeautifulSoup(htmll,'html.parser')
                divtag = tags.find('div', id='left_contents')
                table = divtag.find('table', 'pop_base')
                cnt_chk = 0

                cnt_fname = divtag.find('table', 'pop_detail').find('tbody').find_all('td')[0].text.strip()
                title = table.find('thead').find('span').text.strip()
                cnt_price = table.find('tbody').find('td', 'txt').find('b').text.strip().replace(",","")
                if table.find('tbody').find('td', 'txt').find('img'):
                    img = table.find('tbody').find('td', 'txt').find('img')['alt']
                    if img.find('제휴') != -1:
                        cnt_chk = 1
                # resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filekok',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
                    'Cnt_regdate' : now,
                    'Cnt_chk': cnt_chk
                }
                # print(data)

                conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                except Exception as e:
                    print(e)
                    pass
                finally :
                    conn.close()

            # div = soup.find('div', 'list_n_menu').find_all('a')
            # # print(len(div))
            # if len(div) == 12:
            #     driver.find_element_by_xpath('//*[@id="list_sort"]/div[2]/div/div/a[11]').click()
            #     time.sleep(2)
            # else:
            #     driver.find_element_by_xpath('//*[@id="list_sort"]/div[2]/div/div/a[12]').click()
            #     time.sleep(2)
    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("filekok 크롤링 시작")
    site = ['','search_type=MOV&','search_type=DRA&','search_type=MED&','search_type=ANI&']
    for s in site:
        startCrawling(s)
    print("filekok 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
