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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://series24hd.com/wp-admin/admin-ajax.php'
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break

            Page = {
                'action': 'pagination_request',
                'ajax_nonce': 'a3854eafe0',
                'lang': '',
                'page': i,
                'sid': 'aacd288tdx',
                'unid': ''
            }
            r = s.post(link, data=Page)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            div = soup.find_all('div', 'pt-cv-ifield')

            try:
                for item in div:
                    imgUrl = item.find('img')['src']
                    url = item.find('div', 'pt-cv-title').find('a')['href']
                    titleSub = item.find('div', 'pt-cv-title').find('a').text.strip()
                    if titleSub.find('(') != -1:
                        titleSub = titleSub.split('(')[0].strip()
                    title_check = titleNull(titleSub)

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

                    r = s.post(url, data=Page)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    pSub = soup.find('div', 'entry-content').find_all('a', target="_blank")

                    for item in pSub:
                        title = item.text.strip()
                        title_null = titleNull(title)
                        if title_null.find('Ep') == -1:
                            continue
                        title_null = titleNull(title)
                        host_url = 'https://series24hd.com'+item['href'].replace(' ', '%20')
                        host_url = urllib.parse.unquote(host_url)

                        r = requests.get(host_url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        if soup.find('iframe'):
                            origin_url = soup.find('iframe')['src']
                            origin_osp = origin_url.split('//')[1].split('.')[0]
                            if origin_osp.find('www') != -1:
                                origin_osp = origin_osp.split('www.')[1]
                        else:
                            origin_url = ''
                            origin_osp = ''

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'series24hd',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'thailand',
                            'cnt_writer': '',
                            'cnt_cate': cnt_cate,
                            'origin_url': origin_url,
                            'origin_osp': origin_osp,
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

    print("series24hd 크롤링 시작")
    startCrawling()
    print("series24hd 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
