import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(site):
    i = 0;check = True
    link = "http://www.tple.co.kr/storage/?code="+site+"&page="
    print(link)
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_class_name("storageListTable").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('td', 'txtLeft') == None:
                    continue
                adult = item.find('td', 'txtLeft').find_all('img')
                if len(adult) == 1:
                    adult = item.find('td', 'txtLeft').find('img')['src']
                    if adult.find('main_19') != -1:
                        continue
                elif len(adult) == 2:
                    adult1 = item.find('td', 'txtLeft').find_all('img')[0]['src']
                    adult2 = item.find('td', 'txtLeft').find_all('img')[1]['src']
                    if adult1.find('main_19') != -1 or adult2.find('main_19') != -1:
                        continue
                elif len(adult) == 3:
                    adult1 = item.find('td', 'txtLeft').find_all('img')[0]['src']
                    adult2 = item.find('td', 'txtLeft').find_all('img')[1]['src']
                    adult3 = item.find('td', 'txtLeft').find_all('img')[2]['src']
                    if adult1.find('main_19') != -1 or adult2.find('main_19') != -1 or adult3.find('main_19') != -1:
                        continue
                # title = item.find('td', 'txtLeft').find('a').text.strip()
                cnt_vol = item.find_all('td', 'txtSmall')[1].text.strip()
                cnt_num = item['id'].split("trListMode")[1]
                url = 'http://www.tple.co.kr/storage/?todo=view&source=W&idx='+cnt_num

                driver.get(url)
                time.sleep(2)
                htmll = driver.find_element_by_class_name('topArea').get_attribute('innerHTML')
                tags = BeautifulSoup(htmll,'html.parser')
                cnt_chk = 0

                title = tags.find('div', 'infoTitle').text.strip()
                cnt_writer = tags.find('span', id='memberLayerMenu'+cnt_num).text.strip()
                cnt_price = tags.find('div', 'infoContents').find('span', id='spanCheckFilePoint').text.strip().split("P")[0].replace(",","")
                fname = tags.find('div', 'fileListArea').find('td', 'textLeft').find('div').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip()
                if tags.find('div', 'noticeArea'):
                    text = tags.find('div', 'noticeArea').text.strip()
                    if text.find('제휴업체') != -1:
                        cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'tple',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : fname,
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

    print("tple 크롤링 시작")
    site = ['1','2','4']
    for s in site:
        startCrawling(s)
    print("tple 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
