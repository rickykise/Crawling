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
    while check:
        if site == '1':
            link = 'https://phymnhanh.net/pn/filter?t=f&ct=cat-tv-show&nt=han-quoc&p='
            i = i+1
            if i == 20:
                break
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
        else:
            link = 'https://phymnhanh.net/pn/filter?t=f&mt=mtype-phim-bo&nt=han-quoc&p='
            i = i+1
            if i == 100:
                break
            r = requests.get(link+str(i))
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
                # print(soup)
                text = str(soup)

                mid = text.split('mid:"')[1].split('",')[0].strip()
                num = text.split('mid:"')[1].split('num:')[1].split(',')[0].strip()
                range = soup.find('li', 'eps_list_tab_div').find('a')['data-range']
                end_idx = soup.find('li', 'eps_list_tab_div').find('a')['data-eidx']

                ajax_url = 'https://pn.voocdn.com/content/subitems?drt=up&mid='+mid+'&num='+num+'&range='+range+'&idx=-1&sort=desc&inchd=n&end_idx='+end_idx

                a = 1
                r = requests.get(ajax_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                ajax_text = str(soup).replace('\n', '').replace('\\', '')

                try:
                    for item in ajax_text:
                        ajax_line = ajax_text.split('<a ')[a].split('ttitle')[0]
                        host_url = 'https://phymnhanh.net/'+ajax_line.split('"/')[1].split('"n')[0]
                        title_num = ajax_line.split('"="')[0].strip()
                        if title_num.find('""') != -1:
                            title_num = title_num.split('""')[1].split('=')[0].strip()
                        title = titleSub+'_'+title_num
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'phymnhanh',
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

                        a = a+1
                except:
                    a = 1
                    break
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phymnhanh 크롤링 시작")
    site = ['1', '2']
    for s in site:
        startCrawling(s)
    print("phymnhanh 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
