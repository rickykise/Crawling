import requests
import urllib
import time
import json
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
    link = 'https://xiamov.com/l/s-2-mcid--letter--year--area-%E9%9F%A9%E5%9B%BD-order--p-{}.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        try:
            sub = soup.find_all('a', 'le-playico')

            for item in sub:
                url = 'https://xiamov.com'+item['href']
                titleSub = item.find('img')['alt'].strip()
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
                if soup.find('ul','play-list') == None:
                    continue
                href = 'https://xiamov.com'+soup.find('ul','play-list').find('a')['href']

                r = requests.get(href)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")

                if soup.find('div',id='player2').find('script'):
                    player = soup.find('div',id='player2').find('script').string.replace('var ff_urls=','').replace('\\','').strip("';")
                    playerJson = json.loads(player)
                    for j in playerJson['Data']:
                        if len(j) == 0:
                            break
                        playurls = [p for p in j['playurls']]
                        for u in playurls:
                            title = titleSub+'_'+urllib.parse.unquote(u[0].replace('u',r'\u').encode().decode('unicode-escape'))
                            title_null = titleNull(title)
                            host_url = 'https://xiamov.com'+u[2]
                            origin_url = u[1]
                            if origin_url.find('http') != -1:
                                origin_osp = origin_url.split('//')[1]
                                if origin_osp.find('www') != -1:
                                    origin_osp = origin_osp.split('www.')[1].split('.')[0]
                                else:
                                    origin_osp = origin_osp.split('.')[0]
                            else:
                                origin_osp = ''
                                origin_url = ''

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'xiamov',
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
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("xiamov 크롤링 시작")
    startCrawling()
    print("xiamov 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
