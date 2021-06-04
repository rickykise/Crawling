import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from checkFun import *

cnt_osp = 'megafile'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            LOGIN_INFO = {
                'login_backurl': '',
                'loginid': 'up0001',
                'passwd': 'up0001',
                'site': 'megafile.co.kr',
                'type': '',
                'url': 'http://m.megafile.co.kr/'
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
            }
            with requests.Session() as s:
                login_req = s.post('http://m.megafile.co.kr/user/login_process.php', data=LOGIN_INFO)
                post_one = s.get(url, headers=headers)
                c = post_one.content
                soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                print(soup)
                # cnt_chk = 0
                #
                # if soup.find('div', 'filetitle').find('img'):
                #     jehu = soup.find('div', 'filetitle').find('img')['src']
                #     if jehu.find('icon_copyright2') != -1:
                #         cnt_chk = 1
        except:
            cnt_chk = 2
        # dbUpdate(checkNum,cnt_chk,url)
        print(url)
        print(cnt_chk)
        print('==================================================')

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("megafile check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("megafile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")




headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

def startCrawling(site):
    conn = host
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0; a = 1;check = True
    with requests.Session() as s:
        login_req = s.post('http://m.megafile.co.kr/user/login_process.php', data=LOGIN_INFO)
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.megafile.co.kr/webhard/ajax_list.php?type=&category='+site+'&subcategory=0&search=&time=0.73672800%2013790044113531221&page='
            post_one  = s.get(link+str(i))
            c = post_one.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            div = soup.find_all('div', id='list_div')
            try:
                for item in div:
                    cnt_vol = item.find('span', 'contents_list_size2').text.strip()
                    cnt_num = item.find('a')['href'].split("id=")[1].split("&")[0]
                    href = item.find('a')['href']
                    url = 'http://m.megafile.co.kr'+href
                    post_two = s.get(url, headers=headers)
                    c = post_two.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                    div = soup.find('div', id='fileinfo_text')
                    cnt_chk = 0

                    title = soup.find('div', 'filetitle').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('megafile',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('megafile',title,title_null,url)
                        continue
                    cnt_price = div.find_all('div')[1].text.strip().split('캐시')[1].replace(",","")
                    cnt_writer = div.find_all('div')[2].text.strip().split('등록자')[1].replace(",","")
                    cnt_fname = soup.find('div', 'c_title').text.strip()
                    if soup.find('div', 'filetitle').find('img'):
                        jehu = soup.find('div', 'filetitle').find('img')['src']
                        if jehu.find('icon_copyright2') != -1:
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'megafile',
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

                    conn2 = host
                    try:
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                        insertDB('megafile',title,title_null,url)
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn2.close()
            except:
                continue


if __name__=='__main__':
    start_time = time.time()

    print("megafile 크롤링 시작")
    site = ['','1','2','3','5']
    for s in site:
        startCrawling(s)
    print("megafile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")