import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key):
    i = 0;check = True
    print(key)
    encText = key.encode('euc-kr')
    encText = urllib.parse.quote(encText)
    link = "http://www.kdisk.co.kr/index.php?mode=kdisk&s_act=ok&sort_type=default&sub_sec=&sm_search_keyword=&sm_search=&restrict_act=N&list_count=&search_type=all&search_keyword=title&search="+encText+"&p="

    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        while check:
            i = i+1
            if i == 9:
                break
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id('mnShare_text_list').get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody", id="contents_list").find_all("tr",class_=False)
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if item.find('td', 'subject').find('span', 'textOverflow').find('img'):
                    img = item.find('td', 'subject').find('span', 'textOverflow').find_all('img')
                    if len(img) == 1:
                        if item.find('td', 'subject').find('span', 'textOverflow').find('img')['src'].find('icon_19up') != -1:
                            continue
                    elif len(img) == 2:
                        if item.find('td', 'subject').find('span', 'textOverflow').find_all('img')[1]['src'].find('icon_19up') != -1:
                            continue
                    elif len(img) == 3:
                        if item.find('td', 'subject').find('span', 'textOverflow').find_all('img')[1]['src'].find('icon_19up') != -1:
                            continue
                cnt_num = item.find('td', 'subject').find('a')['idx']
                url = 'http://www.kdisk.co.kr/pop.php?sm=bbs_info&idx=' + cnt_num
                cnt_vol = item.find('td', 'capacity').text.strip()
                cnt_writer = item.find('td', 'nickname').find('a', 'btpTip').text.strip()

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                cnt_chk = 0

                title = soup.find('div', 'ctvTitle').find('h2').text.strip()
                title_null = titleNull(title)
                cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().split("P")[0].replace(",","")
                cnt_fnameCk = soup.find('div', 'bxSkin').find('span', 'capacity').text.strip()
                cnt_fname = soup.find('div', 'bxSkin').text.replace("\n","").replace("\t","").replace("\xa0", "").strip().split(cnt_fnameCk)[0]

                if soup.find('p', 'careMsg'):
                    cnt_chkCh = soup.find('p', 'careMsg').text.strip()
                    if cnt_chkCh.find('제휴') != -1:
                        cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'kdisk',
                    'Cnt_title': title,
                    'Cnt_title_null': title_null,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
                    'Cnt_regdate' : now,
                    'Cnt_chk': cnt_chk
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("kdisk 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("kdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
