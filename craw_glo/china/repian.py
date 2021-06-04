import requests
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
    link = 'https://list.repian.com/{}_22__%BA%AB%B9%FA____.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        r.encoding = r.apparent_encoding
        c = r.text
        soup = BeautifulSoup(c, 'html.parser')
        li = soup.find('ul', id="contents").find_all('li')

        try:
            for item in li:
                url = 'https:'+item.find('div','play-txt').find('h5').find('a')['href']
                titleSub = item.find('div','play-txt').find('h5').find('a').text
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
                div = soup.find_all('div','play-list-box')
                for item in div:
                    origin_osp = item['id'].replace('-pl-list','')
                    sub = soup.find('p','play-list').find_all('a')
                    for item in sub:
                        host_url = 'https://www.repian.com'+item['href']
                        origin_url = host_url
                        title = titleSub + '_' + item['title'].strip()
                        title_null = titleNull(title)
        
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'repian',
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("repian 크롤링 시작")
    startCrawling()
    print("repian 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
