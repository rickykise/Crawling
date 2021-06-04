import requests
import urllib
import json
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
    link = 'http://gougou2018.com/hanju/{}'
    while check:
        i = i+1
        if i == 30:
            break

        r = requests.get(link.format('index.html' if i == 1 else 'index'+str(i)+'.html'))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'lmain').find_all('div','litem')
        try:
            for item in div:
                site_url = 'http://gougou2018.com'+item.find('strong').find('a')['href']
                titleSub = item.find('strong').find('a').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                soupSite = BeautifulSoup(requests.get(site_url).content,"html.parser")
                numList = [];urlList = [];playerList = []
                #youku
                if soupSite.find_all('div', class_='play-list',id=True):
                    for id in soupSite.find_all('div', class_='play-list',id=True):
                        playerList.extend(id.find_all('a'))
                    playerURL = 'http://gougou2018.com'+soupSite.find('div', class_='play-list',id=True).find('li').find('a')['href']
                    soup = BeautifulSoup(requests.get(playerURL).content,"html.parser")
                    scriptURL = 'http://gougou2018.com'+soup.find('div',id="player").find('script')['src']
                    videoListJson = json.loads(requests.get(scriptURL).content.decode('unicode-escape').replace('var VideoListJson=','').strip("'<>() ").replace('\'', '\"').replace('\\','').strip("';").split(',urlinfo=')[0])
                    for v in videoListJson:
                        numList.extend([v2.split('$')[0] for v2 in v[1]])
                        urlList.extend(['https://yongjiujiexi.net/m3u8.html?url='+v2.split('$')[1] for v2 in v[1]])
                #other
                if soupSite.find_all('div', class_='play-list', id=False):
                    for o in soupSite.find_all('div', class_='play-list', id=False):
                        otherList = o.find_all('a')
                        if otherList[0]['href'].find('pan.baidu.com') != -1 or otherList[0]['href'].find('/|file|[TSKS]') != -1:
                            break
                        playerList.extend(otherList)
                        numList.extend([p.text for p in otherList])
                        urlList.extend([p['href'] for p in otherList])
                
                for num,url,host in zip(numList,urlList,playerList):
                    host_url = host['href']
                    if host_url.find('http') == -1:
                        host_url = 'http://gougou2018.com'+host['href']
                    origin_url = url
                    origin_osp = origin_url.replace('https://yongjiujiexi.net/m3u8.html?url=','').split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('.')[1]
                    elif origin_url.find('jjhd') != -1:
                        origin_osp = '吉吉 影音'
                    else:
                        origin_osp = origin_osp.split('.')[0]
                    
                    title = titleSub + '_' + num
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'gougou2018',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': site_url,
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

    print("gougou2018 크롤링 시작")
    startCrawling()
    print("gougou2018 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
