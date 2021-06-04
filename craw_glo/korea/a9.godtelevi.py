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
    i = 0;check = True;cnt_osp = 'a9.godtelevi'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        link = group_url+'bbs/board.php?bo_table='+site+'&page='
        cnt_osp = group_id
    else:
        link = 'https://a9.godtelevi.com/bbs/board.php?bo_table='+site+'&page='
    while check:
        i = i+1
        if i == 50:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        td = soup.find('div', 'tbl_wrap').find_all('td', 'td_subject')

        try:
            for item in td:
                url = item.find('a')['href'].split('&page=')[0].strip()
                titleSub = item.find('a').text.strip()
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
                ul = soup.find('div', id='link-area').find_all('ul')

                if soup.find('div', id="dasibogi-list"):
                    div = soup.find('div', id="dasibogi-list").find_all('div', 'dasibogi-bt')
                    for item in div:
                        url = 'https://a9.godtelevi.com'+item.find('a')['href']
                        titleSub = item.find('a').text.strip()
                        title_check = titleNull(titleSub)

                        r = requests.get(url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        ul = soup.find('div', id='link-area').find_all('ul')

                        for item in ul:
                            sub = item.find_all('a')
                            for item in sub:
                                host_url = item['href']
                                if host_url.find('https') == -1:
                                    host_url = 'https:'+host_url
                                title = titleSub+'_'+item.find('li').text.strip()
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
                else:
                    for item in ul:
                        sub = item.find_all('a')
                        for item in sub:
                            host_url = item['href']
                            if host_url.find('https') == -1:
                                host_url = 'https:'+host_url
                            title = titleSub+'_'+item.find('li').text.strip()
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

    print("a9.godtelevi 크롤링 시작")
    site = ['enter_dasibogi', 'drama_dasibogi']
    for s in site:
        startCrawling(s)
    print("a9.godtelevi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
