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

def startCrawling():
    i = 0;check = True
    link = 'https://www.sosoys.net/type/21-{}.html'
    while check:
        i = i+1
        if i == 12:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul','stui-vodlist').find_all('li')
        try:
            for item in li:
                titleSub = item.find('a')['title'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                url = 'https://www.sosoys.net'+item.find('a')['href']
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div','col-lg-wide-75 col-xs-1').find_all('a',target="_self")
                for item in sub:
                    host_url = 'https://www.sosoys.net'+item['href']
                    title = titleSub+'_'+item['title'].strip()
                    title_null = titleNull(title)
                    soup = BeautifulSoup(requests.get(host_url).content,"html.parser")
                    script = soup.find('div','stui-player__iframe').find('script')
                    if script.string.find('unescape') != -1:
                        ourl = re.sub('[();\'\"]', '', script.string.split('unescape')[1].split(');var pn=')[0])
                        origin_url = urllib.parse.unquote(ourl)
                        origin_osp = origin_url.split('//')[1]
                        if origin_url.find('http') == -1:
                            origin_url = ''
                            origin_osp = ''
                        else:
                            if origin_osp.find('www') != -1:
                                origin_osp = origin_osp.split('www.')[1].split('.')[0]
                            else:
                                origin_osp = origin_osp.split('.')[0]
                    else:
                        origin_url = ''
                        origin_osp = ''
                            
                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'sosoys',
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

    print("sosoys 크롤링 시작")
    startCrawling()
    print("sosoys 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
