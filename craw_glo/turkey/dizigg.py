import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://dizigg.com/ulke/south-korea/page/{}/'
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find('div', 'list_items').find_all('div', 'movie-box')
        try:
            for item in div:
                imgUrl = item.find('img')['data-src']
                url = item.find('a')['href']
                titleSub = item.find('div','name').find('a')['title'].strip()
                title_check = titleNull(titleSub)

                # 이미지 체크
                img_chk = 0
                getIMG = getImage()
                imgCheck = imageCheck(imgUrl,  getIMG)
                if imgCheck == None:
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check,  getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']
                    otoImg = ''
                    cnt_cate = 0
                    img_chk = 0
                else:
                    cnt_id = imgCheck['i']
                    cnt_keyword = imgCheck['k']
                    otoImg = imgCheck['m']
                    cnt_cate = imgCheck['c']

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check,  getKey)
                    if keyCheck['m'] == None:
                        img_chk = 1
                    else:
                        img_chk = 2

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                episode = soup.find('div', id='seasons').find_all('div','episode-box')

                for item in episode:
                    host_url = item.find('div','movie-details').find('a')['href']
                    title = item.find('div','movie-details').find('a')['title'].strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'dizigg',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'turkey',
                        'cnt_writer': '',
                        'cnt_cate': cnt_cate,
                        'origin_url': '',
                        'origin_osp': '',
                        'site_p_img': imgUrl,
                        'site_r_img': otoImg,
                        'site_img_chk': img_chk
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dizigg 크롤링 시작")
    startCrawling()
    print("dizigg 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
