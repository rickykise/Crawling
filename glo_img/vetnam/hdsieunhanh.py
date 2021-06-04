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
    i = 0;check = True
    link = 'http://hdsieunhanh.com/quoc-gia/han-quoc/trang-'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find('div', 'group-film-small').find_all('a', 'film-small')

        try:
            for item in sub:
                imgUrl = item.find('div', 'poster-film-small')['style'].split("url('")[1].split("'")[0].strip()
                url = 'http:'+item['href']
                titleSub = item['title'].replace('\xa0', '')
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
                url2 = 'http://hdsieunhanh'+soup.find('a', 'play-film')['href'].split('hdsieunhanh')[1].replace('\xa0', '')

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'episode-main').find('ul').find_all('li')

                for item in li:
                    title = titleSub + '_' + item.find('a').text.strip()
                    title_null = titleNull(title)
                    host_url = 'http://hdsieunhanh'+item.find('a')['href'].split('hdsieunhanh')[1].replace('\xa0', '')

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'hdsieunhanh',
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

    print("hdsieunhanh 크롤링 시작")
    startCrawling()
    print("hdsieunhanh 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
