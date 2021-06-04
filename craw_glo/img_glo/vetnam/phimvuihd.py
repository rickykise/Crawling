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
    link = 'http://phimvuihd.com/dat-nuoc/han-quoc?page='
    link2 = '&sort=Films.modified&direction=DESC'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'panel-body').find_all('div', 'col-md-3')

        try:
            for item in div:
                imgUrl = item.find('img')['data-original']
                url = 'http://phimvuihd.com'+item.find('div', 'film-name').find('a')['href']
                eng_title = item.find('div', 'font12').find('a')['title']
                if eng_title.find('(') != -1:
                    eng_title = eng_title.split('(')[0].strip()
                titleSub = item.find('div', 'film-name').find('a').text.strip()+eng_title
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
                url2 = 'http://phimvuihd.com'+soup.find('a', 'btn-primary')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'panel-body').find_all('li')

                for item in li:
                    if item.find('a'):
                        host_url = 'http://phimvuihd.com'+item.find('a')['href']
                        titleNum = item.find('a').text.strip()
                        if titleNum.find('Full') != -1:
                            title = titleSub
                        else:
                            title = titleSub+'_'+titleNum
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'phimvuihd',
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

    print("phimvuihd 크롤링 시작")
    startCrawling()
    print("phimvuihd 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
