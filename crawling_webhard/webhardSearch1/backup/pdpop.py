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
    text = str(soup)
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
    cnt_writer = soup.find('div', 'fsview_table').find('strong').text.strip()
    cnt_vol = soup.find('strong', id='chkSize').text.strip()
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
        'Cnt_writer' : cnt_writer,
        'Cnt_vol' : cnt_vol,
        'Cnt_fname' : cnt_fname,
        'Cnt_chk': cnt_chk
    }
    # print(data)
    return data

def startCrawling(site):
    i = 0;a = 1;check = True
    while check:
        i = i+1
        if i == 4:
            break
        link = "http://boardapi.pdpop.com/board?category=F_"+site+"&sort=recent&adult=y&page="+str(i)+"&pagesize=50&format=jsonp&callback=jQuery17107636038667202258_1551670944999&_=1551670976935"
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)

        try:
            for item in text:
                adult = text.split('"adult":"')[a].split('","')[0]
                cnt_num = text.split('"no":')[a].split(',')[0]
                a = a+1
                if a == 51:
                    a = 1
                    break
                if adult == 'Y':
                    continue
                url = 'http://bbs.pdpop.com/board_re.php?mode=view&code=F_'+site+'&no='+cnt_num

                resultData = getContents(url)
                title_null = titleNull(resultData['Cnt_title'])
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    dbResult = insertDB('pdpop',resultData['Cnt_title'],title_null,url)
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    dbResult = insertDB('pdpop',resultData['Cnt_title'],title_null,url)
                    continue
                # checkPrice = str(keyCheck['p'])
                # if checkPrice == resultData['Cnt_price']:
                #     resultData['Cnt_chk'] = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'pdpop',
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

    print("pdpop 크롤링 시작")
    site = ['02','03','04']
    for s in site:
        startCrawling(s)
    print("pdpop 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
