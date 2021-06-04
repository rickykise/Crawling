import requests
import urllib
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://www.bgmys.com/vodshow/15-%E9%9F%A9%E5%9B%BD-------{}---.html'
    while check:
        i = i+1
        if i == 60:
            break
        try:
            r = requests.get(link.format(str(i)))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find('div','index-area').find_all('a','link-hover')
            
            for item in li:
                titleSub = item['title'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                url = 'https://www.bgmys.com'+item['href']
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div','videourl').find_all('a')
                
                for item in sub:
                    host_url = 'https://www.bgmys.com'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    origin_url = str(soup).split('player_data=')[1].split('"url":"')[1].split('",')[0].strip().replace('\\', '')
                    origin_osp = origin_url.split('//')[1]
                    if origin_url.find('https') == -1:
                        origin_url = 'https:'+origin_url
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    else:
                        origin_osp = origin_osp.split('.')[0]

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'bgmys',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
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

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("bgmys 크롤링 시작")
    startCrawling()
    print("bgmys 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
