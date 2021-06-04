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

LOGIN_INFO = {
    'passwd': 'up0001',
    'useridorig': 'up0001'
}

cookies = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}

def startCrawling(key):
    i = 0; a = 1;check = True
    print(key)
    encText = urllib.parse.quote(key)
    with requests.Session() as s:
        login_req = s.post('https://www.filekuki.com/db/db_login.jsp', data=LOGIN_INFO, cookies=cookies)
        while check:
            i = i+1
            if i == 4:
                break
            link = 'https://www.filekuki.com/kuki/kuki_search.jsp?category=&o_category=&linesperpage=20&cate_ds=0&pd=&s_sub=&ps=&wordtype2=21&wordtype=21&cpr=&chk_disabled=&search_word=&rc=20&vp=1&dcnaland=&qry='+encText+'&vp='
            post_one  = s.post(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            if str(soup).find('대한 검색 결과가 없습니다.') != -1:
                break
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

                    post_one  = s.get(url, cookies=cookies)
                    soup = bs(post_one.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('title').text.strip().split(" ◈")[0]
                    title_null = titleNull(title)
                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('filekuki',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('filekuki',title,title_null,url)
                    #     continue
                    aaa = soup.find('title').text.strip()
                    table = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
                    cnt_price = table.split("쿠키")[0].replace(",","").strip()
                    if soup.find('img', alt='특별할인'):
                        priceCh = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
                        cnt_price = priceCh.split("→")[1].split("쿠키")[0].strip()
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

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("filekuki 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("filekuki 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
