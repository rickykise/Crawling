import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(site):
    i = 0;check = True
    link = "https://www.filecity.co.kr/contents/#tab="+site+"&view=list&sale=0&sale2=0&limit=20&pn="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            driver.get(link+str(i))
            i = i+1
            # 페이지 0부터 시작
            if i == 3:
                break
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="except_adult"]/label').click()
            time.sleep(2)
            html = driver.find_element_by_class_name("contents_list").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break
            try:
                for item in tr:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cnt_vol = item.find('td', 'contents_list_td3').text.strip()
                    cnt_writer = item.find('td', 'contents_list_td3 user_id01').text.strip()
                    cnt_num = item.find('td', 'contents_list_td1')['onclick'].split("'")[1].split("'")[0]
                    url = "http://renew.filecity.co.kr/contents/#tab="+site+"&view=list&idx="+cnt_num

                    driver.get(url)
                    time.sleep(2)
                    htmll = driver.find_element_by_class_name('view_inner').get_attribute('innerHTML')
                    tags = BeautifulSoup(htmll,'html.parser')
                    title = tags.find('div', 'cont_title').text.strip()
                    cnt_price = tags.find('li', 'point02').find('span', 'num').text.strip().replace(",","")
                    cnt_fname = tags.find('div', 'info_body').find('li', 'info01').text.strip()
                    cnt_chk = 0
                    if tags.find('ul', 'clearfix icon_alliance '):
                        cnt_chk = 1
                    # print(cnt_chk)


                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filecity',
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
            except:
                continue
    # except:
    #     pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("filecity 크롤링 시작")
    site = ['BD_MV','BD_DM','BD_UC','BD_AN']
    for s in site:
        startCrawling(s)
    print("filecity 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
