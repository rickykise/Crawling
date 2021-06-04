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

def startCrawling(site):
    i = 0;check = True
    link = site[0]
    with requests.Session() as s:
        while check:
            i = i+1
            if i == site[1]:
                break
            r = requests.get(link.format(str(i)))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find_all('li', 'fed-list-item')

            try:
                for item in li:
                    url = 'https://tw.92drama.com'+item.find('a','fed-list-title')['href']
                    titleSub = item.find('a', 'fed-list-title').text.strip()
                    title_check = titleNull(titleSub)

                    imgUrl = item.find('a','fed-list-pics')['data-original']
                    # 이미지 체크
                    img_chk = 0
                    getIMG = getImage()
                    imgCheck = imageCheck(imgUrl, getIMG)
                    if imgCheck == None:
                        # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_check, getKey)
                        if keyCheck['m'] == None:
                            continue
                        cnt_id = keyCheck['i']
                        cnt_keyword = keyCheck['k']
                        otoImg = ''
                        cnt_cate = 0
                        img_chk = 0
                    else:
                        cnt_id = imgCheck['i']
                        cnt_keyword = imgCheck['k']
                        otoImg = imgCheck['m']
                        cnt_cate = imgCheck['c']

                        # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_check, getKey)
                        if keyCheck['m'] == None:
                            img_chk = 1
                        else:
                            img_chk = 2
                    
                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    div = soup.find_all('div', {'class':['fed-tabs-item','fed-drop-info']})

                    for item in div:
                        li = item.find_all('li',{'class':['fed-padding','fed-col-xs3','fed-col-md2','fed-col-lg1']})
                        for item in li:
                            if item.find('a','fed-btns-info') == None:
                                continue
                            host_url = 'https://tw.92drama.com'+item.find('a','fed-btns-info')['href']
                            title = titleSub+'_'+item.find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : '92drama',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'taiwan',
                                'cnt_writer': '',
                                'site_p_img': imgUrl,
                                'site_r_img': otoImg,
                                'site_img_chk': img_chk
                            }
                            dbResult = insertALL(data)
            except Exception as e:
                print(e)
                continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("92drama 크롤링 시작")
    site=[['https://tw.92drama.com/vod/show/area/%E9%9F%93%E5%9C%8B/id/15/page/{}.html',30],['https://tw.92drama.com/vod/show/area/%E9%9F%93%E5%9C%8B/id/3/page/{}.html',18]]
    for item in site:
        startCrawling(item)
    print("92drama 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
