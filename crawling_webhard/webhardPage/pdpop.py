import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    cnt_chk = 0;cnt_price = 0;returnValue = []

    ul = str(soup.find('ul', 'dnld_lstcon'))
    li = soup.find('ul', 'dnld_lstcon').find_all('li')

    for item in li:
        if item.find('span', 'packet'):
            cnt_price = int(item.find('span', 'packet').text.strip().replace(',', '').split("P")[0])
        returnValue.append(cnt_price)
    for i in range(len(li)-1):
        cnt_price = returnValue[i]+cnt_price

    title = soup.find('div', 'fspop_title').find('h4').text.strip()
    fname = soup.find('ul', 'dnld_lstcon').find('span', 'sbj')['class']
    if len(fname) == 1:
        cnt_fname = soup.find('ul', 'dnld_lstcon').find_all('span', 'sbj')[0].text.strip()
    else:
        cnt_fname = soup.find('ul', 'dnld_lstcon').find_all('span', 'sbj')[1].text.strip()

    if soup.find('div', 'dnld_lstbtn').find('span', 'cine'):
        span = soup.find('div', 'dnld_lstbtn').find('span', 'cine').text.strip()
        if span.find('제휴콘텐츠') != -1:
            cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_price': cnt_price,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    link = "http://bbs.pdpop.com/board_re.php?code=F_"+site+"&nPage="
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', "shlstcon")
        li = div.find("ul").find_all("li")
        if len(li) < 2:
            check = False
            print("게시물없음\n========================")
            break
        try:
            for item in li:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cnt_vol = item.find('span', 'size').text.strip()
                cnt_writer = item.find('span', 'name').find('a').text.strip()
                cnt_num = item.find('span', 'pricedown').find('img')['id'].split("E_")[1]
                url = 'http://bbs.pdpop.com/board_re.php?mode=view&code=F_'+site+'&no='+cnt_num
                resultData = getContents(url)

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'pdpop',
                    'Cnt_title': resultData['Cnt_title'],
                    'Cnt_url': url,
                    'Cnt_price': resultData['Cnt_price'],
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : resultData['Cnt_fname'],
                    'Cnt_regdate' : now,
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

    print("pdpop 크롤링 시작")
    site = ['02','03','04']
    for s in site:
        startCrawling(s)
    print("pdpop 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
