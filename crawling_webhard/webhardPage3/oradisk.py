import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
        'Origin': 'http://oradisk.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0; a = 1;check = True;captcha_aes = ''
    r = requests.get('http://oradisk.com/')
    c = r.content
    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
    captcha_aes = soup.find('input', id='captcha_aes')['value']
    LOGIN_INFO = {
        'Frame_login': 'Ok',
        'captcha_aes': captcha_aes,
        'idSave': '0',
        'm': '',
        'm_id': 'up0002',
        'm_pwd': 'up0002'
    }
    with requests.Session() as s:
        login_req = s.post('http://oradisk.com/member/loginCheck.php', data=LOGIN_INFO, headers=headers)
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://oradisk.com/contents/?category1='+site+'&page='
            post_one  = s.get(link+str(i))
            c = post_one.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            tbody = soup.find('table', 'boardtype1').find('tbody')
            tr = tbody.find_all('tr', 'reply')

            # try:
            for item in tr:
                print('========================================')
                adult = item.find('a')['onclick'].split("', '")[2].split("')")[0]
                if adult == '1':
                    continue
                cnt_num = item['id'].split("list_")[1]
                aes = item.find('a')['onclick'].split("', '")[3].split("')")[0]
                url = 'http://oradisk.com/contents/view_top_filedown_new.html?idx='+cnt_num+'&aes='+aes
                cnt_writer = item.find('a', 'uploader').text.strip()
                cnt_vol = item.find('td', 'date1').text.strip()

                post_two  = s.get(url)
                c = post_two.content
                soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                print(soup)
                table = soup.find('table')
                cnt_chk = 0

                title = table.find_all('tr')[4].find('b').text.strip()
                title_null = titleNull(title)
                # 키워드 체크
                # getKey = getKeyword(conn,curs)
                # keyCheck = checkTitle(title_null, getKey)
                # if keyCheck['m'] == None:
                #     continue
                # keyCheck2 = checkTitle2(title_null, getKey)
                # if keyCheck2['m'] == None:
                #     continue
                cnt_price = soup.find('span', id='down_point_span').text.replace(",","").strip()
                cnt_fname = table.find_all('tr')[10].find_all('td')[1].find('font').text.strip()
                jehu = table.find_all('tr')[10].find_all('td')[1].find('img')['src']
                if jehu.find('allri_icon') != -1:
                    cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'oradisk',
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
            # except:
            #     continue

if __name__=='__main__':
    start_time = time.time()

    print("oradisk 크롤링 시작")
    site = ['','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("oradisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
