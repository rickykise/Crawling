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

def startCrawling(site):
    with requests.Session() as s:
        i = 0; a = 1;check = True
        link = 'http://disk.fileguri.com/main/module/bbs_list_sphinx_prc.php?mode=fileguri&list_row=20&page='
        link2 = '&search_type='+site+'&search_type2=title&sub_sec=&search=&hide_adult=Y&blind_rights=N&sort_type=&plans_idx='
        while check:
            i = i+1
            if i == 4:
                break
            post_one  = s.get(link+str(i)+link2)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            tr = soup.find_all('tr')
            try:
                for item in text:
                    cnt_numCh = text.split("idx='")[a].split("'")[0]
                    cnt_num = cnt_numCh.split('"')[1].split('\\')[0]
                    url = 'http://disk.fileguri.com/pop.php?sm=bbs_info&idx='+cnt_num
                    a = a+1
                    if a == 21:
                        a = 1

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    cnt_chk = 0

                    title = soup.find('div', 'ctvTitle').find('span').text.strip()
                    cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().replace(",","")
                    span = soup.find('span', 'capacity').text.strip()
                    cnt_fname = soup.find('div', 'bxSkin').find('li').text.split(span)[0].strip()
                    cnt_writer = soup.find('a', id='js-infoLayer-btn').text.strip()
                    cnt_vol = soup.find('table', 'ctvTbl').find('tbody').find_all('td')[1].text.strip()

                    if soup.find('p', 'careMsg'):
                        cnt_chkCh = soup.find('p', 'careMsg').text.strip()
                        if cnt_chkCh.find('제휴') != -1:
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'fileguri',
                        'Cnt_title': title,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
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

    print("fileguri 크롤링 시작")
    site = ['ALL','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("fileguri 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
