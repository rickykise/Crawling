import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key):
    i = 0; a = 1;check = True;captcha_aes = ''
    print(key)
    encText = key.encode('euc-kr')
    encText = urllib.parse.quote(encText)
    r = requests.get('http://oradisk.com/')
    c = r.content
    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
    captcha_aes = soup.find('input', id='captcha_aes')['value']
    LOGIN_INFO = {
        'Frame_login': 'Ok',
        'captcha_aes': captcha_aes,
        'fromsite': 'oradisk',
        'idSave': '0',
        'm': '',
        'm_id': 'up0001',
        'm_pwd': 'up0001'
    }
    with requests.Session() as s:
        login_req = s.post('http://daoki.com/member/loginCheck.php', data=LOGIN_INFO)
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://daoki.com/contents/?category1=&s_column=title&s_word='+encText+'&page='
            post_one  = s.get(link+str(i))
            c = post_one.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            tbody = soup.find('table', 'boardtype1').find('tbody')
            tr = tbody.find_all('tr', 'reply')

            try:
                for item in tr:
                    adult = item.find('a')['onclick'].split("', '")[2].split("')")[0]
                    if adult == '1':
                        continue
                    cnt_num = item['id'].split("list_")[1]
                    aes = item.find('a')['onclick'].split("', '")[3].split("')")[0]
                    url = 'http://daoki.com/contents/view.htm?idx='+cnt_num+'&aes='+aes
                    url2 = 'http://daoki.com/contents/view_top_filedown_new.html?idx='+cnt_num+'&aes='+aes
                    cnt_vol = item.find('td', 'date1').text.strip()

                    post_two  = s.get(url2)
                    c = post_two.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')

                    table = soup.find('table')
                    text = str(soup).split("<!-- 파일 리스트 종료 -->")[1].split("-->")[0]
                    cnt_chk = 0
                    title = table.find_all('tr')[1].find('b').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('daoki',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('daoki',title,title_null,url)
                    #     continue
                    cnt_writer = table.find('font', 'px12_dotum').text.strip()
                    cnt_price = text.split('bold;">')[1].split("</span>")[0].replace(",","")
                    cnt_fname = soup.find_all('table')[5].find_all('td')[2].find('font').text.strip()

                    jehu = soup.find_all('table')[5].find_all('td')[2].find('img')['src']
                    if jehu.find('allri_icon') != -1:
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
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("daoki 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("daoki 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
