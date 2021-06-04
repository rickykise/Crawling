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

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'UM_distinctid=17254b88e9d1e6-0ae2b14285170f-f7d1d38-1fa400-17254b88e9e9a9; ASPSESSIONIDQESRBTCB=GFOAMKFCKADKEIKJKDNOEIDB; ASPSESSIONIDSERSCSBA=AMDAEFNCGLLPBEIMODEKFJOP; ASPSESSIONIDQESRCTAB=CDCGIJOCKKOEIBEKNHIALIJG; CNZZDATA1261686144=1506290927-1590554560-%7C1590642475; cscpvrich8992_fidx=2',
    'referer': 'https://www.77ds.vip/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'Content-Type':'text/html; charset=utf-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}
def startCrawling():
    i = 0;check = True
    link = 'https://www.77ds.vip/{}_21_____%BA%AB%B9%FA.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(c, 'html.parser')
        li = soup.find('div', 'bolist_body').find_all('li')

        try:
            for item in li:
                url = 'https://www.77ds.vip'+item.find('a')['href']
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
                div = soup.find_all('div', 'bofang_content_body')
                for item in div:
                    sub = soup.find_all('dt')
                    for item in sub:
                        if item.find('a') == None:
                            continue
                        host_url = 'https://www.77ds.vip'+item.find('a')['href']
                        title = titleSub + '_' + item.find('a')['title'].strip()
                        title_null = titleNull(title)
        
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : '77ds',
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
                        print(data)
                        print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("77ds 크롤링 시작")
    startCrawling()
    print("77ds 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
