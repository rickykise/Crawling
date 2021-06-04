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
    div = soup.find('div', 'view_bx')
    # print(div)

    title = div.find('div', 'tit').find('li', 'tit_le').text.strip()
    cnt_vol = div.find('table').find('tr').find_all('td')[1].find('li').text.split("/")[0].strip()
    cnt_fname = div.find('div', 'ftb_name').text.strip()

    data = {
        'Cnt_title': title,
        'Cnt_vol': cnt_vol,
        'Cnt_fname' : cnt_fname
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://fileis.com/contents/index.htm?category1="+site
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id("contentsListWrap").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('td', 'title') == None:
                    continue
                # title = item.find('td', 'title').find('a').text.strip()
                adult = item.find('td', 'title').find('div', 'ellipsis').find_all('img')
                if len(adult) != 2:
                    continue
                cnt_price = item.find_all('td', 'da3')[1].find('span', 'nc_tdco_on').text.strip().split("P")[0].replace(",","")
                cnt_writer = item.find_all('td', 'da3')[3].text.strip()
                cnt_num = item.find('td', 'da3').text.strip()
                url = "http://fileis.com/contents/view.htm?idx=" + cnt_num + "&viewPageNum="
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'fileis',
                    'Cnt_title': resultData['Cnt_title'],
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : resultData['Cnt_vol'],
                    'Cnt_fname' : resultData['Cnt_fname'],
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
    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("fileis 크롤링 시작")
    site = ['MVO#','DRA#','MED#','ANI#']
    for s in site:
        startCrawling(s)
    print("fileis 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
