import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://www.jjinpl.com/contents/board.php?menu='+site+'&page='
            post_one  = s.get(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            li = soup.find('div', 'thumb').find('ul').find_all('li')

            try:
                for item in li:
                    cnt_num = item['class'][1].split('thumbnail')[0].strip()
                    url = 'http://www.jjinpl.com'+item.find('a')['href']
                    title = item.find('label', 'mainchecklabel').text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('jjinpl',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('jjinpl',title,title_null,url)
                        continue

                    cnt_vol = item.find('p', 'tbs_s').text.replace(' ', '').replace(",","").strip()
                    cnt_price = item.find('p', 'tbs_p').text.replace(" ","").replace(",","").split("P")[0].strip()

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    cnt_writer = soup.find('table', 'infoSheet').find('tbody').find('td', colspan="3").text.strip()
                    if cnt_writer.find('평가없음') != -1:
                        cnt_writer = cnt_writer.split('\t')[0].strip()
                    cnt_fname = soup.find('table', 'infoSheet').find('tbody').find('td', colspan="7").text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'jjinpl',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': '0'
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("jjinpl 크롤링 시작")
    site = ['1&menumode=all','1','2','3','5']
    for s in site:
        startCrawling(s)
    print("jjinpl 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
