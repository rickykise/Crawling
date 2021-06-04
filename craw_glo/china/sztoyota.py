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

def startCrawling(param):
    i = 0;check = True
    link = "http://sztoyota.com/vodshow/"+param[0]+"-%E9%9F%A9%E5%9B%BD-------{}---.html"
    
    while check:
        i = i+1
        if i == param[1]:
            break

        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'fcb-ul').find_all('li')
        try:
            for item in li:
                url = 'http://sztoyota.com'+item.find('div','movie-headline1').find('a')['href']
                titleSub = item.find('div','movie-headline1').find('a').text.strip()
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
                sub = soup.find('ul','details-con2-list').find_all('a')
                for item in sub:
                    if item['href'] == '#':
                        continue

                    host_url = 'http://sztoyota.com'+item['href']
                    title = titleSub+'_'+item['title']
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
                        'cnt_osp' : 'sztoyota',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': '',
                        'origin_url': 'http://sztoyota.com/player/play.html?url=' + origin_url,
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

    print("sztoyota 크롤링 시작")
    page = [['rihanju',30],['zongyi',22]]
    for item in page:
        startCrawling(item)
    print("sztoyota 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
