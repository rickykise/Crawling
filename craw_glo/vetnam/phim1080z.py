import requests
import time
import sys, os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://phim1080z.com/phim-bo/han-quoc?page={}'
    while check:
        i = i+1
        if i == 13:
            break

        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find_all('div',  'tray-item')

        try:
            for item in div:
                if item.find('a'):
                    url = item.find('a')['href']
                    url = 'https://phim1080z.com'+url
                    titleSub = item.find('a').find('img', 'tray-item-thumbnail')['alt'].replace('\n', '')
                    title_check = titleNull(titleSub)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check,  getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']
                    
                    tapStr = item.find('div',  'tray-film-likes').text
                    if tapStr.find('tập') == -1:
                        continue
                    
                    tapNum = int(tapStr.split(' / ')[0].strip())
                    for i in range(1, tapNum):
                        host_url = url+'/tap-'+str(i)
                        title_num = str(i)
                        title = titleSub+'_'+title_num
                        title_null = titleNull(title)
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'phim1080z',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url': host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'vietnam',
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

    print("phim1080z 크롤링 시작")
    startCrawling()
    print("phim1080z 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
