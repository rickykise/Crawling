import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    table = soup.find('table', 'view_tb')
    cnt_chk = 0

    cnt_price = table.find('tr').find_all('td')[1].text.strip().split("P")[0].replace(",","")
    cnt_fname = soup.find('div', 'view_name3').text.strip()

    if soup.find('li', 'tit_le2'):
        cnt_chk = 1

    data = {
        'Cnt_fname' : cnt_fname,
        'Cnt_price' : cnt_price,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://me2disk.com/contents/index.htm?category1="+site+"#"
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id('contentsListWrap').get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr", height="31")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if item.find('td' ,'title').find('div', 'ellipsis').find('img'):
                    img = item.find('td' ,'title').find('div', 'ellipsis').find_all('img')
                    div = item.find('td' ,'title').find('div', 'ellipsis')
                    if len(img) == 1:
                        if div.find('img')['src'].find('t19.gif') != -1:
                            continue
                    elif len(img) == 2:
                        if div.find_all('img')[1]['src'].find('t19.gif') != -1:
                            continue
                    elif len(img) == 3:
                        if div.find_all('img')[1]['src'].find('t19.gif') != -1:
                            continue

                title = item.find('a', 'ctn')['title']
                cnt_vol = item.find_all('td')[3].text.strip()
                cnt_writer = item.find_all('td')[5].text.strip()
                cnt_num = item['data-idx']
                url = 'http://me2disk.com/contents/view.htm?idx='+cnt_num+'&viewPageNum='
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'me2disk',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : resultData['Cnt_fname'],
                    'Cnt_regdate' : now,
                    'Cnt_chk': resultData['Cnt_chk']
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

    print("me2disk 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("me2disk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
