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
    link = "https://kdramastv.com/page/{}/"
    while check:
        i = i+1
        if i == 251:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        h3 = soup.find('div', id='main-content').find_all('h3',"post-box-title")

        try:
            for item in h3:
                url = item.find('a')['href']
                title = item.find('a').text
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                iframe = soup.find_all('iframe')

                for item in iframe:
                    origin_url = item['src']

                    if origin_url.find('http') == -1:
                        origin_url = 'https:'+origin_url
                    origin_osp = origin_url.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    elif origin_osp.find('myqcloud') != -1:
                        origin_osp = 'myqcloud'
                    else:
                        origin_osp = origin_osp.split('.')[0]

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'kdramastv',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'other',
                        'cnt_writer': '',
                        'origin_url': origin_url,
                        'origin_osp': origin_osp
                    }

                    dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kdramastv 크롤링 시작")
    startCrawling()
    print("kdramastv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
