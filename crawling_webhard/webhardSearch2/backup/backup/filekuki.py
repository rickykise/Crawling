import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

#-------------------파일쿠키 드라이버 설치해야됨------------------------------------

LOGIN_INFO = {
    'passwd': 'up0001',
    'useridorig': 'up0001'
}

def getContents(url):
    with requests.Session() as s:
        login_req = s.post('https://www.filekuki.com/db/db_login.jsp')
        headers = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}
        post_one  = s.get(url, headers=headers)
        # time.sleep(2)
        soup = bs(post_one.text, 'html.parser')
        cnt_chk = 0
        # print(soup)

        title = soup.find('title').text.strip().split(" ◈")[0]
        aaa = soup.find('title').text.strip()
        table = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
        cnt_price = table.split("쿠키")[0].replace(",","").strip()
        if soup.find('img', alt='특별할인'):
            priceCh = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
            cnt_price = priceCh.split("→")[1].split("쿠키")[0].strip()
        cnt_writer = soup.find_all('td', scope='col')[1].text.strip()
        cnt_fname = soup.find('td', colspan='3').find('img').text.strip()
        # if soup.find('img', alt='폴더'):
        #     cnt_fname = soup.find('td', colspan='3').find('img').text.strip()
        if soup.find('img', alt='제휴'):
            cnt_chk = 1

        data = {
            'Cnt_title' : title,
            'Cnt_price': cnt_price,
            'Cnt_writer' : cnt_writer,
            'Cnt_fname' : cnt_fname,
            'Cnt_chk': cnt_chk
        }
        return data

def startCrawling(site):
    i = 0; a = 1;check = True
    with requests.Session() as s:
        login_req = s.post('https://www.filekuki.com/db/db_login.jsp')
        headers = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}
        post_one  = s.get('http://www.filekuki.com/', headers=headers)
        # time.sleep(2)
        while check:
            i = i+1
            if i == 4:
                break
            link = "https://www.filekuki.com/kuki/kuki.jsp?category="+site+"&vp="
            post_one  = s.post(link+str(i))
            # time.sleep(2)
            soup = bs(post_one.text, 'html.parser')
            if soup.find('body onload') != -1:
                post_one  = s.post(link+str(i))
                time.sleep(2)
                soup = bs(post_one.text, 'html.parser')
            div = soup.find('div', id="rank_movie")
            tr = div.find("tbody").find_all("tr", align='center')
            try:
                for item in tr:
                    adult = item.find('a')['onclick'].split("', '")[1].split("', ")[0]
                    if adult == 'Y':
                        continue
                    cnt_num = item.find('a')['onclick'].split('openDnWin(')[1].split(', ')[0]
                    url = 'http://www.filekuki.com/popup/kukicontview.jsp?id=' + cnt_num
                    cnt_vol = item.find_all('td')[1].text.strip()
                    resultData = getContents(url)

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filekuki',
                        'Cnt_title': resultData['Cnt_title'],
                        'Cnt_url': url,
                        'Cnt_price': resultData['Cnt_price'],
                        'Cnt_writer' : resultData['Cnt_writer'],
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : resultData['Cnt_fname'],
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

if __name__=='__main__':
    start_time = time.time()

    print("filekuki 크롤링 시작")
    site = ['','01','02','03','04']
    for s in site:
        startCrawling(s)
    print("filekuki 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
