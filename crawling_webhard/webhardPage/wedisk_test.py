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
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'freechargelLayer=done; contentsListBar=true; wediskNewIDSet=bGxpbTk4OTg%3D; NSHcookie=200907221b0a72d26c6f0003; _gid=GA1.3.1822846277.1552872043; _ga=GA1.3.1917148549.1552872043; JSESSIONID=2BDBDC99E5F1E811267F43FF94A8AE5D; _gat=1',
    'Host': 'www.wedisk.co.kr',
    'Referer': 'http://www.wedisk.co.kr/wediskNew/home.do',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    while check:
        with requests.Session() as s:
            i = i+1
            if i == 2:
                break
            link = 'http://www.wedisk.co.kr/wediskNew/Home/contentsList.do?data=%7B%22searchType%22%3A%221%22%2C%22category%22%3A%22'+site+'%22%2C%22subCategory%22%3A%22%22%2C%22subKey%22%3A%22%22%2C%22searchArea%22%3A%2221%22%2C%22searchKeyword%22%3A%22%22%2C%22pageViewRowNumber%22%3A%2220%22%2C%22selectCategory%22%3A%2200%22%2C%22selectSubCategory%22%3A%22%22%2C%22pageViewPoint%22%3A%22'+str(i)+'%22%2C%22oldSearchOption%22%3A%22%22%2C%22sort%22%3A%220%22%2C%22chkMbc%22%3A%22%22%2C%22SubCategory%22%3A%22%22%2C%22keyword%22%3A%22%22%7D'
            post_one  = s.get(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find('tbody', id='data_list').find_all('tr')

            for item in tr:
                adult = item.find('div', 'data_title')['onclick'].split(",'")[1].split("')")[0]
                if adult == 'Y':
                    continue
                cnt_num = item.find('td', 'data_info')['id'].split("c")[1]
                url = 'http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID=' + cnt_num
                if site == "00":
                    searchtype = 1
                else:
                    searchtype = 2



                print(url)
                # headers2 = {
                #     'Accept': '*/*',
                #     'Accept-Encoding': 'gzip, deflate',
                #     'Accept-Language': 'ko-KR',
                #     'Cache-Control': 'no-cache',
                #     'Connection': 'Keep-Alive',
                #     'Content-Length': '168',
                #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                #     'Cookie': 'JSESSIONID=EE9526EE52871383E09D21EF60E7D108; _gid=GA1.3.1822846277.1552872043; _ga=GA1.3.1917148549.1552872043; _gat=1; NSHcookie=200907221b0a72d26c6f0003; wediskNewIDSet=bGxpbTk4OTg%3D; contentsListBar=true',
                #     'Host': 'www.wedisk.co.kr',
                #     'Referer': link,
                #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                #     'X-Requested-With': 'XMLHttpRequest'
                # }
                Page = {
                    'contentsID': cnt_num,
                    'searchKey': {"searchType":searchtype,"category":site,"subCategory":"","subKey":"","keyword":""}
                }

                post_contents = s.post('http://www.wedisk.co.kr/wediskNew/contentsView.do', data=Page, headers=headers)
                soup2 = bs(post_contents.text, 'html.parser')
                # print(soup2)



                post_two = s.get(url, headers=headers)
                soup = bs(post_two.text, 'html.parser')



                cnt_chk = 0

                title = soup.find('div', 'register_title')['title']
                print(title)
                # print(soup)
                # print('========================================================================')
                # cnt_price = soup.find('span', 'price').text.strip().split("캐시")[0].replace(",","")
                # cnt_writer = soup.find('div', 'user_id').find('a').text.strip()
                # cnt_vol = soup.find('span', 'price').text.strip().split("/ ")[1]
                # cnt_fname = soup.find('li', 'file_title').text.strip()
                # if soup.find('li', 'file_type00'):
                #     cnt_fname = soup.find('li', 'file_type00')['title']
                # if soup.find('div', 'no_jw'):
                #     jehu = soup.find('div', 'no_jw')['class']
                #     if len(jehu) == 1:
                #         cnt_chk = 1
                #
                # data = {
                #     'Cnt_num' : cnt_num,
                #     'Cnt_osp' : 'wedisk',
                #     'Cnt_title': title,
                #     'Cnt_url': url,
                #     'Cnt_price': cnt_price,
                #     'Cnt_writer' : cnt_writer,
                #     'Cnt_vol' : cnt_vol,
                #     'Cnt_fname' : cnt_fname,
                #     'Cnt_chk': cnt_chk
                # }
                # print(data)
                print('========================================================================')
                # break

if __name__=='__main__':
    start_time = time.time()

    print("wedisk 크롤링 시작")
    site = ['00']
    # site = ['00','01','02','03','05']
    for s in site:
        startCrawling(s)
    print("wedisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
