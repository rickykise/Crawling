import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

#-------------------빅파일 드라이버 설치해야됨------------------------------------

def startCrawling(site):
    i = 0;check = True
    link = "http://www.bigfile.co.kr/content/ajax_db_exod.php?sEg=Y&pg="
    link2 = "&total_count=66567&outmax=20&s_field=S_TOTAL&cateGory=000"+ site
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i)+link2)
            time.sleep(2)
            html = driver.find_element_by_xpath("/html/body/table[1]").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break
            try:
                for item in tr:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    td = item.find_all('td')
                    if len(td) == 1:
                        continue

                    img = item.find_all('td')[2].find_all('img')
                    if len(img) == 1:
                        adult = item.find_all('td')[2].find('img')['src']
                        if adult.find('adult') != -1:
                            continue
                    elif len(img) == 2:
                        adult1 = item.find_all('td')[2].find_all('img')[0]['src']
                        adult2 = item.find_all('td')[2].find_all('img')[1]['src']
                        if adult1.find('adult') != -1 or adult2.find('adult') != -1:
                            continue
                    elif len(img) == 3:
                        adult1 = item.find_all('td')[2].find_all('img')[0]['src']
                        adult2 = item.find_all('td')[2].find_all('img')[1]['src']
                        adult3 = item.find_all('td')[2].find_all('img')[2]['src']
                        if adult1.find('adult') != -1 or adult2.find('adult') != -1 or adult3.find('adult') != -1:
                            continue
                    elif len(img) == 4:
                        adult1 = item.find_all('td')[2].find_all('img')[0]['src']
                        adult2 = item.find_all('td')[2].find_all('img')[1]['src']
                        adult3 = item.find_all('td')[2].find_all('img')[2]['src']
                        adult4 = item.find_all('td')[2].find_all('img')[3]['src']
                        if adult1.find('adult') != -1 or adult2.find('adult') != -1 or adult3.find('adult') != -1 or adult4.find('adult') != -1:
                            continue
                    elif len(img) == 5:
                        adult1 = item.find_all('td')[2].find_all('img')[0]['src']
                        adult2 = item.find_all('td')[2].find_all('img')[1]['src']
                        adult3 = item.find_all('td')[2].find_all('img')[2]['src']
                        adult4 = item.find_all('td')[2].find_all('img')[3]['src']
                        adult5 = item.find_all('td')[2].find_all('img')[4]['src']
                        if adult1.find('adult') != -1 or adult2.find('adult') != -1 or adult3.find('adult') != -1 or adult4.find('adult') != -1 or adult5.find('adult') != -1:
                            continue

                    title = item.find_all('a')[0]['title']
                    urlCh = item.find_all('a')[0]['href'].split("('")[1].split("','")[0]
                    cnt_chk = 0
                    if title.find('요청자료') != -1:
                        title = item.find_all('a')[1]['title']
                        urlCh = item.find_all('a')[1]['href'].split("('")[1].split("','")[0]
                    elif title.find('제휴업체') != -1:
                        title = item.find_all('a')[1]['title']
                        urlCh = item.find_all('a')[1]['href'].split("('")[1].split("','")[0]
                        cnt_chk = 1
                    cnt_num = item.find('td', 'conlist_s').text.strip()
                    url = 'http://www.bigfile.co.kr' + urlCh + '#top'
                    cnt_vol = item.find_all('td', 'conlist_s')[1].text.strip()
                    cnt_writer = item.find('td', 'conlist_id').text.strip()

                    driver.get(url)
                    time.sleep(2)
                    htmll = driver.find_element_by_class_name('info').get_attribute('innerHTML')
                    tags = BeautifulSoup(htmll,'html.parser')
                    cnt_price = tags.find('li', 'gm ar02').text.strip().split(" 캐시")[0].replace(",","")
                    cnt_fname = tags.find('div', id='pp_fileinfo').find('tr').find('td')['title']

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'bigfile',
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
                continue
    # except:
    #     pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("bigfile 크롤링 시작")
    site = ['1','2','3','5']
    for s in site:
        startCrawling(s)
    print("bigfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
