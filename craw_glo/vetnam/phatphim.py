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
    link = 'https://phatphim.com/phim-bo/han-quoc-phim-bo/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', 'grid-item')

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
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
                url2 = soup.find('a', 'btn-danger')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                postid = soup.find('link', rel="shortlink")['href'].split('p=')[1].strip()
                ajax_url = 'https://phatphim.com/wp-admin/admin-ajax.php'

                headers = {
                    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ko-KR',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie': '__cfduid=dba9084a60ebc26843976ba9d6558e1dc1618885024; _ga=GA1.2.885721336.1618885026; _gid=GA1.2.583481901.1618885026; _gat_gtag_UA_178762869_2=1; _gat_gtag_UA_141768961_1=1; _gat_gtag_UA_166809982_1=1; _gat_gtag_UA_172364664_1=1; _gat_gtag_UA_173909579_1=1',
                    'Host': 'phatphim.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'X-Requested-With': 'XMLHttpRequest'
                }

                data = {
                    'action':'halim_ajax_show_all_eps_list',
                    'episode':'1',
                    'postid': postid,
                    'server':'1'
                }

                r = requests.post(ajax_url,data=data, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find_all('li', 'halim-episode')

                for item in li:
                    tap = item.find('span')['data-episode']
                    ser = item.find('span')['data-server']
                    host_url = url2.split('tap-')[0]+'tap-'+tap+'-server-'+ser+'/'
                    titleNum = item.find('span').text.strip()
                    title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'phatphim',
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
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phatphim 크롤링 시작")
    startCrawling()
    print("phatphim 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
