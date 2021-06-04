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
    i = 0;check = True;cnt_osp = 'h3.hitjjal'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        link = group_url+'bbs/board.php?bo_table=streaming0'+site+'&page='
        cnt_osp = group_id
    else:
        link = 'https://h3.hitjjal.com/bbs/board.php?bo_table=streaming0'+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'tbl_wrap').find('tbody').find_all('tr')

        try:
            for item in div:
                if len(item['class']) >= 1:
                    continue
                aCount = item.find('td', 'td_subject').find_all('a')
                if len(aCount) == 1:
                    url = item.find('td', 'td_subject').find('a')['href']
                    url = urllib.parse.unquote(url)
                    title = item.find('td', 'td_subject').find('a').text.strip()
                else:
                    url = item.find('td', 'td_subject').find_all('a')[1]['href']
                    url = urllib.parse.unquote(url)
                    title = item.find('td', 'td_subject').find_all('a')[1].text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('section', id='bo_v_atc').find_all('p')

                for item in sub:
                    if item.find('a'):
                        host_url = item.find('a')['href']

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

    print("h3.hitjjal 크롤링 시작")
    site = ['3', '1']
    for s in site:
        startCrawling(s)
    print("h3.hitjjal 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
