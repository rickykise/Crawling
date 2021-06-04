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

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    table = soup.find('table', 'view_tb')
    cnt_chk = 0

    title = soup.find('div', 'view_bx').find('div', 'tit').find('li', 'tit_le').text.strip()
    cnt_writer = table.find('span', 'bold mar_rig5').text.strip()
    cnt_vol = table.find_all('td')[3].text.strip()
    cnt_price = table.find_all('td')[1].text.strip().split("P")[0].replace(",","")
    cnt_fname = soup.find('div', 'filelist').find('div', 'view_name3').text.strip()
    if soup.find('div', 'view_bx').find('div', 'tit').find('li', 'tit_le2'):
        cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_fname' : cnt_fname,
        'Cnt_writer' : cnt_writer,
        'Cnt_vol' : cnt_vol,
        'Cnt_price' : cnt_price,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

LOGIN_INFO = {
    'backurl': 'Lw==',
    'caller': 'main',
    'flag_saveid': 'on',
    'securityLoin': '1',
    'site_set': 'sharebox',
    'todo': 'exec',
    'userid': 'up0001',
    'userpw': 'up0001',
    'webs': ''
}

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0; check = True
    with requests.Session() as s:
        login_req = s.post('https://ssl.filekok.com/loginClass.php', data=LOGIN_INFO)
        headers = {'Cookie': '_ga=GA1.3.2033550487.1545813582; _gid=GA1.3.1833979890.1545813582; PHPSESSID=ibn5eu8aujauiddak7s4jm1n04; SHL=MTU0NTg3NzIzMA%3D%3D; CUC=dXAwMDAx; auth500_event=1; _gat=1'}
        post_one  = s.post('http://sharebox.co.kr/', headers=headers)
        soup = bs(post_one.text, 'html.parser')

        while check:
            Page = {
                'adultEx': 'adultEx',
                'list_scale': '100',
                'section': site,
                'start': i
            }
            with requests.Session() as s:
                headers2 = {'Cookie': '_ga=GA1.3.2033550487.1545813582; _gid=GA1.3.1833979890.1545813582; PHPSESSID=ibn5eu8aujauiddak7s4jm1n04; SHL=MTU0NTg3NzIzMA%3D%3D; CUC=dXAwMDAx; auth500_event=1; coupon=; _gat=1'}
                post_two  = s.post('http://sharebox.co.kr/storage/list_db.php', data=Page, headers=headers2)
                soup = bs(post_two.text, 'html.parser')
                i = i+25
                if i == 100:
                    break
                input = soup.find_all('input', 'chk_node')

                try:
                    for item in input:
                        cnt_num = item['value']
                        url = 'http://sharebox.co.kr/storage/storage.php?todo=view&idx=' + cnt_num
                        resultData = getContents(url)
                        title_null = titleNull(resultData['Cnt_title'])
                        # 키워드 체크
                        getKey = getKeyword(conn,curs)
                        keyCheck = checkTitle(title_null, getKey)
                        if keyCheck['m'] == None:
                            continue
                        keyCheck2 = checkTitle2(title_null, getKey)
                        if keyCheck2['m'] == None:
                            continue

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'sharebox',
                            'Cnt_title': resultData['Cnt_title'],
                            'Cnt_title_null': title_null,
                            'Cnt_url': url,
                            'Cnt_price': resultData['Cnt_price'],
                            'Cnt_writer' : resultData['Cnt_writer'],
                            'Cnt_vol' : resultData['Cnt_vol'],
                            'Cnt_fname' : resultData['Cnt_fname'],
                            'Cnt_chk': resultData['Cnt_chk']
                        }
                        # print(data)

                        conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                        try:
                            curs = conn.cursor(pymysql.cursors.DictCursor)
                            dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                        except Exception as e:
                            print(e)
                            pass
                        finally :
                            conn.close()
                except:
                    continue

if __name__=='__main__':
    start_time = time.time()

    print("sharebox 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("sharebox 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
