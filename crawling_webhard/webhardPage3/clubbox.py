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
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True
    link = "http://greenbbs.clubbox.co.kr:8126/app/index.php?pageNo="
    link2 = "&c_no="+site+"&c_depth=1&listPerPage=&search_word=&search_col=b_subject&c_adult=N"
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'file_list')
        tr = div.find('table').find_all('tr')
        try:
            for item in tr:
                td = item.find_all('td')
                if len(td) != 7:
                    continue
                adult = item.find('a', id=re.compile("cutTitle_+"))['href'].split("', '")[1].split("'")[0]
                if adult == '1':
                    continue
                cnt_fname = item.find('ul').find('li').text.strip()
                cnt_vol = item.find('td', 'file_cash_info').text.strip()
                cnt_num = item.find('a', id=re.compile("cutTitle_+"))['id'].split("cutTitle_")[1]
                url = 'http://greenbbs.clubbox.co.kr:8126/app/index.php?b_no='+cnt_num+'&control=view'

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                table = soup.find('div', 'scroll_file_down').find('table')
                cnt_price = 0;returnValue = []

                title = soup.find('a', 'b_twitter')['href'].split("', '")[1].split("'")[0]
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeyword(conn,curs)
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue
                tr = table.find_all('tr')
                for item in tr:
                    cnt_price = int(item.find_all('td')[3].text.replace(",", "").strip().split("C")[0])
                    returnValue.append(cnt_price)
                for i in range(len(tr)-1):
                    cnt_price = returnValue[i]+cnt_price

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'clubbox',
                    'Cnt_title': title,
                    'Cnt_title_null': title_null,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : '',
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
                    'Cnt_chk': '1'
                }
                # print(data)

                conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                try:
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                except Exception as e:
                    print(e)
                    pass
                finally :
                    conn2.close()
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("clubbox 크롤링 시작")
    site = ['','1','13','16','10']
    for s in site:
        startCrawling(s)
    print("clubbox 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
