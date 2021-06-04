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
    if site == '1' or site == '2':
        if site == '1':
            link = 'https://dramacu.com/featured.html?page='
        else:
            link = 'https://dramacu.com/tv-series.html?page='
    else:
        if site =='3':
            link = 'https://dramacu.com/top-movies.html'
        else:
            link = 'https://dramacu.com/country-korea.html'

    while check:
        i = i+1
        if i == 30:
            break
        if site == '1' or site == '2':
            r = requests.get(link+str(i))
        else:
            r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', id=re.compile("film-+"))

        try:
            for item in div:
                imgUrl = item.find('img')['src']
                url = item.find('a')['href']
                titleSub = item.find('img')['alt']
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

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                film_idCount = url.count('-')
                film_id = url.split('-')[film_idCount].split('.html')[0]
                url2 = soup.find('div', 'icon-play').find('a')['href']
                epid = url2.split(film_id+'.')[1].split('.html')[0]

                Page = {
                    'epid': epid,
                    'film_id': film_id
                }

                r = requests.post('https://dramacu.com/ajax/loadServer.php', data=Page)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)
                a = 1

                try:
                    for item in text:
                        epidSub = text.split('href=')[a].split('&lt')[0].split(film_id+'.')[1].split('.html')[0]
                        urlSub = url2.split(epid)[0]
                        host_url = urlSub+epidSub+'.html'
                        title = titleSub+'_'+text.split('href=')[a].split('&lt')[0].split('title=')[1].split('>')[1].strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'dramacu',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'other',
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
                        a = a+1
                except:
                    a = 1
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dramacu 크롤링 시작")
    site = ['1', '2', '3', '4']
    for s in site:
        startCrawling(s)
    print("dramacu 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
