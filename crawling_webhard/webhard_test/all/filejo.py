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
    cnt_chk = 0

    title = soup.find('title').text.strip()
    cnt_vol = soup.find_all('td', 'black_a_s')[2].text.replace("\n","").replace("\t","").replace("\xa0", "").replace(",","").split("/")[0].strip()

    cnt_price = soup.find_all('td', 'black_a_s')[2].find('font').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(",","").strip().split("P")[0]

    if cnt_price.find('↓') != -1:
        cnt_price = soup.find_all('td', 'black_a_s')[2].find_all('font')[1].text.replace("\n","").replace("\t","").replace("\xa0", "").replace(",","").strip().split("P")[0]

    # cnt_fname = soup.find_all('td', 'black_a_s')[3]['title']
    if soup.find('td', 'brown_b').find('img'):
        img = soup.find('td', 'brown_b').find('img')['src']
        if img == 'http://wimg.filejo.com/icon/icon_join_info2.gif':
            cnt_chk = 1

    data = {
        'Cnt_title': title,
        'Cnt_vol' : cnt_vol,
        # 'Cnt_fname' : cnt_fname,
        'Cnt_price' : cnt_price,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def getFname(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    str1 = soup.find_all('td', 'str1')
    if len(str1) == 1:
        cnt_fname = soup.find('td', 'str1').text.strip()
    elif len(str1) == 2:
        cnt_fname = soup.find_all('td', 'str1')[1].text.strip()
    elif len(str1) == 3:
        cnt_fname = soup.find_all('td', 'str1')[2].text.strip()

    return cnt_fname


def startCrawling(site):
    i = 0;check = True
    link = "http://www.filejo.com/main/storage.php?section="+site+"&p="
    # link = "http://www.filejo.com/main/doc/storage/list_div.php?section="+site+"&p="
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find_all('tr')
        returnValue = []
        urlCheck = ""

        for item in tr:
            cnt_writer = item.find('td', width='60')
            if cnt_writer == None:
                continue
            else:
                cnt_writer = item.find('td', width='60').text.split("..")[0].strip()
                returnValue.append(cnt_writer)
        del returnValue[0]
        del returnValue[1]
        count = 0

        try:
            for item in tr:
                if item.find('a'):
                    if item.find('a')['href'] == "#null":
                        cnt_num = item.find('a')['onclick'].split("('")[1].split("','")[0]
                        adult = item.find('a')['onclick'].split("','")[1].split("')")[0]
                        if urlCheck == cnt_num:
                            continue
                        urlCheck = cnt_num
                        if adult == '1':
                            count += 1
                            continue
                        url = 'http://www.filejo.com/main/popup/bbs_info.php?idx=' + cnt_num
                        resultData = getContents(url)
                        url2 = 'http://www.filejo.com/main/popup/frame_filelist.php?idx=' + cnt_num
                        cnt_fname = getFname(url2)
                        if count == 26:
                            count = 0
                        cnt_writer = returnValue[count]
                        # print(count)
                        count += 1
                        title_null = titleNull(resultData['Cnt_title'])
                        # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_null, getKey)
                        if keyCheck['m'] == None:
                            dbResult = insertDB('filejo',resultData['Cnt_title'],title_null,url)
                            continue
                        keyCheck2 = checkTitle2(title_null, getKey)
                        if keyCheck2['m'] == None:
                            dbResult = insertDB('filejo',resultData['Cnt_title'],title_null,url)
                            continue


                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'filejo',
                            'Cnt_title': resultData['Cnt_title'],
                            'Cnt_title_null': title_null,
                            'Cnt_url': url,
                            'Cnt_price': resultData['Cnt_price'],
                            'Cnt_writer' : cnt_writer,
                            'Cnt_vol' : resultData['Cnt_vol'],
                            'Cnt_fname' : cnt_fname,
                            'Cnt_chk': resultData['Cnt_chk']
                        }
                        # print(data)

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("filejo 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("filejo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
