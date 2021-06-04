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
    'Frame_login': 'Ok',
    'keep': 'Y',
    'm_id': 'up0001@naver.com',
    'm_pwd': 'up0001'
}

def startCrawling(site):
        i = 0;a = 1;check = True
        link = "http://smartfile.co.kr/contents/contents_list_inc.php"
        while check:
            with requests.Session() as s:
                headers = {'Cookie': '_ga=GA1.3.1815700316.1545894808; PHPSESSID=ajgp9p5oobd0m23e6do6v9fq67; _gid=GA1.3.1732146722.1548318471; 7b0596d2e793be34d2366c836163650f=MA%3D%3D; 046dd99d5c62a46485c88ba0022a8fa7=dXAwMDAxQG5hdmVyLmNvbQ%3D%3D; Nnum=1; d994c3d58197ed689769fa93d904018a=MTU0ODQwNDkxNw%3D%3D; mecross_box_3333=17818634; storm_sale=F; wcs_bt=79d0ffc89b3d5:1548318599; _gat=1'}
                login_req = s.post('http://smartfile.co.kr/member/loginCheck.php', data=LOGIN_INFO, headers=headers)
                post_one  = s.post('http://smartfile.co.kr/index.php', headers=headers)

                Page = {
                    'category1': site,
                    'category2': '',
                    'chkcopy': '',
                    'limit': '0',
                    'opr': 'true',
                    'page': i,
                    'page_su': '10',
                    's_word': '',
                    'sort1': '',
                    'sort2': '',
                    'type': 'json',
                    'uploader': ''
                }
                i = i+1
                if i == 4:
                    break
                post_one  = s.post(link, data=Page)
                soup = bs(post_one.text, 'html.parser')
                text = str(soup)
                # try:
                for item in text:
                    if a == 25:
                        a = 1
                    cnt_num = text.split('"id":"')[a].split('","')[0]
                    adult = text.split('"flag_adult":"')[a].split('","')[0]
                    a = a+1
                    url = 'http://smartfile.co.kr/contents/view.php?idx='+cnt_num
                    if adult == '1':
                        continue

                    r = s.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    print(soup)
                    table = soup.find('table', summary='컨텐츠정보표').find('tbody')
                    cnt_chk = 0

                    title = soup.find('title').text.strip()
                    cnt_price = table.find_all('td')[2].find('span').text.strip().split("P")[0].replace(",","")
                    cnt_vol = table.find_all('td')[2].text.strip().replace(" ","").split("/")[0]
                    cnt_writer = table.find_all('td')[3]['onclick'].split("', '")[1].split("', '")[0]
                    cnt_fname = soup.find('span', 'file_name').text.strip()
                    if table.find_all('td')[2].find('img'):
                        jehu = table.find_all('td')[2].find('img')['title']
                        if jehu == '제휴':
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'smartfile',
                        'Cnt_title': title,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    print(data)

                        # conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                        # try:
                        #     curs = conn.cursor(pymysql.cursors.DictCursor)
                        #     dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                        # except Exception as e:
                        #     print(e)
                        #     pass
                        # finally :
                        #     conn.close()
                # except:
                #     continue

if __name__=='__main__':
    start_time = time.time()

    print("smartfile 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("smartfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
