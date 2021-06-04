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
    link = 'https://daebakdrama.com/'+site+'/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'entry-content').find_all('div', 'even-grid-item')

        try:
            for item in div:
                imgUrl = item.find('img')['src']
                div = item.find('div', 'rt-detail')
                url = div.find('a')['href']
                titleSub = div.find('a').text.strip()
                title_check = titleNull(titleSub)

                # 이미지 체크
                getIMG = getImage()
                imgCheck = imageCheck(imgUrl, getIMG)
                if imgCheck == None:
                    continue
                otoImg = imgCheck['m']
                cnt_id = imgCheck['i']
                cnt_keyword = imgCheck['k']
                cnt_cate = imgCheck['c']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('ul', 'lcp_catlist').find_all('li')

                for item in li:
                    host_url = item.find('a')['href']
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'daebakdrama',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'indonesia',
                        'cnt_writer': '',
                        'cnt_cate': cnt_cate,
                        'origin_url': '',
                        'origin_osp': '',
                        'site_p_img': imgUrl,
                        'site_r_img': otoImg
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("daebakdrama 크롤링 시작")
    site = ['kd','km','currently-airing']
    for s in site:
        startCrawling(s)
    print("daebakdrama 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
