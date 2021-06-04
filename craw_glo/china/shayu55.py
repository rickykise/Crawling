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
    # link = 'https://www.97hanju.com/list/'+site+'/index-'
    # link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        if site == '1':
            if i == 1:
                link = 'https://www.shayu55.com/HJ/index.html'
                r = requests.get(link)
            else:
                link = 'https://www.shayu55.com/HJ/index-'
                link2 = '.html'
                r = requests.get(link+str(i)+link2)
        else:
            link = 'https://www.shayu55.com/l-4-1--time--%E9%9F%A9%E5%9B%BD--0.html'
            r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'channel').find('ul').find_all('li')

        try:
            for item in li:
                imgUrl = item.find('img')['src']
                url = 'https://www.shayu55.com'+item.find('div', 'li_text').find('a')['href']
                titleSub = item.find('div', 'li_text').find('a').text.strip()
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
                div = soup.find_all('div', 'playlist')

                for item in div:
                    li = item.find_all('li')
                    for item in li:
                        host_url = 'https://www.shayu55.com'+item.find('a')['href']
                        title = titleSub+'_'+item.find('a').text.replace('2019', '').strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'shayu55',
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

    print("shayu55 크롤링 시작")
    site = ['1', '2']
    for s in site:
        startCrawling(s)
    print("shayu55 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
