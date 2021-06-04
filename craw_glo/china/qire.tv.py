import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
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
    link = 'https://www.qire.tv/you/s15/page/'
    link2 = '.html'
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            r = s.get(link+str(i)+link2)
            c = r.text
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find_all('li', 'fed-list-item')
            try:
                for item in li:
                    imgUrl = item.find('a')['data-original']
                    url = 'https://www.qire.tv'+item.find('a')['href']
                    titleSub = item.find('a', 'fed-list-title').text.strip()
                    title_check = titleNull(titleSub)

                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_check, getKey)
                    # if keyCheck['m'] == None:
                    #     continue
                    # cnt_id = keyCheck['i']
                    # cnt_keyword = keyCheck['k']

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
                    c = r.text
                    soup = BeautifulSoup(c,"html.parser")
                    ul = soup.find_all('ul', 'fed-tabs-btm')

                    for item in ul:
                        li = item.find_all('li')
                        for item in li:
                            host_url = 'https://www.qire.tv'+item.find('a')['href']
                            title = titleSub+'_'+item.find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'qire.tv',
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
                                'site_p_img': imgUrl,
                                'site_r_img': otoImg,
                                'site_img_chk': img_chk
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
            except Exception as e:
                continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("qire.tv 크롤링 시작")
    startCrawling()
    print("qire.tv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
