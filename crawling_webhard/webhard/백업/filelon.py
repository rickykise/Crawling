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
    div = soup.find('div', id='left_contents')

    cnt_vol = div.find('table', 'pop_base').find('tbody').find('tr').find_all('td')[1].text.replace("\n","").replace("\t","").split("/")[0].strip()
    cnt_fname = soup.find('table', 'pop_detail').find('tbody').find('tr')['title']
    thead = div.find('table', 'pop_base').find('thead').find('tr').find('th').find_all('span')
    if len(thead) == 1:
        title = div.find('table', 'pop_base').find('thead').find('tr').find('th').find_all('span')[0].text.strip()
    else:
        title = div.find('table', 'pop_base').find('thead').find('tr').find('th').find_all('span')[1].text.strip()
    # print(title)

    data = {
        'Cnt_title': title,
        'Cnt_vol': cnt_vol,
        'Cnt_fname' : cnt_fname
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.filelon.com/main/storage.php?" + site + "liststate=&list_count=&search_sort="
    print(link)
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get(link)
    time.sleep(3)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            html = driver.find_element_by_id("list_sort").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('td', 'tit').find('span', 'adult19') != None:
                    continue
                # title = item.find('div', 'bbsTitle_1').text.strip()
                cnt_price = item.find('td', 'eng').find('span', 'coin_btxt').text.strip().split("P")[0].replace(",","")
                cnt_writer = item.find_all('td')[4].find('span').text.strip()
                cnt_num = item.find('td').find('div').find('input')['value']
                url = 'http://www.filelon.com/main/popup.php?doc=bbsInfo&idx=' + cnt_num
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filelon',
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

            div = soup.find('div', 'list_n_menu').find_all('a')
            # print(len(div))
            if len(div) == 12:
                driver.find_element_by_xpath('//*[@id="list_sort"]/div[2]/div/div/a[11]').click()
                time.sleep(2)
            else:
                driver.find_element_by_xpath('//*[@id="list_sort"]/div[2]/div/div/a[12]').click()
                time.sleep(2)
    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("filelon 크롤링 시작")
    site = ['','search_type=MOV&','search_type=DRA&','search_type=MED&','search_type=ANI&']
    for s in site:
        startCrawling(s)
    print("filelon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
