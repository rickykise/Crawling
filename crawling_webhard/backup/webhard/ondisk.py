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

    if soup.find('div', id='loadingBar'):
        data = '삭제'
    else:
        title = soup.find('span', 'tit_txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(" ", "").strip()
        cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().replace(",","")
        span = soup.find('div', 'bxSkin').find('ul').find('li').find('span').text.strip()
        cnt_fname = soup.find('div', 'bxSkin').find('ul').find('li').text.replace("\n","").replace("\t","").replace("\xa0", "").strip().split(span)[0]

        if soup.find('div', 'ctvTitle').find('h2').find('img'):
            img = soup.find('div', 'ctvTitle').find('h2').find('img')['src']
            if img.find('icon_partnership') != -1:
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
    link = "http://ondisk.co.kr/index.php?mode=ondisk&search_type="+site+"&page="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            # if i == 4:
            #     break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id('js-bbslist').get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody", id="contents_list").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break
            try:
                for item in tr:
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if item.find('td', 'subject').find('a')['onclick'].find("winBbsInfo") != -1:
                        cnt_num = item.find('td', 'subject').find('a')['onclick'].split("winBbsInfo('")[1].split("','")[0]
                        url = 'http://ondisk.co.kr/pop.php?sm=bbs_info&idx=' + cnt_num
                        cnt_vol = item.find('td', 'capacity').text.strip()
                        cnt_writer = item.find('td', 'nickname').text.strip()
                        resultData = getContents(url)
                    else:
                        continue

                    if resultData == '삭제':
                        continue

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'ondisk',
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
            except:
                continue

    # except:
    #     pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("ondisk 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("ondisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
