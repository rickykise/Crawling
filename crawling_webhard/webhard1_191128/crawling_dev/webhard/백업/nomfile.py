import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

# ==================불법 업체==================

def startCrawling(site):
    i = 0;check = True
    link = "http://nomfile.com/contents/" + site
    print(link)
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get(link)
    time.sleep(3)
    # if driver.find_element_by_xpath('//*[@id="threechk"]'):
    #     driver.find_element_by_xpath('//*[@id="threechk"]').click()
    #     time.sleep(2)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            html = driver.find_element_by_class_name("contentsList").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find_all('table', 'boardtype1')[1]
            if table.find("tbody").find_all("tr", "reply") == None:
                break
            tr = table.find("tbody").find_all("tr", "reply")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # title = item.find('td', 'title').text.strip()
                cnt_num = item['id'].split("list_")[1]
                url = "http://nomfile.com/contents/view.htm?idx=" + cnt_num
                cnt_vol = item.find_all('td', 'date1')[0].text.strip()
                cnt_price = item.find_all('td', 'date1')[1].find('b').text.strip().split("P")[0].replace(",","")
                cnt_writer = item.find_all('td', 'date')[1].find('a').text.strip()

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                frame = "http://nomfile.com/contents/" + soup.find_all('frame')[0]['src']
                driver.get(frame)
                time.sleep(3)
                htmll = driver.find_element_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr[1]/td[1]/table').get_attribute('innerHTML')
                tags = BeautifulSoup(htmll,'html.parser')
                title = tags.find('tbody').find('tr').find('table').find('tr').find_all('td')[1].text.strip()
                cnt_fname = tags.find('tbody').find('table', 'file').find('tbody').find('td').text.strip()

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'nomfile',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
                    'Cnt_regdate' : now,
                    'Cnt_chk': '0'
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

            driver.find_element_by_xpath('//*[@id="rightqick"]/a[1]').click()
            time.sleep(2)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("nomfile 크롤링 시작")
    site = ['','?c1=MVO','?c1=DRA','?c1=MED','?c1=ANI']
    for s in site:
        startCrawling(s)
    print("nomfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
