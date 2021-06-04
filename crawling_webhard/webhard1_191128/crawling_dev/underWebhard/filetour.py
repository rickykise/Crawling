import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print('키워드: ',key)
    key = emoKey(key)
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True;pn_sd = '';insertNum = 0
    link = "http://www.filetour.com/front/contents?lcate_cd=&list_cnt=20&sword="+key
    while check:
        try:
            if pn_sd != '':
                link = 'http://www.filetour.com'+pn_sd
            r = requests.get(link)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            div = soup.find('div', 'list_contents')
            ul = div.find_all('ul', 'list_body2')
            if len(ul) == 0:
                break
            if pn_sd == '':
                if len(soup.find('div', 'paginator_content').find_all('li')) != 5:
                    pn_sd = soup.find('div', 'paginator_content').find_all('li')[i+3].find('a')['href']
                else:
                    pn_sd = 'end'
            else:
                try:
                    pn_sd = soup.find('div', 'paginator_content').find_all('li')[i+1].find('a')['href']
                except:
                    pn_sd = 'end'
            i = i+1

            for item in ul:
                if item.find('span', 'icon-img icon-19'):
                    continue
                cnt_num = item.find('a')['href'].split("contents/")[1]
                url = 'http://www.filetour.com/front/contents/'+cnt_num

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                table = soup.find('table', 'show_table')
                cnt_chk = 0

                title = soup.find('title').text.strip().split('파일투어 - ')[1]
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeyword(conn,curs)
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue
                cnt_price = soup.find('span', 'red-txt bold-txt').text.replace(" ","").replace(",","").strip().split('P')[0]
                cnt_writer = table.find_all('td')[1].text.strip()
                cnt_vol = table.find_all('td')[2].text.strip()
                cnt_fname = table.find_all('tr')[2].find('td').text.strip()
                if table.find('span', 'b_blue_btn disp_ibl'):
                    jehu = table.find('span', 'b_blue_btn disp_ibl').text.strip()
                    if jehu == '제휴':
                        cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filetour',
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

                conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                try:
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    if dbResult == True:
                        continue
                    else:
                        insertNum = insertNum+1
                finally :
                    conn2.close()
            if pn_sd == 'end':
                break
        except:
            continue

    print("insert : ",insertNum)
    print('==================================================================')

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getUnderSearchKey(conn,curs)
    conn.close()

    print("filetour 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("filetour 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
