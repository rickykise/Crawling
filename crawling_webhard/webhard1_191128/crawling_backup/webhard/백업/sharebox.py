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

    title = soup.find('div', 'view_bx').find('div', 'tit').find('li', 'tit_le').text.strip()
    cnt_price = table.find_all('td')[1].text.strip().split("P")[0].replace(",","")
    cnt_fname = soup.find('div', 'filelist').find('div', 'view_name3').text.strip()
    if soup.find('div', 'view_bx').find('div', 'tit').find('li', 'tit_le2'):
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
    link = "http://sharebox.co.kr/storage/storage.php?section="+site
    print(link)
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get(link)
    time.sleep(3)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            html = driver.find_element_by_id("contents_list").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find('table', 'ctn_list')
            tr = table.find("tbody").find_all("tr", "bbs_list")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                img = item.find('td', 'alignL clickable').find_all('img')
                if len(img) == 1:
                    adult = item.find('td', 'alignL clickable').find('img')['alt']
                    if adult.find('성인') != -1:
                        continue
                elif len(img) == 2:
                    adult1 = item.find('td', 'alignL clickable').find_all('img')[0]['alt']
                    adult2 = item.find('td', 'alignL clickable').find_all('img')[1]['alt']
                    if adult1.find('성인') != -1 or adult2.find('성인') != -1:
                        continue
                # title = item.find('span', 'mar_left10').text.strip()
                cnt_num = item.find('span', 'font11').text.strip()
                cnt_vol = item.find_all('span', 'font11')[1].text.strip()
                cnt_writer = item.find_all('td', 'alignC')[4].text.strip()
                url = 'http://sharebox.co.kr/storage/storage.php?todo=view&idx=' + cnt_num
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'sharebox',
                    'Cnt_title': resultData['Cnt_title'],
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : resultData['Cnt_fname'],
                    'Cnt_chk': resultData['Cnt_chk']
                }
                # print(data)
                # print('=========================================')

                conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                except Exception as e:
                    print(e)
                    pass
                finally :
                    conn.close()

            img = soup.find('div', 'page_nom').find_all('img')
            if len(img) == 1:
                if str(i).find('0') != -1:
                    driver.find_element_by_xpath('//*[@id="contents_list"]/div/img').click()
                    time.sleep(2)
                    i = 0
                else:
                    driver.find_element_by_xpath('//*[@id="contents_list"]/div/span['+str(i)+']').click()
            else:
                if str(i).find('0') != -1:
                    driver.find_element_by_xpath('//*[@id="contents_list"]/div/img[2]').click()
                    time.sleep(2)
                    i = 0
                else:
                    driver.find_element_by_xpath('//*[@id="contents_list"]/div/span['+str(i)+']').click()

    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("sharebox 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("sharebox 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
