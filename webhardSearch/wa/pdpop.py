import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
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

def startCrawling(key):
    i = 0;a = 1;b = 1;check = True
    print(key)
    encText = urllib.parse.quote(key)
    while check:
        i = i+1
        if i == 2:
            break
        link = 'http://bbs.pdpop.com/search_re.php?mode=loadList&code=&contentid=&szSearchCategory=bbs_subject&szSearchWord='+encText+'&nListPerPage=20&nBbsFlag=&nPage=1&content_id_minus=&request=&hash=0.1415155471033756&modifyNo=undefined&mbcevent='
        try:
            r = requests.get(link)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)

            for item in text:
                cnt_num = str(text).split('\n')[a].split('	')[0].strip()
                cate = text.split('F_')[b].split('	')[0].strip()

                a = a+1
                if cnt_num.find('head') != -1:
                    continue
                if cnt_num.find('</') != -1:
                    continue
                if len(cnt_num) <= 3:
                    continue
                b = b+1

                url = 'http://bbs.pdpop.com/board_re.php?mode=view&code=F_'+cate+'&no='+cnt_num

                resultData = getContents(url)
                title_null = titleNull(resultData['Cnt_title'])

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue

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
                # print("=================================")

                dbResult = insertALL(data)
        except:
            a = 1
            b = 1
            continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("pdpop 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("pdpop 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
