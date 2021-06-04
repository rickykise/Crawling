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

def startCrawling():
    i = 0; a = 1;check = True
    link = 'http://maplestage.com/drama/kr'
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)

        try:
            for item in text:
                titleSub = text.split('"slug":"')[a].split('",')[0]
                title_check = titleNull(titleSub)
                a = a+1
                if a == 1033:
                    a = 1
                    break

                url = 'http://maplestage.com/show/'+titleSub
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")

                text2 = str(soup.find('div', 'show-page-module__imgDiv___3s4BP'))
                imgUrl = text2.split("url('")[1].split("'")[0]

                # 이미지 체크
                img_chk = 0
                getIMG = getImage()
                imgCheck = imageCheck(imgUrl, getIMG)
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

                sub = soup.find('div', 'show-page-module__episodesBox___6KqJo').find_all('a')
                for item in sub:
                    host_url = 'http://maplestage.com'+item['href']
                    title = item['title']
                    if title.find('ost') != -1 or title.find('OST') != -1:
                        continue
                    title_null = titleNull(title)

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    text = str(soup)

                    try:
                        if text.find('iframe'):
                            origin_url = text.split('<iframe')[1].split('/iframe')[0].split('"')[1].split('"')[0].replace('\\', '')
                            if origin_url.find('https') == -1:
                                origin_url = 'https:'+origin_url
                            origin_osp = origin_url.split('//')[1]
                            if origin_osp.find('www') != -1:
                                origin_osp = origin_osp.split('www.')[1].split('.')[0]
                            else:
                                origin_osp = origin_osp.split('.')[0]
                        else:
                            origin_url = ''
                            origin_osp = ''
                    except:
                        origin_url = ''
                        origin_osp = ''

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'maplestage',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
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

    print("maplestage 크롤링 시작")
    startCrawling()
    print("maplestage 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
