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

# ==================불법 업체==================

def startCrawling(site):
    with requests.Session() as s:
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://www.filelon.com/main/storage.php',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'PHPSESSID=4mlgobeqpi3inu07uepjun1ju2; _ga=GA1.2.525518839.1547171616; _gid=GA1.2.1559732266.1547171616; __utma=30719528.525518839.1547171616.1547171616.1547171616.1; __utmc=30719528; __utmz=30719528.1547171616.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; REALUCODE=MTQuNTIuOTUuMTk5fDE1NDY0MDM2ODR8ODk5Mg%3D%3D; dspbase=; dsptarget=; idx01=3788021; tab_chk=bbs; bbs_history=%5B%5D; __utmb=30719528.14.10.1547171616; check_cookie_skidSafeFlag=Y'
        }
        i = 0;check = True
        link = "http://www.filelon.com/main/storage.php?" + site + "liststate=&list_count=&search_sort=&p="
        while check:
            i = i+1
            if i == 4:
                break
            post_one  = s.get(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            table = soup.find('table', 'table_list')
            tr = table.find('tbody').find_all("tr")
            try:
                for item in tr:
                    cnt_writer = item.find_all('td', 'kor')[1].find('span').text.strip()
                    cnt_num = item.find('input', 'list_check')['value']
                    url = 'http://www.filelon.com/main/popup.php?doc=bbsInfo&idx=' + cnt_num

                    post_two  = s.get(url)
                    soup2 = bs(post_two.text, 'html.parser')
                    table = soup2.find_all('table', 'pop_base')[1]
                    table2 = soup2.find('table', 'pop_detail').find('tbody')

                    title = soup2.find('title').text.strip().split("다운로드 > ")[1]
                    cnt_price = table.find('td', 'txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").replace(",", "").strip().split("/")[1].split("P")[0]
                    if soup2.find('b', class_=None):
                        cnt_price = soup2.find('b', class_=None).text.strip().replace(",", "").split("P")[0]
                    cnt_vol = table.find('td', 'txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", "").replace(" ", "").strip().split("/")[0]
                    cnt_fname = table2.find('tr')['title']

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filelon',
                        'Cnt_title': title,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': '0'
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

    print("filelon 크롤링 시작")
    site = ['','search_type=MOV&','search_type=DRA&','search_type=MED&','search_type=ANI&']
    for s in site:
        startCrawling(s)
    print("filelon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
