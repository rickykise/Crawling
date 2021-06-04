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
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
}

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.filehon.com/index.php?page='+str(i)+'&doc=board_list&cate1='+site+'&cate2='
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find('ul', 'contents_list').find_all('li')

            try:
                for item in li:
                    cnt_chk = 0
                    text = str(item)
                    if text.find('19금') != -1:
                        continue
                    if text.find('제휴') != -1:
                        cnt_chk = 1
                    title_sub = item.find('strong', 'con_title').text.strip()
                    title_check = titleNull(title_sub)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_check, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    url_sub = 'https://m.filehon.com'+item.find('a')['href'].replace(" ","")
                    cnt_num = url_sub.split("&idx=")[1].split("&")[0]
                    # etc_url1 = url_sub.split("&page")[0].strip()
                    # etc_url2 = url_sub.split("&page=")[1].split("&cate1")[1].strip()
                    # url = etc_url1+'&cate1'+etc_url2
                    url = url_sub

                    headers2 = {
                        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Connection': 'Keep-Alive',
                        'Host': 'm.filehon.com',
                        'Referer': url,
                        'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
                    }

                    post_one  = s.post(url, headers=headers2)
                    soup = bs(post_one.text, 'html.parser')

                    title = soup.find('div', 'title_area').text.strip()
                    title_null = titleNull(title)
                    cnt_price = soup.find('dl', 'detail_info').find_all('dd')[1].text.split("P")[0].replace(",","").strip()
                    cnt_vol = soup.find('div', 'filelist_details').find_all('span')[1].text.split("원본크기 :")[1].strip()

                    cnt_writer = soup.find('dl', 'detail_info').text.split("판매자")[1].strip()
                    if cnt_writer.find('자료보기') != -1:
                        cnt_writer = cnt_writer.split('자료보기')[0].strip()
                    cnt_fname = soup.find('div', 'filelistBox').find('li').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filehon',
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
                    # print('=============================================')

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_filehon 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_filehon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
