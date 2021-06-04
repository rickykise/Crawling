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

    try:
        price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip()
        if price.find('\n') != -1:
            cnt_price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip().split("\n")[1].split("P")[0].replace(",","")
        else:
            cnt_price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip().split("P")[0].replace(",","")
        cnt_writer = soup.find_all('td', 'tdspan')[5].text.strip()
        cnt_fname = soup.find('tr', id='filedef').find_all('tr')[1].find_all('td')[0].text.strip()

        if soup.find('img', src='http://wimg.fileham.com/popup/new/dc_title_al.png'):
            cnt_chk = 1

        data = {
            'Cnt_price': cnt_price,
            'Cnt_writer' : cnt_writer,
            'Cnt_fname' : cnt_fname,
            'Cnt_chk': cnt_chk
        }
    except:
        pass
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://www.fileham.com/main/storage.php?section="+site
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
            tr = soup.find("tbody").find_all("tr", id="bbs_list")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                adult = item.find('div', 'ellipsis').find_all('img')
                if len(adult) == 1:
                    pass
                elif adult[1]['alt'] == '성인자료':
                    continue
                title = item.find('span', 'bbsTitleAll bold').text.strip()
                cnt_vol = item.find_all('td')[4].text.strip()
                cnt_num = item['data-idx']
                url = 'http://www.fileham.com/main/popup.php?doc=bbsInfo&idx='+cnt_num
                resultData = getContents(url)

                if resultData == None:
                    print('삭제게시물')
                    continue

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'fileham',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : resultData['Cnt_writer'],
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

            div = soup.find('table', id='paging').find_all('td')
            # print(len(div))
            if len(div) == 19:
                driver.find_element_by_xpath('//*[@id="paging"]/tbody/tr/td[17]').click()
                time.sleep(2)
            elif len(div) == 20:
                driver.find_element_by_xpath('//*[@id="paging"]/tbody/tr/td[18]').click()
                time.sleep(2)
            else:
                driver.find_element_by_xpath('//*[@id="paging"]/tbody/tr/td[19]').click()
                time.sleep(2)

    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("fileham 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("fileham 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
