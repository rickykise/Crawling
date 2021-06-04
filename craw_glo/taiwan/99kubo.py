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
    link = site[0]
    with requests.Session() as s:
        while check:
            i = i+1
            if i == site[1]:
                break
            link = site[0]
            r = requests.get(link.format(str(i)))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find('ul', 'vod-item-img').find_all('li')

            try:
                for item in li:
                    imgUrl = item.find('img')['data-original']
                    url = 'https://m.99kubo.tv'+item.find('a')['href']
                    titleSub = item.find('h5','text-ellipsis').find('a')['title']
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
                    li = soup.find('ul', 'list-unstyled').find_all('li')

                    for item in li:
                        host_url = 'https://m.99kubo.tv'+item.find('a')['href']
                        title = titleSub+'_'+item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : '99kubo',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'taiwan',
                            'cnt_writer': '',
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

    print("99kubo 크롤링 시작")
    site=[['https://m.99kubo.tv/list-read-id-18-p-{}.html',30],['https://m.99kubo.tv/list-read-id-4-p-{}.html',30]]
    for item in site:
        startCrawling(item)
    print("99kubo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
