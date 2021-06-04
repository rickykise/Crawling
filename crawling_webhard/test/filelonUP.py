import pymysql
import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='sms@unionc',db='otogreen',port=3306,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#DB 업데이트 함수
def dbUpdate(cnt_price,url):
    sql = "UPDATE cnt_all SET cnt_price=%s WHERE cnt_url=%s;"
    curs.execute(sql,(cnt_price,url))
    conn.commit()

# url 가져오는 함수
def getSearchUrl():
    with conn.cursor() as curs:
        sql = "select cnt_url, cnt_osp from cnt_all where cnt_price = '다운로드' and cnt_osp = 'filekok' order by cnt_regdate asc;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in returnValue:
                returnValue[key].append(result[i][1])
            else:
                returnValue.update({key:[result[i][1]]})
        # print(returnValue)

        return returnValue

def startCrawling(url):
    try:
        token = ''
        with requests.Session() as s:
            Page = {
                'act': 'get_token'
            }
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'http://www.filekok.com',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            login_token = s.post('http://www.filekok.com/ajax_controller.php', data=Page, headers=headers)
            soup = bs(login_token.text, 'html.parser')
            text = str(soup)
            token = text.split('{"result":"')[1].split('","')[0]

            LOGIN_INFO = {
                    'browser': 'pc',
                    'isSSL': 'Y',
                    'mb_id': 'up0001',
                    'mb_pw': 'up0001',
                    'repage': 'reload',
                    'token': token,
                    'url': '/main/module/loginClass.php',
                    'url_ssl': 'https://ssl.filekok.com/loginClass.php'
            }
            login_req = s.post('https://ssl.filekok.com/loginClass.php', data=LOGIN_INFO, headers=headers)
            post_one  = s.post(url, headers=headers)
            soup = bs(post_one.text, 'html.parser')

            cnt_price = soup.find_all('td', 'txt')[4].text.replace("\n","").replace("\t","").replace(" ","").replace(",","").strip().split(" / ")[1].split("P")[0]
            if soup.find('span', 'half_arrow'):
                cnt_price = soup.find_all('b', class_=False)[2].text.strip().replace(",","").split("P")[0]

            dbUpdate(cnt_price, url)
            print(url)
            print(cnt_price)
            print('========================================')
    except:
        pass

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl()
    print("filonTest check 크롤링 시작")
    for u in getUrl.keys():
        startCrawling(u)
    print("filonTest check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
