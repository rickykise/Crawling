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
    cnt_chk = 0

    title = soup.find('title').text.strip()
    cnt_price = soup.find_all('td', 'black_a_s')[2].find('font').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(",","").strip().split("P")[0]
    cnt_fname = soup.find_all('td', 'black_a_s')[3]['title']
    if soup.find('td', 'brown_b').find('img'):
        img = soup.find('td', 'brown_b').find('img')['src']
        if img == 'http://wimg.filejo.com/icon/icon_join_info2.gif':
            cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_fname' : cnt_fname,
        'Cnt_price' : cnt_price,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.filejo.com/main/storage.php?section="+site+"&p="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_xpath('//*[@id="list_sort"]/table/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr/td/table').get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # print(item)
                td = item.find_all('td')
                if len(td) != 11:
                    continue

                if item.find_all('td')[3].find('img'):
                    img = item.find_all('td')[3].find_all('img')
                    if len(img) == 1:
                        if item.find_all('td')[3].find('img')['src'].find('19.gif') != -1:
                            continue
                    elif len(img) == 2:
                        if item.find_all('td')[3].find_all('img')[1]['src'].find('19.gif') != -1:
                            continue

                # title = item.find_all('td')[4].find('span').text.strip()
                cnt_num = item.find_all('td')[4].find('a')['onclick'].split("winBbsInfo('")[1].split("','")[0]
                url = 'http://www.filejo.com/main/popup/bbs_info.php?idx=' + cnt_num
                cnt_vol = item.find_all('td')[8].find('font').text.strip()
                cnt_writer = item.find_all('td')[9].find('font').text.strip()
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filejo',
                    'Cnt_title': resultData['Cnt_title'],
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

    print("filejo 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("filejo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
