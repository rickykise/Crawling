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

# ==================불법 업체==================

# def getContents(url):
#     r = requests.get(url)
#     c = r.content
#     soup = BeautifulSoup(c,"html.parser")
#
#     cnt_price = soup.find('span', 'b_price').text.strip().split("P")[0].replace(",","")
#     cnt_writer = soup.find('table', 'file_detail').find_all('tr')[0].find_all('td', 'point_vol')[1].text.strip()
#     cnt_fname = soup.find('td', 'file_f').text.strip()
#     # print(cnt_writer)
#
#     data = {
#         'Cnt_price': cnt_price,
#         'Cnt_writer' : cnt_writer,
#         'Cnt_fname' : cnt_fname
#     }
#     # print(data)
#     return data

# LOGIN_INFO = {
#     'adtme': '1547188359',
#     'httpsurl': 'https://guard.jdisk.com/models/common/main/login/loginPrc_ssl.php',
#     'httpurl': '/models/common/main/login/loginPrc_ssl.php',
#     'mb_id': 'up0001',
#     'mb_pw': 'up0001',
#     'parrot': 'hrJKK1InBJyszhDjCiOdl9J+d3vfNUA03DERAxdRIXk=',
#     'renew': 'ok',
#     'sSiteNameLogin': 'jdisk.com',
#     'secure': 'Y'
# }
#
headers = {
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'http://www.jdisk.com/board.php',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'PHPSESSID=3te3kj5c1cslqjk3n5uc1p50k0; _bbsInfoTab=Y'
}

def startCrawling(site):
    with requests.Session() as s:
        # login_req = s.post('https://guard.jdisk.com/models/common/main/login/loginPrc_ssl.php', data=LOGIN_INFO, headers=headers)
        # soup = bs(login_req.text, 'html.parser')
        # print(soup)
        i = 5;check = True
        # link = "http://www.jdisk.com/board.php?section=MVO&nLimit=20"
        link = 'http://www.jdisk.com/board.php?act=asyncList&banner_keyword=&searchKey=&searchValue=&search_keyword_hidden=&search_type=DRA&search_keyword=&search=&useridx=&section=DRA&sub_sec=&nPage=1&tPage=4923&act=asyncList&mode=&s_act=&nLimit=20&_=1547445978683'
        while check:
            i = i+1
            if i == 2:
                break
            # Page = {
            #     'banner_keyword': '',
            #     'searchKey': '',
            #     'searchValue': '',
            #     'search_keyword_hidden': '',
            #     'search_type': site,
            #     'search_keyword': '',
            #     'search': '',
            #     'useridx': '',
            #     'section': site,
            #     'sub_sec': '',
            #     'nPage': i,
            #     'act': 'asyncList',
            #     'mode': '',
            #     's_act': '',
            #     'nLimit': '20',
            #     '_': '1547187463011',
            # }
            # post_one  = s.get(link)
            # soup = bs(post_one.text, 'html.parser')
            # print(soup)
            # break
            post_one  = s.get(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            print(soup)
        # html = driver.find_element_by_id("contentList_Table").get_attribute('innerHTML')
        # soup = BeautifulSoup(html,'html.parser')
        # tr = soup.find("tbody").find_all("tr")
        # if len(tr) < 2:
        #     check = False
        #     print("게시물없음\n========================")
        #     break
        #
        # for item in tr:
        #     now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     titlesub = item.find('td', 'c_title').find('a').find('span', 'txt').find_all('img')
        #     if len(titlesub) == 2:
        #         continue
        #     title = item.find('td', 'c_title').find('a').find('span', 'txt').text.strip()
        #     cnt_num = item['data-idx']
        #     url = "http://www.jdisk.com/board.php?act=bbs_info&idx="+cnt_num
        #     cnt_vol = item.find_all('td', 'c_data')[1].text.strip()
        #     resultData = getContents(url)
        #
        #     data = {
        #         'Cnt_num' : cnt_num,
        #         'Cnt_osp' : 'jdisk',
        #         'Cnt_title': title,
        #         'Cnt_url': url,
        #         'Cnt_price': resultData['Cnt_price'],
        #         'Cnt_writer' : resultData['Cnt_writer'],
        #         'Cnt_vol' : cnt_vol,
        #         'Cnt_fname' : resultData['Cnt_fname'],
        #         'Cnt_regdate' : now,
        #         'Cnt_chk': '0'
        #     }
        #     # print(data)
        #
        #     conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
        #     try:
        #         curs = conn.cursor(pymysql.cursors.DictCursor)
        #         dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
        #     except Exception as e:
        #         print(e)
        #         pass
        #     finally :
        #         conn.close()

if __name__=='__main__':
    start_time = time.time()

    print("jdisk 크롤링 시작")
    site = ['ALL']
    # site = ['ALL','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    # startCrawling()
    print("jdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
