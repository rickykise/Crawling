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

    cnt_fname = soup.find('table', 'infoSheet').find('div', 'file').text.strip()
    cnt_writer = soup.find('td', colspan='2').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")

    data = {
        'Cnt_writer': cnt_writer,
        'Cnt_fname' : cnt_fname
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.filesun.com/disk/board.php?board="+site+"&page="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_class_name("listTable").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find_all('td')[1].find('span', 'icon adult') != None:
                    continue
                title = item.find_all('td')[1].find('a').text.strip()
                url = 'http://www.filesun.com' + item.find_all('td')[1].find('a')['href']
                cnt_num = url.split("&n=")[1].split("&m")[0]
                cnt_vol = item.find('td', 'size').text.strip().split(" ")[0] + item.find('td', 'size').text.strip().split(" ")[1]
                cnt_price = item.find('td', 'downpoint').text.split("→")[1].split("P")[0].strip().replace(",","")
                resultData = getContents(url)

                # driver.get(url)
                # time.sleep(2)
                # page_main = driver.find_element_by_id("diskBoardArticleInfo").get_attribute('innerHTML')
                # tags = BeautifulSoup(page_main,'html.parser')
                # cnt_writer = tags.find('tbody').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").split("판매자")[1].split("파일수")[0]
                # cnt_fname = tags.find('tbody').find('tr', 'viewList_list').find('div', 'file').text.strip()

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filesun',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : resultData['Cnt_writer'],
                    'Cnt_vol' : cnt_vol,
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

    print("filesun 크롤링 시작")
    site = ['1&listmode=all','1','2','3','5']
    for s in site:
        startCrawling(s)
    print("filesun 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
