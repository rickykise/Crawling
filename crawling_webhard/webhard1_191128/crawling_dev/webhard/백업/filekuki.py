import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

#-------------------파일쿠키 드라이버 설치해야됨------------------------------------

def startCrawling(site):
    i = 0;check = True
    link = "https://www.filekuki.com/kuki/kuki.jsp?category="+site+"&vp="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get('http://www.filekuki.com/')
    time.sleep(3)
    driver.switch_to_frame('main')
    page_source = driver.page_source
    driver.find_element_by_name('useridorig').send_keys('up0001')
    driver.find_element_by_name('passwd').send_keys('up0001')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="loginSubmit"]').click()
    time.sleep(2)
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(3)
            driver.switch_to_frame('main')
            page_source = driver.page_source
            soup = BeautifulSoup(page_source,'html.parser')
            div = soup.find('div', id='rank_movie')
            tr = div.find("tbody").find_all("tr", align='center')
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('td').find('img'):
                    continue
                title = item.find('td').find('span').text.strip()
                cnt_num = item.find('td').find('a')['onclick'].split("openDnWin(")[1].split(",")[0]
                url = 'http://www.filekuki.com/popup/kukicontview.jsp?id=' + cnt_num
                cnt_vol = item.find_all('td')[1].text.strip()

                driver.get(url)
                time.sleep(3)
                htmll = driver.find_element_by_id('contview_wrap').get_attribute('innerHTML')
                tags = BeautifulSoup(htmll,'html.parser')
                tr = tags.find('tbody').find_all('tr')[1]
                tr2 = tags.find('tbody').find_all('tr')[2]
                cnt_chk = 0

                cnt_writer = tr.find_all('td')[1].text.strip()
                cnt_fname = tr2.find('td').text.strip()
                cnt_price = tr.find_all('td')[0].text.replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","").strip()
                if tr.find_all('td')[0].find('img'):
                    cnt_price = cnt_price.split("→")[1].split("쿠키")[0]
                else:
                    cnt_price = cnt_price.split("쿠키")[0]

                if tags.find('p', 'ico_coop'):
                    cnt_chk = 1
                # resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filekuki',
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

    print("filekuki 크롤링 시작")
    site = ['&o_category=0','01','02','03','04']
    for s in site:
        startCrawling(s)
    print("filekuki 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
