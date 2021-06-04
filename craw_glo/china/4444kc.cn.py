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

def startCrawling(site):
    i = 0;check = True
    link = 'http://4444kc.cn/list/'+site+'/{}.html'
    while check:
        i = i+1
        if i == 30:
            break
        try:
            r = requests.get(link.format(str(i)))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find('div','index-area').find_all('li')

            for item in li:
                titleSub = item.find('a','link-hover')['title'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                site_url = 'http://4444kc.cn'+item.find('a')['href']
                r = requests.get(site_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")

                url = 'http://4444kc.cn'+soup.find('div','videourl').find_all('a')[0]['href']
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                script = soup.find('div','player').find('script')
                playList = ['http://4444kc.cn'+p['href'] for p in soup.find('div','videourl clearfix').find_all('a')]
                if script.string.find('unescape') != -1:
                    playerListStr = re.sub('[();\']', '', script.string.split('unescape')[1])
                    playerList = urllib.parse.unquote(playerListStr.replace('%u',r'\u').encode().decode('unicode-escape')).split('#')

                    for player,host_url in zip(playerList,playList):
                        arr = player.split('$')
                        title = titleSub+'_'+arr[0].strip()
                        title_null = titleNull(title)
                        origin_url = arr[1]
                        origin_osp = origin_url.split('//')[1]

                        if origin_osp.find('www') != -1:
                            origin_osp = origin_osp.split('www.')[1].split('.')[0]
                        else:
                            origin_osp = origin_osp.split('.')[0]

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : '4444kc.cn',
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

    print("4444kc.cn 크롤링 시작")
    site = ['2','3']
    for s in site:
        startCrawling(s)
    print("4444kc.cn 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
