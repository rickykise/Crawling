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
    link = "http://fileman.co.kr/contents/"+site+"&category2=&s_column=&s_word=&rows=20&show_type=0&sort=sort&page="
    print(link)
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get('http://fileman.co.kr/')
    time.sleep(3)
    driver.find_element_by_name('m_id').send_keys('up0001')
    driver.find_element_by_name('m_pwd').send_keys('up0001')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="mainLoginForm"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input').click()
    driver.find_element_by_xpath('//*[@id="mainLoginForm"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input').click()
    time.sleep(2)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))

            time.sleep(2)
            html = driver.find_element_by_class_name("boardtype1").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item.find('td', 'title').find('a')['title']
                cnt_vol = item.find('td', 'date1').text.strip()
                cnt_writer = item.find('a', 'uploader').text.strip()
                cnt_num = item.find('td', 'num').text.strip()
                url = "http://fileman.co.kr/contents/view_top.html?idx="+cnt_num

                driver.get(url)
                time.sleep(3)
                htmll = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table').get_attribute('innerHTML')
                tags = BeautifulSoup(htmll,'html.parser')
                cnt_chk = 0

                cnt_price = tags.find_all('tr')[4].find('b').text.strip().split("P")[0].replace(" ","").replace("\n","").replace("\t","").replace(",","")
                cnt_fname = tags.find('table', 'file').find_all('span', 'font_layerlist')[1].text.strip()
                if tags.find('span', style='color:#0066cc'):
                    checktext = tags.find('span', style='color:#0066cc').text.strip()
                    if checktext.find('제휴') != -1:
                        cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'fileman',
                    'Cnt_title': title,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
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

    print("fileman 크롤링 시작")
    site = ['index.htm?category1=','?category1=MVO','?category1=DRA','?category1=MED','?category1=ANI']
    for s in site:
        startCrawling(s)
    print("fileman 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
