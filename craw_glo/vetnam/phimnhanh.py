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
    i = 0;a = 1;check = True
    link = 'https://phimnhanh.biz/pn/filter?t=f&ct=&nt=han-quoc&ot=&mt=&p='
    while check:
        if i == 30:
            break
        r = requests.get(link+str(i))
        i = i+1
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'col-sm-6')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('h2', 'title elipsis').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                url2 = soup.find('a', 'btn-effect')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)

                drt = text.split("drt:'")[1].split("',mid")[0].strip()
                mid = text.split('mid:"')[1].split('",num')[0].strip()
                num = text.split(mid+'",num:')[1].split(',current')[0].strip()
                current = text.split("var current='")[1].split("';")[0].strip()
                pos = soup.find('div', 'tab-content').find('div')['data-pos']
                idx = int(pos)*10-1
                range = soup.find('div', 'tab-content').find('div')['data-range']
                sort = text.split(",sort:'")[1].split("',inchd")[0].strip()
                inchd = text.split(",inchd:'")[1].split("',end_idx")[0].strip()
                end_idx = soup.find('div', 'tab-content').find('div')['data-eidx']

                ajax_url = 'https://pn.voocdn.com/content/subitems?drt='+drt+'&mid='+mid+'&num='+num+'&current='+current+'&idx='+str(idx)+'&range='+range+'&sort='+sort+'&inchd='+inchd+'&end_idx='+end_idx

                r = requests.get(ajax_url)
                c = r.content
                soup = BeautifulSoup(c.decode('utf8','replace'),"html.parser")
                text = str(soup).split('</a>')[0].replace('\\', '').strip()

                for item in text:
                    host_url = text.split("href='"+'"')[a].split('"')[0].strip()
                    title = titleSub+'_'+text.split('nttTu1eadp')[a].split('t')[0].strip()
                    title_null = titleNull(title)
                    a = a+1

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'phimnhanh',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            a = 1
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phimnhanh 크롤링 시작")
    startCrawling()
    print("phimnhanh 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
