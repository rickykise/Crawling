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

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.qdown.com/plist.html?cate1='+site+'&keyword=&cate2=&page_num='+str(i)
            post_one  = s.get(link)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            li = soup.find('ul', 'move_lst').find_all('li')

            try:
                for item in li:
                    adult = str(item)
                    if adult.find('list_bg_19') != -1:
                        continue
                    cnt_num = item.find('a')['onclick'].split("('")[1].split("')")[0]
                    url = 'http://www.qdown.com/main/popup/bbs_info.php?idx='+cnt_num

                    post_two  = s.get(url)
                    c = post_two.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                    text = str(soup)
                    cnt_chk = 0

                    title = soup.find('title').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = soup.find('td', 'infotable_td2').text.replace(" ","").replace(",","").split("P")[0].strip()
                    cnt_vol = soup.find('td', 'infotable_td2').text.replace(" ","").split("/")[1].strip()
                    cnt_writer = text.split("target_nick=")[1].split('","')[0]
                    cnt_fname = soup.find('td', 'infotable_list_td1').text.strip()
                    if soup.find('td', 'infotable_td2').find('img'):
                        jehu = soup.find('td', 'infotable_td2').find('img')['title']
                        if jehu == '제휴':
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'qdown',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_qdown 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_qdown 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
