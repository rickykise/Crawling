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
    'm_id': 'CVGcsfoTFRkXrojtgppmFPpNEc4/bwvFHI+XFBpLHZw=',
    'm_pwd': '0zECSuUdpqBGKRETou9pEw=='
}

def startCrawling(site):
    i = 0;a = 1;check = True
    link = "http://smartfile.co.kr/contents/contents_list_inc.php"
    while check:
        with requests.Session() as s:
            headers = {'Cookie': 'disp_side=Y; SAVED_PW=N; 046dd99d5c62a46485c88ba0022a8fa7=ZW5qb3kxMUBuYXZlci5jb20%3D; SAVED_ID2=N; SAVED_ID=N; wcs_bt=79d0ffc89b3d5:1561337379; _ga=GA1.3.1715228641.1560152123; PHPSESSID=j3h2sq62knce5i7bjlp64ju810; _gid=GA1.3.281777038.1561336706; _gat=1; 762923a460671e5fbf8c4215c65f969e=b2s%3D; 7b0596d2e793be34d2366c836163650f=MA%3D%3D; mecross_box_3333=17822093; storm_sale=F; Nnum=2; 9156b2c986b1eaf93a874d568b93d16d=MTU2MTQyMzMxNQ%3D%3D; 07099283cfc31f2d473bf5b4628ab3a6=VjFST2MySXhjRVZWVkZaTllXdHJlRlJyVFRCbFJURkZWMWhXVGxaRlZqUlhSRVpYVmtaS1YxTnJjRk5TYW1nMFZHNXdibVZWTVhGUlZGWk9aSG93T1E9PQ%3D%3D; 36478754c7023054f291ec39b489451c=ZjNiYTExMzYxN2IyMjYwMWM0OTI4YWEzZWNkOTJlNTY%3D; 1308190361fc32582bb2d826ace35be5=WQ%3D%3D'}
            login_req = s.post('http://smartfile.co.kr/member/loginCheck.php', data=LOGIN_INFO)

            post_one  = s.post('http://smartfile.co.kr/index.php')
            soup = bs(post_one.text, 'html.parser')
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
            try:
                for item in text:
                    if a == 25:
                        a = 1
                        break
                    cnt_num = text.split('"id":"')[a].split('","')[0]
                    adult = text.split('"flag_adult":"')[a].split('","')[0]
                    a = a+1
                    url = 'http://smartfile.co.kr/contents/view.php?idx='+cnt_num
                    if adult == '1':
                        continue

                    r = s.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    table = soup.find('table', summary='컨텐츠정보표').find('tbody')
                    cnt_chk = 0

                    title = soup.find('title').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('smartfile',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('smartfile',title,title_null,url)
                    #     continue
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
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    print(data)
                    print('============================================')

                    # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("smartfile 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("smartfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
