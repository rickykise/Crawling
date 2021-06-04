import requests,re
import pymysql,time,datetime
import urllib.parse
from commonFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : ",key)
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        i = 0;
        regex = re.compile(r'\d{4}-\d+-\d+ \d+:\d+:\d+')
        insertNum = 0; ninsertNum = 0;paramKey = None;check = False
        if key == '공유' or key == '정유미': paramKey = key
        link = "https://www.ygosu.com/all_search/?type=board&add_search_log=Y&keyword="+key+"&order=1&page="
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link+str(i+1))
        time.sleep(2)
        html = driver.find_element_by_class_name("rst_detail").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        li = soup.find('ul', 'type_board2').find_all("li",class_=False)

        for item in li:
            conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if(item.find('li','default_body') == None):
                title = item.find('li','thumbnail_body').find('a').text.strip()
                url = item.find('li','thumbnail_body').find('a')['href']
                datecheck = item.find('li','thumbnail_body').find('span').text
                board_number = url.split("idx=")[1]
            else:
                title = item.find('li','default_body').find('a').text.strip()
                url = item.find('li','default_body').find('a')['href']
                datecheck = item.find('li','default_body').find('span').text
                board_number = url.split("idx=")[1]
            if datecheck < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
            # if datecheck < '2018-06-03': check=False;break
            driver.get(url)
            time.sleep(2)
            page_main = driver.find_element_by_class_name("board_body").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            [s.extract() for s in tags('script')]
            writer = tags.find('div', 'nickname').find('a').text
            ip = tags.find('div', 'ipadd').text.split("IP : ")[1].strip()
            date = tags.find('div', 'date').text.split(": ")[1].split(" /")[0].strip()
            # content = tags.find('div','container').text.replace("\n","").replace("\t","").replace("\xa0", "")
            print(writer)
            try:
                data = {
                    'title' : title,
                    'url' : url,
                    'contents' : '',
                    'date': date,
                    'writer': writer,
                    'ip': ip,
                    'board_number':  board_number
                }
                # print(data)
            except:
                continue
            result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
            if result:
                conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'ygosu',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=True;break
                finally :
                    conn.close()
            # if(driver.find_element_by_class_name("board_body").get_attribute('innerHTML') == None):
            #     page_main = driver.find_element_by_class_name("container").get_attribute('innerHTML')
            #     tags = BeautifulSoup(page_main,'html.parser')
            #     [s.extract() for s in tags('script')]
            #     content = tags.find('div', 'content').text.replace("\n","").replace("\t","")
            #     print(content)
                # if(content.find('원하시는') != -1):
                #     break
            # else:
            #     page_main = driver.find_element_by_class_name("board_body").get_attribute('innerHTML')
            #     tags = BeautifulSoup(page_main,'html.parser')
            #     writer = tags.find('div', 'nickname').find('a').text
            #     ip = tags.find('div', 'ipadd').text.split("IP : ")[1].strip()
            #     date = tags.find('div', 'date').text.split(": ")[1].split(" /")[0].strip()
                # co = tags.find('div', 'container').find_all('p',class_=False)
                # [s.extract() for s in tags('script')]
                # for content in co:
                #     cco = content.text.replace("\n","").replace("\t","")
                #     print(cco)

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("ygosu 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '아이유':
            startCrawling(k)
        # startCrawling(k)
    print("ygosu 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
