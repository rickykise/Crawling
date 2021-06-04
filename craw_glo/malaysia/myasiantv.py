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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://www8.myasiantv.io/drama?selOrder=&selCat=&selCountry=&selYear=&btnFilter=Submit&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'items').find_all('li')

        try:
            for item in li:
                imgUrl = item.find('img')['src']
                url = 'https://www8.myasiantv.io'+item.find('a')['href']
                titleSub = item.find('img')['alt']
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
                li = soup.find('ul', 'list-episode').find_all('li')

                for item in li:
                    host_url = 'https://www8.myasiantv.io/'+item.find('a')['href']
                    title = item.find('a')['title']
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'myasiantv',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'malaysia',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)

                with requests.Session() as s:
                    urlSub = soup.find('a', 'paging')['onclick']
                    page = urlSub.split("('")[1].split("',")[0]
                    urlTitle = urlSub.split("','")[1].split("')")[0]
                    link = 'https://www8.myasiantv.io/ajax/episode-list/'+urlTitle+'/'+page+'.html?page='+page

                    headers = {
                        'Accept': 'text/html, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Referer': url,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                        'X-Requested-With': 'XMLHttpRequest'
                    }

                    Data = {
                        'page': page
                    }
                    post_one  = s.get(link, headers=headers, data=Data)
                    soup = bs(post_one.text, 'html.parser')
                    li = soup.find_all('li')

                    for item in li:
                        host_url = 'https://www8.myasiantv.io/'+item.find('a')['href']
                        title = item.find('a')['title']
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'myasiantv',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'malaysia',
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

    print("myasiantv 크롤링 시작")
    startCrawling()
    print("myasiantv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
