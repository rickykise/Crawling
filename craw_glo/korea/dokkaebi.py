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
path = inspect.getfile(inspect.currentframe())
x = path.split('\\')
x.reverse()
osp_id = x[0].split('.py')[0].strip()

def startCrawling(site):
    i = 0;check = True;cnt_osp = 'dokkaebi'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        link = group_url+'genre/'+site+'/page/'
        cnt_osp = group_id
    else:
        link = 'https://dokkaebi.tv/genre/'+site+'/page/'
    while check:
        i = i+1
        if i == 10:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', id=re.compile("post-+"))

        try:
            for item in article:
                url = item.find('div', 'data').find('a')['href']
                url = urllib.parse.unquote(url)
                titleSub = item.find('div', 'data').find('a').text.replace('다시보기', '').strip()
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
                li = soup.find('ul', 'episodios').find_all('li')

                for item in li:
                    host_url = item.find('div', 'episodiotitle').find('a')['href']
                    host_url = urllib.parse.unquote(host_url)
                    title = titleSub+'_'+item.find('div', 'episodiotitle').find('a').text.replace('다시보기', '').strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : cnt_osp,
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'southkorea',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("dokkaebi 크롤링 시작")
    site = ['krtvdrama', 'krtvdramaend']
    for s in site:
        startCrawling(s)
    print("dokkaebi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
