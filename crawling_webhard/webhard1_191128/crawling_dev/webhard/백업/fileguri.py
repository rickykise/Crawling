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

    title = soup.find('div', 'ctvTitle').find('span').text.strip()
    cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().replace(",","")
    span = soup.find('span', 'capacity').text.strip()
    cnt_fname = soup.find('div', 'bxSkin').find('li').text.split(span)[0].strip()

    if soup.find('p', 'careMsg'):
        cnt_chkCh = soup.find('p', 'careMsg').text.strip()
        if cnt_chkCh.find('제휴') != -1:
            cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_price': cnt_price,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://disk.fileguri.com/index.php?mode=fileguri&search_type="+site
    print(link)
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get(link)
    time.sleep(3)
    # driver.find_element_by_xpath('//*[@id="mnShare"]/div[3]/p[2]/label[1]').click()
    # time.sleep(3)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            html = driver.find_element_by_id("mnShare").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find('tbody', id='contents_list').find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('img', 'icon-19'):
                    continue
                # title = item.find('span','txt').text.strip()
                cnt_vol = item.find('td', 'capacity').text.strip()
                cnt_writer = item.find('td', 'nickname').text.strip()
                cnt_num = item.find('td', 'subject').find('a')['idx']
                url = 'http://disk.fileguri.com/pop.php?sm=bbs_info&idx='+cnt_num
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'fileguri',
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

            div = soup.find('div', id='paging').find_all('a')
            # print(len(div))
            if len(div) == 20:
                driver.find_element_by_xpath('//*[@id="paging"]/p/a[18]').click()
                time.sleep(2)
            else:
                driver.find_element_by_xpath('//*[@id="paging"]/p/a[19]').click()
                time.sleep(2)
    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("fileguri 크롤링 시작")
    site = ['ALL','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("fileguri 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
