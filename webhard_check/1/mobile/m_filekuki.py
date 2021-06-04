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
global host

LOGIN_INFO = {
    'passwd': 'up0001',
    'useridorig': 'up0001'
}

cookies = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}

def startCrawling(site):
    conn = host
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True
    with requests.Session() as s:
        login_req = s.post('https://www.filekuki.com/db/db_login.jsp', data=LOGIN_INFO, cookies=cookies)
        while check:
            i = i+1
            if i == 4:
                break
            link = "https://m.filekuki.com/mobile/mobile_list.jsp?sect="+site+"&list_type=list&s_sub=&vp="+str(i)
            post_one  = s.post(link, cookies=cookies)
            soup = bs(post_one.text, 'html.parser')
            div = soup.find_all('div', 'content')
            try:
                for item in div:
                    adult = item.find('ul')['onclick'].split("', '")[1].split("', ")[0]
                    if adult == 'Y':
                        continue
                    cnt_num = item.find('ul')['onclick'].split("contentView(")[1].split(", '")[0]
                    url = 'https://m.filekuki.com/mobile/contents_view.jsp?id='+cnt_num
                    url2 = 'http://www.filekuki.com/popup/kukicontview.jsp?id=' + cnt_num

                    post_one  = s.get(url2, cookies=cookies)
                    soup = bs(post_one.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('title').text.strip().split(" ◈")[0]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    table = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
                    cnt_price = table.split("쿠키")[0].replace(",","").strip()
                    if soup.find('img', alt='특별할인'):
                        priceCh = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
                        cnt_price = priceCh.split("→")[1].split("쿠키")[0].strip()
                    cnt_vol = table.split("/")[1].strip()
                    cnt_writer = soup.find_all('td', scope='col')[1].text.strip()
                    cnt_fname = soup.find('td', colspan='3').find('img').text.strip()
                    if soup.find('img', alt='제휴'):
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filekuki',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)

                    conn2 = host
                    try:
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn2.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_filekuki 크롤링 시작")
    site = ['','01','02','03','04']
    for s in site:
        startCrawling(s)
    print("m_filekuki 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
