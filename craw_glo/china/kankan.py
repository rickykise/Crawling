import requests,re
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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'KANKANWEBUID=66fd0efbefb6b01b4682d60db233e33e; adFilter_ck=1.0; KANKANWEBSESSIONID=bb132f566747b6b5a32b9bb168552195; vjuids=-15fd4b384.17254abe4cc.0.325609ea9a14a; cm_cookie_id=798c921ffa5557e40000017254abed32; Hm_lvt_f85580b78ebb540403fe1f04da080cfd=1590558453; gid=; blockid=; f_refer=http%253A%252F%252Fwww.kankan.com%252F; kklist_taglist_status=; kklist_channel_type=teleplay; __xltjbr=1590558491702; __gads=ID=45adfd60cf5dbc3c:T=1590558492:S=ALNI_MarVy8cVRiO8j5gvrP5n6Yiu9d0cQ; vjlast=1590558451.1590638180.13; Hm_lpvt_f85580b78ebb540403fe1f04da080cfd=1590639260',
    'Host': 'movie.kankan.com',
    'Referer': 'http://movie.kankan.com/type,order,area/teleplay,update,1/page2/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

def startCrawling():
    i = 0;check = True
    link = 'http://movie.kankan.com/type,order,area/teleplay,update,1/page{}/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)), allow_redirects=False, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', id='movie_list').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
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
                div = soup.find_all('div', {'class': ['section','s2']},id=re.compile('^change_first_'))
                for item in div:
                    li = item.find_all('li')
                    origin_osp = item['id'].replace('change_first_','')

                    for item in li:
                        host_url = item.find('a')['href']
                        origin_url = host_url
                        title = titleSub + '_' + item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'kankan',
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
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kankan 크롤링 시작")
    startCrawling()
    print("kankan 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
