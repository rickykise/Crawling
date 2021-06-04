import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

LOGIN_INFO = {
    'fromsite': 'daoki',
    'go_url': '/',
    'm': '',
    'pg_mode': 'login',
    'userid': 'up0001',
    'userpw': 'up0001'
}

cookies = {'Cookie': 'PHPSESSID=pd3g2lpfe78st514cufvo2tb26; count_index=1; __utma=109757584.1517675866.1548047108.1548047108.1548234028.2; __utmc=109757584; __utmz=109757584.1548234028.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; club_view=YToxOntpOjkxMDg4MjM7aToxNTQ4MzIwNTcwO30%3D; __utmb=109757584.6.10.1548234028'}

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0; a = 1;check = True
    with requests.Session() as s:
        login_req = s.post('http://www.daoki.com/login/index.php', data=LOGIN_INFO)
        while check:
            link = 'http://www.daoki.com/file_share/basic/bbs.php?start='
            link2 = '&bbscode='+site+'&list_scale=20'
            post_one  = s.get(link+str(i)+link2)
            soup = bs(post_one.text, 'html.parser')
            table = soup.find_all('table', width='100%')[12]
            tr = table.find_all('tr')
            try:
                for item in tr:
                    td = item.find_all('td')
                    if len(td) == 1:
                        continue
                    a = item.find_all('a', 'pds_list')[2]
                    if a.find('font'):
                        cnt_num = a['href'].split('idx=')[1].split('&')[0]
                        url = 'http://www.daoki.com/file_share/basic/bbs.php'+a['href'].split('("')[1].split('",')[0]
                        cnt_writer = item.find('td', width='80').find('font', 'pt9').text.strip()

                        post_two  = s.get(url)
                        soup = bs(post_two.text, 'html.parser')
                        text = str(soup)
                        cnt_chk = 0
                        if text.find('차단된 게시물') != -1:
                            continue

                        title = soup.find('font', 'bbstitle_bold').text.strip().split('+')[0]
                        title_null = titleNull(title)
                        # 키워드 체크
                        # getKey = getKeyword(conn,curs)
                        # keyCheck = checkTitle(title_null, getKey)
                        # if keyCheck['m'] == None:
                        #     continue
                        # keyCheck2 = checkTitle2(title_null, getKey)
                        # if keyCheck2['m'] == None:
                        #     continue
                        cnt_price = soup.find_all('font', 'intro_level_bcount')[1].text.strip().replace(",","").split('P')[0]
                        cnt_vol = soup.find_all('font', 'intro_level_bcount')[2].text.strip()
                        cnt_fname = soup.find_all('font', 'spacing')
                        if len(cnt_fname) >= 2:
                            cnt_fname = soup.find_all('font', 'spacing')[1].text.strip()
                        else:
                            cnt_fname = soup.find_all('font', 'spacing')[0].text.strip()
                        if text.find('ico_notice.gif') != -1:
                            cnt_chk = 1

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'daoki',
                            'Cnt_title': title,
                            'Cnt_title_null': title_null,
                            'Cnt_url': url,
                            'Cnt_price': cnt_price,
                            'Cnt_writer' : cnt_writer,
                            'Cnt_vol' : cnt_vol,
                            'Cnt_fname' : cnt_fname,
                            'Cnt_chk': cnt_chk
                        }
                        print(data)

                        # conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                        # try:
                        #     curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        #     dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                        # except Exception as e:
                        #     print(e)
                        #     pass
                        # finally :
                        #     conn2.close()
            except:
                continue

            i = i+20
            if i == 60:
                break

if __name__=='__main__':
    start_time = time.time()

    print("daoki 크롤링 시작")
    site = ['120459264342971','120459270334279','129177279075701','120459275742423']
    for s in site:
        startCrawling(s)
    print("daoki 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
