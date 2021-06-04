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

headers={
    'age': '758',
    'cache-control': 'max-age=14400',
    'cf-cache-status': 'HIT',
    'cf-ray': '59cd2bd79daee794-LAX',
    'cf-request-id': '031419baba0000e7948e2e7200000001',
    'content-encoding': 'br',
    'content-type': 'text/html',
    'date': 'Tue, 02 Jun 2020 00:48:52 GMT',
    'expect-ct': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"',
    'last-modified': 'Mon, 01 Jun 2020 20:09:34 GMT',
    'server': 'cloudflare',
    'status': '200',
    'vary': 'Accept-Encoding',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}
def startCrawling():
    i = 0;check = True
    link = 'https://bigshows.org/%E9%9F%93%E7%B6%9C/'
    r = requests.get(link)
    r.encoding = r.apparent_encoding
    c = r.text
    soup = BeautifulSoup(c, 'html.parser')
    sub = soup.find('div', 'show_alone').find_all('a','sizing')
    for item in sub:
        try:
            url = 'https://bigshows.org'+item['href']
            titleSub = item['title']
            title_check = titleNull(titleSub)

            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_check, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']
            url = 'https://bigshows.org/深夜正式演藝/'
            r = requests.get(url,headers=headers)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            if r.status_code == 404 or soup.find('div','content').text.find('噢噢，您要找的頁面不存在') != -1:
                continue

            div = soup.find('div',id='album_items').find_all('a')
            for item in div:
                host_url = 'https://www.bigshows.com'+item['href']
                title = item['title'].strip()
                title_null = titleNull(title)

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'bigshows',
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
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("bigshows 크롤링 시작")
    startCrawling()
    print("bigshows 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
