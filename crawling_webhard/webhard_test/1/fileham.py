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
    soup = BeautifulSoup(c.decode('euc-kr','replace'),"html.parser")
    cnt_chk = 0

    title = soup.find('title').text.strip()
    cnt_vol = soup.find_all('td', 'tdspan')[3].find_all('span')[1].text.split("/ ")[1].strip()
    price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip()
    if price.find('\n') != -1:
        cnt_price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip().split("\n")[1].split("P")[0].replace(",","")
    else:
        cnt_price = soup.find_all('td', 'tdspan')[3].find_all('span')[0].text.strip().split("P")[0].replace(",","")
    cnt_writer = soup.find_all('td', 'tdspan')[5].text.strip()
    cnt_fname = soup.find('tr', id='filedef').find_all('tr')[1].find_all('td')[0].text.strip()

    if soup.find('img', src='http://wimg.fileham.com/popup/new/dc_title_al.png'):
        cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_price': cnt_price,
        'Cnt_writer' : cnt_writer,
        'Cnt_vol' : cnt_vol,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        link = "http://www.fileham.com/main/storage.php?section="+site+"&list_count=100&p="
        while check:
            i = i+1
            if i == 4:
                break
            post_one  = s.post(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find_all('tr', id='bbs_list')
            try:
                for item in tr:
                    adult = item.find('td', align='left')['onclick'].split("','")[1].split("'")[0]
                    if adult == '1':
                        continue
                    cnt_num = item['data-idx']
                    url = 'http://www.fileham.com/main/popup.php?doc=bbsInfo&idx='+cnt_num
                    try:
                        resultData = getContents(url)
                    except:
                        continue

                    title_null = titleNull(resultData['Cnt_title'])
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('fileham',resultData['Cnt_title'],title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('fileham',resultData['Cnt_title'],title_null,url)
                        continue

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'fileham',
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

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("fileham 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("fileham 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
