import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
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

def startCrawling(site):
    i = 0;check = True
    link = 'https://phimchon.net/'+site
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'thumb')

        try:
            for item in div:
                imgUrl = item.find('img')['src'].split("url=")[1].split("'")[0].strip()
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                title_check = titleNull(titleSub)

                # 이미지 체크
                img_chk = 0
                getIMG = getImage()
                try:
                    imgCheck = imageCheck(imgUrl, getIMG)
                except:
                    continue
                if imgCheck == None:
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
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
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        img_chk = 1
                    else:
                        img_chk = 2

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                url2 = soup.find('a', 'btn-see')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'server_item')

                for item in div:
                    li = soup.find('ul', 'listep').find_all('li')
                    for item in li:
                        host_url = item.find('a')['href']
                        titleNum = item.find('a').text.strip()
                        title = titleSub+'_'+titleNum
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'phimchon',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'vietnam',
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phimchon 크롤링 시작")
    site = ['type/phim-bo-han-quoc/', 'quoc-gia/han-quoc/']
    for s in site:
        startCrawling(s)
    print("phimchon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
