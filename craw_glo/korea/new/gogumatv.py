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
    linkSub = 'y'
    link = 'https://www.gogumatv.net/index.php/vod/type/id/'+site+'/page/'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'img-list').find_all('li')

        try:
            for item in li:
                url = 'https://www.gogumatv.net'+item.find('a')['href']
                if url.find('index') == -1:
                    continue
                titleSub = item.find('a')['title']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                keyCheck2 = checkTitle2(title_check, getKey)
                if keyCheck2['m'] == None:
                    continue

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find('div', "video_list").find_all('a')

                for item in div:
                    host_url = 'https://www.gogumatv.net'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    # r = requests.get(host_url)
                    # c = r.content
                    # soup = BeautifulSoup(c,"html.parser")
                    # origin_url = soup.find('iframe')['src']
                    # if origin_url.find('http') == -1:
                    #     origin_url = 'https:'+origin_url
                    # origin_osp = origin_url.split('//')[1]
                    # if origin_osp.find('www') != -1:
                    #     origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    # elif origin_osp.find('myqcloud') != -1:
                    #     origin_osp = 'myqcloud'
                    # else:
                    #     origin_osp = origin_osp.split('.')[0]

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'gogumatv',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'southkorea',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("gogumatv 크롤링 시작")
    site = ['13', '14','15', '21','22', '23','24', '25','26', '27','28', '29']
    for s in site:
        startCrawling(s)
    print("gogumatv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
