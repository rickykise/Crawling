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

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    title = soup.find('div', 'ctvTitle').find('span', id='js-titleEllipsis').text.strip()
    cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().split("P")[0]
    cnt_fnameCk = soup.find('div', 'bxSkin').find('span', 'capacity').text.strip()
    cnt_fname = soup.find('div', 'bxSkin').text.replace("\n","").replace("\t","").replace("\xa0", "").strip().split(cnt_fnameCk)[0]

    data = {
        'Cnt_title': title,
        'Cnt_fname' : cnt_fname,
        'Cnt_price' : cnt_price
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.kdisk.co.kr/index.php?mode=kdisk&section="+site+"&p="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id('mnShare_text_list').get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody", id="contents_list").find_all("tr",class_=False)
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('td', 'subject').find('span', 'textOverflow').find('img'):
                    img = item.find('td', 'subject').find('span', 'textOverflow').find_all('img')
                    if len(img) == 1:
                        if item.find('td', 'subject').find('span', 'textOverflow').find('img')['src'].find('icon_19up') != -1:
                            continue
                    elif len(img) == 2:
                        if item.find('td', 'subject').find('span', 'textOverflow').find_all('img')[1]['src'].find('icon_19up') != -1:
                            continue
                    elif len(img) == 3:
                        if item.find('td', 'subject').find('span', 'textOverflow').find_all('img')[1]['src'].find('icon_19up') != -1:
                            continue
                cnt_num = item.find('td', 'subject').find('a')['idx']
                url = 'http://www.kdisk.co.kr/pop.php?sm=bbs_info&idx=' + cnt_num
                cnt_vol = item.find('td', 'capacity').text.strip()
                cnt_writer = item.find('td', 'nickname').find('a', 'btpTip').text.strip()
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'kdisk',
                    'Cnt_title': resultData['Cnt_title'],
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : resultData['Cnt_fname'],
                    'Cnt_regdate' : now
                }
                # print(data)

                conn = pymysql.connect(host='umj7-001.cafe24.com',user='ikoda',password='uni1004!@',db='ikoda',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_regdate'])
                    if dbResult:
                        check=False
                finally :
                    conn.close()

    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("kdisk 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("kdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
