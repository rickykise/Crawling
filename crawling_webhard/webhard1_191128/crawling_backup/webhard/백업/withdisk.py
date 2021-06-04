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

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    cnt_fname = soup.find('td', 'td_tit').text.strip()
    # print(cnt_fname)

    data = {
        'Cnt_fname' : cnt_fname
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.withdisk.com/contents/?category1="+site+"&page="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_class_name("boardtype1").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item.find('td', 'title').find('a').text.strip()
                cnt_num = item['id'].split("list_")[1]
                url = "http://www.withdisk.com/contents/view.htm?idx="+cnt_num
                cnt_vol = item.find_all('td', 'date')[0].text.strip()
                cnt_price = item.find_all('td', 'date')[1].text.strip().split("P")[0].replace(",","")
                cnt_writer = item.find_all('td', 'date')[3].text.strip()
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num, #게시물 번호
                    'Cnt_osp' : 'withdisk', #사이트
                    'Cnt_title': title, #제목
                    'Cnt_url': url, #url
                    'Cnt_price': cnt_price, #가격
                    'Cnt_writer' : cnt_writer, #작성
                    'Cnt_vol' : cnt_vol, #용량
                    'Cnt_fname' : resultData['Cnt_fname'], #파일명
                    'Cnt_regdate' : now, #등록일
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

    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("withdisk 크롤링 시작")
    site = ['ALL','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("withdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
