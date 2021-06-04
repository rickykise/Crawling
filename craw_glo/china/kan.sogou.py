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
    i = 0
    check = True
    link = 'http://kan.sogou.com/dianshiju/-hanguo---{}/'
    while check:
        i = i+1
        if i == 7:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find('div', 'add-list-1').find_all('div', 'cell cf')

        try:
            for item in div:
                url = 'http://kan.sogou.com' + item.find('p', 'tit').find('a')['href']
                titleSub = item.find('p', 'tit').find('a').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                script = soup.find('script', text=lambda text: text and "var defaultEpisodeList" in text)
                import json
                player = script.string.replace('var defaultEpisodeList =','').split("var groupinfo =")[0].replace(';','').strip()
                playerJson = json.loads(player)

                for item in playerJson['data']:
                    if 'vid' in item and 'num' in item and 'surl' in item:
                        host_url = 'http://kan.sogou.com/epjump?vid={}&vtype=2&index={}&gid=238623&url={}'.format(str(item['vid']),item['num'],item['surl'])
                        title = titleSub +'_'+ item['num']
                        title_null = titleNull(title)

                        origin_url = item['surl']
                        origin_osp = origin_url
                        if origin_osp.find('www') != -1:
                            origin_osp = origin_osp.split('www')[1].lstrip('.').split('.')[0]
                        else:
                            origin_osp = origin_osp.split('.')[0]
                            
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'kan.sogou',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url': host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'china',
                            'cnt_writer': '',
                            'origin_url': origin_url,
                            'origin_osp': origin_osp
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    start_time = time.time()
    if getDel == '1':
        sys.exit()

    print("kan.sogou 크롤링 시작")
    startCrawling()
    print("kan.sogou 크롤링 끝")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("=================================")
