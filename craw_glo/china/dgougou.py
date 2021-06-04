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
    link = 'http://www.dgougou.com/index.php?s=home-vod-type-id-23-mcid--area--year--letter--order--picm-1-p-{}'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        r.encoding = r.apparent_encoding
        c = r.content
        soup = BeautifulSoup(c, 'html.parser')
        li = soup.find('ul', id='content').find_all('li')

        try:
            for item in li:
                url = 'http://www.dgougou.com'+item.find('a')['href']
                titleSub = item.find('a')['title']
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
                playTab = soup.find('ul', id='playTab').find_all('li','hidden-xs')
                if soup.find('li','player-more'):
                    playTab2 = soup.find('li','player-more').find('ul', 'dropdown-menu').find_all('li')
                    playTab.extend(playTab2)

                palyList = soup.find_all('ul','clearfix',id=re.compile('^con_playlist_'))
                for item,item2 in zip(playTab,palyList):
                    origin_osp = item.text
                    sub = item2.find_all('li')
                    for item in sub:
                        host_url = 'http://www.dgougou.com'+item.find('a')['href']
                        origin_url = host_url
                        title = titleSub + '_' + item.find('a').text.strip()
                        title_null = titleNull(title)
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'dgougou',
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

    print("dgougou 크롤링 시작")
    startCrawling()
    print("dgougou 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
