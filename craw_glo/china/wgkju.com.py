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
    link = 'http://www.wgkju.com/index.php/vod/show/area/%E9%9F%A9%E5%9B%BD/id/15/page/{}.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('li', 'mo-paxs-5px')

        try:
            for item in li:
                url = 'http://www.wgkju.com'+item.find('a','mo-situ-name')['href']
                titleSub = item.find('a', 'mo-situ-name').text.strip()
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
                soup = BeautifulSoup(c,"html.parser")
                ul = soup.find_all('ul', 'mo-movs-item')
                for item in ul:
                    li = item.find_all('li','mo-cols-info')
                    for item in li:
                        if item.find('a','mo-part-btns') == None:
                            continue
                        host_url = 'http://www.wgkju.com'+item.find('a','mo-part-btns')['href']
                        title = titleSub+'_'+item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'wgkju.com',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'china',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("wgkju.com 크롤링 시작")
    startCrawling()
    print("wgkju.com 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
