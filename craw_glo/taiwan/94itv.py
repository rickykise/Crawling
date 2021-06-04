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
    while check:
        i = i+1
        if i == site[1]:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'vodlist').find_all('li','vodlist_item')
        try:
            for item in li:
                imgUrl = item.find('a')['data-original']
                url = 'https://94itv.net'+item.find('a')['href']
                titleSub = item.find('a')['title'].strip()
                title_check = titleNull(titleSub)
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
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div', 'play_source').find_all('a',href=lambda x: x and "/vod-play-id" in x)
                for item in sub:
                    host_url = 'https://94itv.net'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : '94itv',
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
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("94itv 크롤링 시작")
    site=[['https://94itv.net/vod-show-id-15-page-{}.html',17],['https://94itv.net/vod-show-area-%E9%9F%A9%E5%9B%BD-id-3-page-{}.html',8]]
    for item in site:
        startCrawling(item)
    print("94itv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
