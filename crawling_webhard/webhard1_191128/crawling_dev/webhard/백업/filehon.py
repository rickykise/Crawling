import requests,re
import pymysql,time,datetime
import urllib.parse
import pyautogui
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

    fname = soup.find('div', 'fileList').find('li').find('span', 'capacity').text.strip()
    cnt_fname = soup.find('div', 'fileList').find('li').text.strip().split(fname)[0]
    table = soup.find('table', 'ctnVtbl').find_all('td')[3]
    cnt_price = table.find('span', 'price').text.strip().replace(",","")
    if table.find('img'):
        cnt_chk = 1

    data = {
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://filehon.com/contents/index.php?"+site+"&show_type=0&adult_del_check=Y&cp_del_check=N&rows=20&page="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get(link)
    time.sleep(3)
    driver.find_element_by_name('m_id').send_keys('up0001')
    driver.find_element_by_name('m_pwd').send_keys('up0001')
    time.sleep(1)
    pyautogui.hotkey('enter')
    pyautogui.hotkey('enter')
    time.sleep(2)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_class_name("bbslist3").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('td', 'subject') == None:
                    continue
                title = item.find('td', 'subject').text.strip()
                cnt_vol = item.find_all('td')[4].text.strip()
                cnt_writer = item.find_all('td')[5].text.strip()
                cnt_num = item.find_all('td')[1].text.strip()
                url = "http://filehon.com/contents/view.php?idx="+cnt_num

                driver.get(url)
                time.sleep(3)
                htmll = driver.find_element_by_id('ctnView-head').get_attribute('innerHTML')
                tags = BeautifulSoup(htmll,'html.parser')
                cnt_chk = 0

                fname = tags.find('div', 'fileList').find('li').find('span', 'capacity').text.strip()
                cnt_fname = tags.find('div', 'fileList').find('li').text.strip().split(fname)[0]
                table = tags.find('table', 'ctnVtbl').find_all('td')[3]
                cnt_price = tags.find('span', 'price').text.strip()
                if table.find('img'):
                    cnt_chk = 1
                # resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filehon',
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
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("filehon 크롤링 시작")
    site = ['','category1=MVO','category1=DRA','category1=MED','category1=ANI']
    for s in site:
        startCrawling(s)
    print("filehon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
