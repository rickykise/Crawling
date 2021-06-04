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
    link = "http://smartfile.co.kr/contents/?"+site+"&limit=&page="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id("search_list").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr1 = soup.find_all('tr', 'rows')
            tr2 = soup.find_all('tr', 'file_list')

            for files in tr2:
                cnt_fname = files.find('ul', 'file-list').find('span', 'f-name').text.strip()
                cnt_numCh = files.find('div', 'thumb').find('img')['id'].split("img_d_")[1]

                data2 = {
                    'Cnt_fname' : cnt_fname,
                    'Cnt_numCh' : cnt_numCh
                }
                # print(data2)

            for tags in tr1:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(data2['Cnt_fname'])
                if tags.find('li', 'adult'):
                    continue
                title = tags.find('span', 'dtitle').find('font').text.strip()
                cnt_num = tags['id'].split("row_")[1]
                cnt_vol = tags.find('td', 'size').text.strip()
                cnt_writer = tags.find('div', 'seller').text.strip()
                url = 'http://smartfile.co.kr/contents/view.php?idx='+cnt_num

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'smartfile',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'cnt_regdate': now
                }
                # print(data)

                # conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                # try:
                #     curs = conn.cursor(pymysql.cursors.DictCursor)
                #     # dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],'',data['Cnt_writer'],data['Cnt_vol'],'',data['cnt_regdate'])
                #     sql = "UPDATE cnt_all SET cnt_fname=%s WHERE cnt_num=%s;"
                #     curs.execute(sql,(data2['Cnt_fname'],data2['Cnt_numCh']))
                #     conn.commit()
                #     # if dbResult:
                #     #     check=False
                # finally :
                #     conn.close()



    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("smartfile 크롤링 시작")
    site = ['category1=MVO','category1=DRA','category1=MED','category1=ANI']
    for s in site:
        startCrawling(s)
    print("smartfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
